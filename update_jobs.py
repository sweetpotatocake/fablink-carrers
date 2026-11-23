"""FABLINK scheduled discovery.

Uses the public Bing RSS search endpoint (no signup or API key), and accepts
only directly fetched schema.org JobPosting entries with a future validThrough
and clear 4-year degree.
This is best-effort discovery, NOT a comprehensive/live status guarantee.
"""
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATH = ROOT / 'data.json'
DATA = json.loads(PATH.read_text(encoding='utf-8'))
TZ = dt.timezone(dt.timedelta(hours=9))
NOW = dt.datetime.now(TZ)
TODAY = NOW.date()
STAMP = NOW.strftime('%Y-%m-%d %H:%M KST')
BASIC = [
    '반도체 공정기술 공정개발 신입 4년제 채용',
    '반도체 전공정 증착 식각 세정 엔지니어 학사 채용',
    '반도체 후공정 패키징 범핑 테스트 학사 신입 채용',
    'PCB 패키지기판 공정기술 생산기술 대졸 채용',
    '도금액 표면처리 첨가제 품질 공정 엔지니어 학사 채용',
    '반도체 소재 케미컬 공정개발 품질 학사 채용',
    'semiconductor process engineer bachelor Korea hiring',
    'site:saramin.co.kr/job-search/view 반도체 공정기술 학사 신입',
    'site:jobkorea.co.kr/Recruit/GI_Read 반도체 공정개발 대졸 신입',
]
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; FABLINK-job-discovery/1.0)'}


def fetch(url, payload=None):
    headers = dict(HEADERS)
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8') if payload is not None else None, headers=headers)
    with urllib.request.urlopen(req, timeout=16) as response:
        return response.read().decode('utf-8', errors='replace')


def search(q):
    # Bing's public RSS search response may change or be blocked at any time.
    # A valid RSS document with zero items is a successful search, NOT verified jobs.
    url = 'https://www.bing.com/search?' + urllib.parse.urlencode({
        'q': q, 'format': 'rss', 'setlang': 'ko-KR', 'cc': 'KR'
    })
    try:
        body = fetch(url)
        root = ET.fromstring(body)
        if root.tag != 'rss':
            raise ValueError('response was not RSS')
        links = []
        for item in root.findall('./channel/item'):
            link = (item.findtext('link') or '').strip()
            if link.startswith('https://'):
                links.append(link)
        return list(dict.fromkeys(links)), True
    except Exception as exc:
        print('RSS search failed:', q[:50], str(exc)[:160])
        return [], False


def parse_date(value):
    if not value:
        return None
    m = re.search(r'(20\d\d)[-/\.년 ]+(\d{1,2})[-/\.월 ]+(\d{1,2})', str(value))
    if not m:
        return None
    try:
        return dt.date(*map(int, m.groups()))
    except ValueError:
        return None


def all_jobs(node):
    if isinstance(node, list):
        for item in node:
            yield from all_jobs(item)
    elif isinstance(node, dict):
        types = node.get('@type', [])
        types = types if isinstance(types, list) else [types]
        if any(str(t).lower().split('/')[-1] == 'jobposting' for t in types):
            yield node
        for k, v in node.items():
            if k != '@context':
                yield from all_jobs(v)


def strip_tags(text):
    return html.unescape(re.sub(r'<[^>]+>', ' ', str(text or '')))


def degree_valid(job):
    education = job.get('educationRequirements', '')
    if isinstance(education, (list, dict)):
        education = json.dumps(education, ensure_ascii=False)
    education = strip_tags(education).lower()
    if re.search(r'학력\s*무관|고졸\s*이상|초대졸\s*이상|high school', education):
        return False
    return bool(re.search(r'4년제|대졸\s*\(?4년\)?|학사|석사|박사|bachelor|master|ph\.?d|university degree', education))


