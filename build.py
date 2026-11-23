import json,html
from pathlib import Path
# company list: name, category, tier
raw='''삼성전자|전공정·제조|대기업
SK하이닉스|전공정·제조|대기업
DB하이텍|전공정·제조|중견기업
키파운드리|전공정·제조|중견기업
SK키파운드리|전공정·제조|중견기업
매그나칩반도체|전공정·제조|중견기업
LX세미콘|설계·팹리스|대기업
텔레칩스|설계·팹리스|중견기업
어보브반도체|설계·팹리스|중견기업
실리콘마이터스|설계·팹리스|강소기업
리노공업|후공정·검사|중견기업
하나마이크론|후공정·검사|중견기업
SFA반도체|후공정·검사|중견기업
네패스|후공정·검사|중견기업
네패스아크|후공정·검사|중견기업
LB세미콘|후공정·검사|중견기업
LB루셈|후공정·검사|중견기업
두산테스나|후공정·검사|중견기업
시그네틱스|후공정·검사|중견기업
앰코테크놀로지코리아|후공정·검사|중견기업
ASE코리아|후공정·검사|중견기업
스태츠칩팩코리아|후공정·검사|중견기업
ISC|후공정·검사|중견기업
마이크로컨텍솔|후공정·검사|강소기업
티에스이|후공정·검사|중견기업
디아이|후공정·검사|중견기업
테크윙|후공정·검사|중견기업
인텍플러스|후공정·검사|중견기업
고영테크놀러지|후공정·검사|중견기업
아이엠티|후공정·검사|강소기업
삼성전기|PCB·패키지기판|대기업
LG이노텍|PCB·패키지기판|대기업
대덕전자|PCB·패키지기판|중견기업
이수페타시스|PCB·패키지기판|중견기업
심텍|PCB·패키지기판|중견기업
코리아써키트|PCB·패키지기판|중견기업
디에이피|PCB·패키지기판|중견기업
디에이피솔루션즈|PCB·패키지기판|강소기업
대덕|PCB·패키지기판|중견기업
현우산업|PCB·패키지기판|중견기업
이녹스첨단소재|PCB·패키지기판|중견기업
디에이피|PCB·패키지기판|중견기업
디에스케이|PCB·패키지기판|중견기업
뉴프렉스|PCB·패키지기판|중견기업
인터플렉스|PCB·패키지기판|중견기업
영풍전자|PCB·패키지기판|중견기업
시노펙스|PCB·패키지기판|중견기업
타이거일렉|PCB·패키지기판|강소기업
이브이첨단소재|PCB·패키지기판|중견기업
스템코|PCB·패키지기판|중견기업
대만 유니마이크론|PCB·패키지기판|대기업
세메스|전공정 장비|대기업
원익IPS|전공정 장비|중견기업
주성엔지니어링|전공정 장비|중견기업
유진테크|전공정 장비|중견기업
테스|전공정 장비|중견기업
PSK|전공정 장비|중견기업
피에스케이홀딩스|후공정·검사|중견기업
케이씨텍|전공정 장비|중견기업
에이피티씨|전공정 장비|중견기업
브이엠|전공정 장비|중견기업
넥스틴|전공정 장비|중견기업
제우스|전공정 장비|중견기업
한미반도체|후공정·검사|중견기업
SFA|전공정 장비|중견기업
에스티아이|전공정 장비|중견기업
에프에스티|전공정 장비|중견기업
아이씨디|전공정 장비|중견기업
에스엔유프리시젼|전공정 장비|중견기업
에스에프에이|전공정 장비|중견기업
로체시스템즈|전공정 장비|중견기업
아이엠티|전공정 장비|강소기업
에스피지|전공정 장비|중견기업
ASML코리아|외국계 장비|대기업
어플라이드머티어리얼즈코리아|외국계 장비|대기업
램리서치코리아|외국계 장비|대기업
도쿄일렉트론코리아|외국계 장비|대기업
KLA코리아|외국계 장비|대기업
SCREEN SPE 코리아|외국계 장비|중견기업
스크린에스피이코리아|외국계 장비|중견기업
원익머트리얼즈|소재·도금약품|중견기업
솔브레인|소재·도금약품|중견기업
동진쎄미켐|소재·도금약품|중견기업
이엔에프테크놀로지|소재·도금약품|중견기업
한솔케미칼|소재·도금약품|중견기업
후성|소재·도금약품|중견기업
SK스페셜티|소재·도금약품|대기업
SK실트론|소재·도금약품|대기업
OCI|소재·도금약품|대기업
덕산테코피아|소재·도금약품|중견기업
덕산하이메탈|소재·도금약품|중견기업
레이크머티리얼즈|소재·도금약품|중견기업
디엔에프|소재·도금약품|중견기업
퓨릿|소재·도금약품|중견기업
와이엠티|소재·도금약품|중견기업
켐트로닉스|소재·도금약품|중견기업
LT메탈|소재·도금약품|중견기업
삼화페인트공업|소재·도금약품|중견기업
맥더미드 퍼포먼스 솔루션즈 코리아|소재·도금약품|중견기업
아토텍코리아|소재·도금약품|중견기업
엔쏘닉|소재·도금약품|강소기업
와이씨켐|소재·도금약품|중견기업
미원상사|소재·도금약품|중견기업
램테크놀러지|소재·도금약품|중견기업
케이씨코트렐|소재·도금약품|중견기업
에이디텍|설계·팹리스|강소기업
딥엑스|설계·팹리스|강소기업
에이앤아이|전공정 장비|강소기업
리버트론|설계·팹리스|강소기업
코비스테크놀로지|전공정 장비|강소기업
테라다인코리아|외국계 장비|대기업
키사이트테크놀로지스코리아|외국계 장비|대기업
에이디테크놀로지|설계·팹리스|중견기업
가온칩스|설계·팹리스|중견기업
에이직랜드|설계·팹리스|중견기업
오픈엣지테크놀로지|설계·팹리스|중견기업
퀄리타스반도체|설계·팹리스|강소기업
파두|설계·팹리스|중견기업
제주반도체|설계·팹리스|중견기업
넥스트칩|설계·팹리스|중견기업
에이엘티|후공정·검사|중견기업
윈팩|후공정·검사|중견기업
큐알티|후공정·검사|중견기업
아이텍|후공정·검사|중견기업
오로스테크놀로지|전공정 장비|중견기업
엘오티베큠|전공정 장비|중견기업
엔투텍|전공정 장비|강소기업
에이프로|전공정 장비|중견기업
기가비스|PCB·패키지기판|중견기업
코세스|후공정·검사|중견기업
유니셈|전공정 장비|중견기업
GST|전공정 장비|중견기업
지오엘리먼트|소재·도금약품|강소기업
미코|소재·도금약품|중견기업
원익QnC|소재·도금약품|중견기업
월덱스|소재·도금약품|중견기업
하나머티리얼즈|소재·도금약품|중견기업
티씨케이|소재·도금약품|중견기업
코미코|소재·도금약품|중견기업'''
seen=set(); companies=[]
for row in raw.splitlines():
 name,sector,tier=row.split('|');
 if name in seen:continue
 seen.add(name);companies.append(dict(name=name,sector=sector,tier=tier))
