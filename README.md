# FABLINK · 자동 갱신 반도체 채용 대시보드

137개 기업을 공정별로 탐색하고 **최근 7일 안에 학력 및 마감일을 확인한** 공개 공고를 볼 수 있는 채용 대시보드입니다. 채용 마감일이 미래라는 이유만으로 실시간 접수 중임을 보장하지 않으며, 회사 공식 공고의 최신 상태가 우선입니다.

## 1. 중요한 차이: 로컬 HTML vs. 지속적으로 갱신되는 웹사이트

- `index.html`을 컴퓨터에서 열면 **현재 저장된 스냅샷**만 보입니다. 시간이 지나도 이 파일은 저절로 바뀌지 않습니다.
- **GitHub 저장소 + GitHub Pages + GitHub Actions + 검색 API**를 연결하면 새로 게시되는 온라인 사이트에서 자동 갱신된 데이터를 볼 수 있습니다.
- 자동화 주기: **매일 한국시간 08:17**(UTC 전날 23:17). GitHub 처리량에 따라 지연되거나 누락될 수 있습니다.
- 자동 검색 대상은 일부 공개 공고만입니다. **137개 기업의 모든 공고, 모든 채용 플랫폼의 공고를 완전하게 수집하는 기능이 아닙니다.** 각 채용 사이트의 접근 정책과 스키마 지원 여부에 따라 누락됩니다.

## 2. 처음 한 번 설정하기

1. https://github.com 에 로그인하고 새 **Public repository** (예: `fablink-careers`)를 만듭니다.
2. 이 ZIP 안의 `FABLINK` **폴더 안에 있는 파일과 숨김 `.github` 폴더까지** 저장소 루트에 업로드합니다. 반드시 `.github/workflows/refresh-and-deploy.yml` 경로를 유지합니다.
3. https://serper.dev 에서 검색 API 키를 발급받습니다. 유료 한도/무료 크레딧은 서비스의 현재 정책을 확인합니다.
4. GitHub 저장소 → **Settings → Secrets and variables → Actions → New repository secret**에서 이름 `SERPER_API_KEY`, 값은 발급받은 API 키로 저장합니다. **키를 HTML이나 data.json에 적지 마세요.**
5. GitHub 저장소 → **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 선택합니다.
6. GitHub 저장소 → **Actions → FABLINK daily refresh and publish → Run workflow**를 1회 실행하고 성공 여부를 확인합니다.
7. **Settings → Pages**에서 발급된 `https://<아이디>.github.io/<저장소>/` 주소를 즐겨찾기 하세요. 몇 달 후에는 다운로드한 HTML이 아닌 **이 주소**로 접속해야 최신 데이터를 봅니다.

> GitHub Actions에 쓰기 권한이 제한된 조직 설정에서는 Repository Settings → Actions → General → Workflow permissions를 확인해야 할 수 있습니다. Pages 환경 승인 정책도 확인하세요.

## 3. 검색 방식과 신뢰도

- 기본 산업 키워드 9개를 매일 검색하고, 회사명 목록 137개를 **7일에 나누어 순환 검색**합니다. 따라서 특정 기업이 매일 모두 검색되는 방식은 아닙니다.
- 검색 결과의 실제 공개 웹페이지에서 `schema.org/JobPosting`의 `educationRequirements`와 `validThrough`가 구체적으로 제공되는 경우만 공고에 추가합니다.
- **4년제 학사/석사/박사 이상**이 명시된 경우만 수록합니다. `고졸 이상`, `초대졸 이상`, `학력무관`은 제외하고, 학력 정보가 누락된 공고도 제외합니다.
- 7일 동안 재확인이 없는 공고는 메인 목록에서 자동 제외합니다. 마감된 공고도 제외합니다. 원문 삭제나 조기마감까지 실시간 보장하지는 않습니다.
- `data.json`의 `sync.lastSearchSuccessAt`가 마지막 자동 검색 성공 시각입니다. 검색 성공은 공고 검증 성공을 의미하지 않으며, 검증 건수는 `freshlyVerified`를 확인합니다.
- 누락된 기업과 채용공고는 '전체 기업 탐색'의 기업 홈페이지/채용 사이트 검색으로 확인할 수 있습니다.

## 4. 장기 운영 시 반드시 알아야 할 점

- **GitHub는 공개 저장소에서 60일간 활동이 없으면 정기 실행을 자동으로 비활성화할 수 있습니다.** 이 경우 Actions에서 다시 활성화해야 합니다. 검색 API 잔여 쿼터 소진·키 만료·웹사이트 구조 변경·GitHub 장애·이용정책 변경 등으로도 갱신이 중단될 수 있습니다.
- 공개 저장소에서 Actions가 자동으로 새 데이터 커밋을 만들 수 있지만, 이것만으로 60일 비활성화가 절대 일어나지 않는다고 보장하지 않습니다.
- GitHub Actions는 엄밀한 실시간 스트리밍이 아니라 **일일 배치 검색**입니다. 연속 실시간 모니터링 또는 모든 채용정보의 완전한 집계가 필요하면 공식 제휴/채용 API 및 상시 서버 운영이 추가로 필요합니다.
- 검색 API 사용량/비용을 수시로 확인하세요. 기본 설정은 검색 9개 + 기업 약 19~20개 = **약 29개 검색/일**입니다.
- 프로세스 실행 실패 시 기존 게시 사이트는 그대로 남을 수 있습니다. 화면의 `마지막 검색 시각`을 확인하세요.

## 5. 수동 실행/수정

```
# 갱신 (SERPER_API_KEY를 환경변수로 설정한 상태)
python update_jobs.py
python render.py
```

기업 추가: `data.json`의 `companies` 배열에 이름/업종/규모/홈페이지를 수정하고 `python render.py`를 실행합니다. 브라우저 관심기업 기능은 해당 브라우저 로컬 스토리지에만 보관됩니다.

## 파일 안내
- `index.html`: GitHub Pages에서 실제로 열리는 사이트
- `site.html`: 사이트 템플릿 (독립 실행 불가)
- `data.json`: 기업, 공고, 마지막 갱신 메타데이터
- `update_jobs.py`: 공개 검색 API + 구조화 공고 검증
- `render.py`: 템플릿과 데이터를 합쳐 새 index.html 생성
- `.github/workflows/refresh-and-deploy.yml`: 매일 검색, 저장, GitHub Pages 배포
- `build.py`: 초기 기업/공고 데이터 참고 스크립트 (운영 중 재실행하면 데이터 덮어쓸 수 있음)