def parse_post(url):
    try:
        page = fetch(url)
        scripts = re.findall(r'<script\b[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>(.*?)</script>', page, re.I | re.S)
        results = []
        for raw in scripts:
            try:
                nodes = list(all_jobs(json.loads(raw.strip())))
            except (ValueError, TypeError):
                continue
            for job in nodes:
                deadline = parse_date(job.get('validThrough'))
                if not deadline or deadline < TODAY or not degree_valid(job):
                    continue
                title = strip_tags(job.get('title', '')).strip()
                organization = job.get('hiringOrganization') or {}
                company = organization.get('name', '') if isinstance(organization, dict) else str(organization)
                if not title or not company:
                    continue
                target = title + ' ' + company
                if not re.search(r'반도체|공정|PCB|패키|도금|표면처리|소재|장비|설계|품질|엔지니어|semiconductor|process|plating|etch|test|assembly|engineer', target, re.I):
                    continue
                desc = strip_tags(job.get('description', ''))
                if re.search(r'경력\s*[1-9]|[1-9]\s*years|experienced', title + ' ' + desc, re.I):
                    experience = '경력 (원문 확인)'
                elif re.search(r'신입|entry.level|new grad|graduate', title + ' ' + desc, re.I):
                    experience = '신입 (원문 확인)'
                else:
                    experience = '신입·경력 확인 필요'
                company_norm = re.sub(r'\s', '', company).lower()
                sector = next((c['sector'] for c in DATA['companies'] if re.sub(r'\s', '', c['name']).lower() == company_norm), '기타 반도체')
                location = job.get('jobLocation', '')
                if isinstance(location, list):
                    location = location[0] if location else ''
                if isinstance(location, dict):
                    addr = location.get('address', '')
                    location = ' '.join(str(addr.get(k, '')) for k in ('addressRegion', 'addressLocality')) if isinstance(addr, dict) else str(addr)
                canonical = str(job.get('url') or url)
                if not canonical.startswith('https://'):
                    canonical = url
                results.append({
                    'id': 'live-' + hashlib.sha256(canonical.encode()).hexdigest()[:16],
                    'company': company, 'title': title, 'sector': sector,
                    'degree': '학사 이상', 'experience': experience,
                    'location': str(location).strip()[:80] or '원문 확인',
                    'deadline': deadline.isoformat(), 'url': canonical,
                    'source': urllib.parse.urlparse(url).netloc,
                    'degreeVerified': True, 'verifiedAt': TODAY.isoformat(),
                    'note': '공개 구조화 데이터의 학력/마감일 확인 · 실제 접수/조기마감 원문 확인',
                    'automated': True,
                })
        return results
    except Exception:
        return []


def main():
    # 137 firms spread across ~7 days to limit free RSS requests; broad searches run daily.
    firms = list({c['name']: c for c in DATA['companies']}.values())
    slot = (TODAY - dt.date(2026, 1, 1)).days % 7
    queries = BASIC + [f'"{c["name"]}" 채용 학사 공정기술 엔지니어' for i, c in enumerate(firms) if i % 7 == slot]
    with ThreadPoolExecutor(max_workers=4) as executor:
        batches = list(executor.map(search, queries))
    success = sum(ok for _, ok in batches)
    if not success:
        print('ERROR: All search requests failed. Snapshot will not be marked refreshed.', file=sys.stderr)
        return 1
    urls = list(dict.fromkeys(url for group, _ in batches for url in group))[:240]
    with ThreadPoolExecutor(max_workers=6) as executor:
        fresh = [job for group in executor.map(parse_post, urls) for job in group]
    dedup = {j['url']: j for j in fresh}
    # Previously discovered links stay only if revalidated within 7 days.
    for old in DATA.get('jobs', []):
        deadline = parse_date(old.get('deadline'))
        checked = parse_date(old.get('verifiedAt'))
        if deadline and deadline >= TODAY and checked and (TODAY - checked).days <= 7:
            dedup.setdefault(old['url'], old)
    DATA['jobs'] = sorted(dedup.values(), key=lambda j: (j['deadline'], j['company']))
    DATA['checkedAt'] = TODAY.isoformat()
    DATA['sync'] = {
        'mode': 'public-rss-search',
        'lastAttemptAt': STAMP,
        'lastSearchSuccessAt': STAMP,
        'searchQueries': len(queries), 'queriesSucceeded': success,
        'candidatePages': len(urls), 'freshlyVerified': len(fresh),
        'firmsCheckedThisRun': sum(i % 7 == slot for i in range(len(firms))),
        'totalRegisteredFirms': len(firms),
        'scope': 'Bing 공개 RSS 검색 기반 · 구조화 데이터가 확인된 일부 공고만 표시 · 전체 채용공고 수집 아님',
    }
    PATH.write_text(json.dumps(DATA, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Successful searches {success}/{len(queries)}, candidates {len(urls)}, verified {len(fresh)}, shown {len(DATA["jobs"])}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