# verified as-of Nov 23; academic (4 year) explicit
jobs=[
 dict(company='스크린에스피이코리아',title='반도체 장비 CS 및 SET UP 엔지니어 (신입)',sector='외국계 장비',degree='학사 이상',experience='신입',location='평택·이천·청주·용인 등',deadline='2026-11-23',url='https://m.saramin.co.kr/job-search/view?rec_idx=55502916',source='사람인',note='학위 요건은 원문에서 재확인 필요',degreeVerified=False),
 dict(company='에이디텍',title='반도체 IC Field Application Engineer',sector='설계·팹리스',degree='학사 이상',experience='신입',location='경기',deadline='2026-11-30',url='https://m.saramin.co.kr/job-search/view?rec_idx=55628814',source='사람인',note='4년제 대졸 이상 명시',degreeVerified=True),
 dict(company='딥엑스',title='AI 반도체 Field Application Engineer (영어 가능)',sector='설계·팹리스',degree='학사 이상',experience='신입',location='성남 판교',deadline='2026-11-30',url='https://m.saramin.co.kr/job-search/view?rec_idx=55640718',source='사람인',note='4년제 대졸 이상 명시',degreeVerified=True),
 dict(company='에이앤아이',title='반도체 자동화 장비 운영 및 비전 SW 개발',sector='전공정 장비',degree='학사 이상',experience='신입·경력',location='경기 수원',deadline='2026-11-30',url='https://m.saramin.co.kr/job-search/view?rec_idx=55170549',source='사람인',note='4년제 대졸 이상 명시',degreeVerified=True),
 dict(company='리버트론',title='Hardware 설계 엔지니어 (회로·PCB)',sector='설계·팹리스',degree='학사 이상',experience='신입·경력',location='서울 영등포',deadline='2026-11-30',url='https://m.saramin.co.kr/job-search/view?rec_idx=55564005',source='사람인',note='반도체 관련 전공 우대·학사 이상',degreeVerified=True),
 dict(company='에이디텍',title='PCB 해외 기술영업 (중국어·영어 가능자)',sector='PCB·패키지기판',degree='학사 이상',experience='신입',location='경기 화성',deadline='2026-11-30',url='https://m.saramin.co.kr/job-search/view?rec_idx=55628776',source='사람인',note='PCB 관련 직무·4년제 대졸 이상',degreeVerified=True),
 dict(company='맥더미드 퍼포먼스 솔루션즈 코리아',title='Technical Service Engineer — PCB 표면처리',sector='소재·도금약품',degree='학사 이상',experience='경력 5~10년',location='경기 안산',deadline='2026-11-30',url='https://m.saramin.co.kr/job-search/view?rec_idx=55604541',source='사람인',note='4년제 대졸·경력 5~10년',degreeVerified=True),
 dict(company='미공개 반도체부품 기업',title='도금 공정 엔지니어 (헤드헌팅)',sector='소재·도금약품',degree='학사 이상',experience='경력 4~8년',location='충북 청주',deadline='2026-11-30',url='https://m.saramin.co.kr/job-search/view?rec_idx=55633733',source='사람인',note='고용 기업명 비공개·4년제 대졸 이상',degreeVerified=True),
 dict(company='테라다인코리아',title='반도체 기구 설계 엔지니어',sector='외국계 장비',degree='학사 이상',experience='경력',location='공고 참조',deadline='2026-11-30',url='https://m.jobkorea.co.kr/Recruit/GI_Read/50363609',source='잡코리아',note='대졸 이상·채용 시 조기 마감 가능',degreeVerified=True),
]
# remove degree-unverified from primary; put in review
for j in jobs:j['verifiedAt']='2026-11-23';j['id']=len([x for x in jobs if x is not j]) # replaced below
for i,j in enumerate(jobs):j['id']='job'+str(i+1)
Path('/mnt/data/career_hub/data.json').write_text(json.dumps(dict(companies=companies,jobs=jobs,checkedAt='2026-11-23'),ensure_ascii=False,indent=2))
print(len(companies),len(jobs))
