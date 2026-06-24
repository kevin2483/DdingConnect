# DdingConnect
띵커넥트 (DdingConnect) — 데이터 파트 핵심 코드


캡스톤 프로젝트 띵커넥트에서 제가 담당한 데이터 파트 코드입니다.
전체 프로젝트는 팀 레포지토리(Private)에서 관리되며, 본 레포는 제 기여 파트만 공개합니다.




📌 프로젝트 소개

띵커넥트는 진로 고민 중인 융합소프트웨어학부 학생에게 관심 직무·기술 스택·목표 기업이 유사한 졸업생 선배를 실시간으로 추천하는 커피챗 매칭 서비스입니다.


🧠 핵심 문제 & 해결 방법

콜드 스타트(Cold Start) 문제

사용자 초기 이력 데이터가 없어 협업 필터링을 적용할 수 없었습니다.
이를 해결하기 위해 내용 기반 가중치 매칭 모델을 직접 설계했습니다.

항목가중치알고리즘관심 직무 유사도40%직무 일치 100점 / 개발 직군 내 50점 / 비개발 0점기술 스택 유사도40%자카드 유사도 (교집합 / 합집합 × 100)목표 기업 유사도20%완전 일치 100점


가중치 비율은 팀원들과 반복 실험을 통해 도출했으며, 교수님 피드백을 반영해 항목별 실험 결과를 문서화했습니다.
최종 테스트 데이터 기준 94.4% 매칭 정확도 달성




📁 파일 구조

├── recommend_model.py   # 커피챗 추천 알고리즘 (자카드 유사도 기반 가중치 매칭)
├── master_crawler.py    # 원티드 채용 공고 크롤링 파이프라인
├── upload_jobs.py       # 크롤링 데이터 → DB 적재 파이프라인
└── models.py            # SQLAlchemy DB 스키마 설계


⚙️ 주요 기능 설명

1. 추천 알고리즘 (recommend_model.py)

자카드 유사도(Jaccard Similarity)를 핵심으로 하는 내용 기반 필터링 모델입니다.

python# 기술 스택 자카드 유사도 계산
def calculate_ability_score(user_a_stacks, user_b_stacks):
    set_a = set(user_a_stacks)
    set_b = set(user_b_stacks)
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    similarity = (intersection / union) * 100
    return round(similarity, 1)


calculate_job_score() : 직무 유사도 계산 (가중치 40%)
calculate_ability_score() : 기술 스택 자카드 유사도 계산 (가중치 40%)
calculate_goal_score() : 목표 기업 유사도 계산 (가중치 20%)
get_coffeechat_match_result() : 3가지 점수를 종합해 최종 매칭률 반환



2. 원티드 크롤링 파이프라인 (master_crawler.py)

원티드 공개 API를 활용해 채용 공고 데이터를 수집합니다.


get_job_list() : 채용 공고 목록 수집 (회사명, 지역, 구/시)
get_job_details() : 공고별 상세 API 호출 → 기술 스택 텍스트 파싱, 마감일, 회사 로고 추출
run_crawling() : 전체 크롤링 실행 후 final_jobs_data.json으로 저장


크롤링 흐름:
원티드 API → 공고 목록 수집 → 상세 정보 파싱 → JSON 저장


3. DB 적재 파이프라인 (upload_jobs.py)

크롤링된 JSON 데이터를 DB에 적재합니다.


공고 제목 텍스트를 분석해 직무(BACKEND / FRONTEND / DATA 등)와 연차를 자동 분류
Member → Graduate → TechStack 순서로 관계형 DB에 적재


적재 흐름:
final_jobs_data.json → Member 생성 → Graduate 연결 → TechStack 등록 → DB Commit


4. DB 스키마 (models.py)

SQLAlchemy ORM 기반으로 설계한 테이블 구조입니다.

테이블역할Member공통 회원 정보 (이름, 학번, 학과, 인증 여부, 역할)Graduate졸업생 상세 정보 (직무, 회사, 연차, 명함 이미지)Student재학생 정보 (학년)TechStack기술 스택 목록 (JAVA, PYTHON 등)Roadmap로드맵 콘텐츠


🛠 기술 스택

분류기술언어Python웹 프레임워크FastAPIDB ORMSQLAlchemy데이터 수집requests (원티드 API)파싱re (정규표현식)연동REST API (Spring Boot 메인 서버와 연동)


📊 성과


테스트 데이터 기준 매칭 정확도 94.4% 달성
교수님 피드백 반영 → 가중치 항목별 실험 결과 문서화
캡스톤 디자인 최종 A+ 학점 취득
