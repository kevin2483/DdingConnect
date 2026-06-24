import json
import random
from database import SessionLocal
from models import Member, Graduate, TechStack

def parse_career_year(position_str):
    """공고 제목 문자열을 분석하여 연차(숫자)로 매핑"""
    pos = position_str.lower()
    if "신입" in pos or "인턴" in pos: return 0
    elif "2년" in pos: return 2
    elif "3년" in pos: return 3
    elif "5년" in pos: return 5
    return random.randint(1, 5) # 기본 1~5년차 랜덤 부여

def parse_job_type(position_str):
    """공고 제목 문자열을 분석하여 백엔드 JobType ENUM 규격으로 매핑"""
    pos = position_str.lower()
    if "백엔드" in pos or "backend" in pos: return "BACKEND"
    elif "프론트" in pos or "frontend" in pos: return "FRONTEND"
    elif "풀스택" in pos or "fullstack" in pos: return "FULLSTACK"
    elif "데이터" in pos or "data" in pos or "분석" in pos: return "DATA"
    elif "인공지능" in pos or "ai" in pos or "머신러닝" in pos or "ml" in pos: return "AI_ML"
    elif "인프라" in pos or "devops" in pos: return "DEVOPS"
    return "ETC"

def run_db_migration():
    db = SessionLocal()
    
    try:
        # 최종 정제된 json 파일 로드
        with open("final_jobs_data.json", "r", encoding="utf-8") as f:
            jobs_list = json.load(f)
            
        inserted_count = 0

        for idx, item in enumerate(jobs_list):
            position_text = item.get("position", "")
            
            # 1. Member(선배 공통 정보) 생성
            member_entry = Member(
                email=f"dummy_senior_{idx}@mju.ac.kr",
                name=f"이선배{idx}", # UI에 띄워줄 가짜 선배 이름
                nickname=f"선배님{idx}",
                password="dummy_password",
                department="컴퓨터공학과",
                role="GRADUATE"
            )
            db.add(member_entry)
            db.flush() # DB에 임시 저장하여 member_entry.id 값을 즉시 받아옴
            
            # 2. Graduate(졸업생 상세 정보) 생성
            graduate_entry = Graduate(
                member_id=member_entry.id, # 방금 만든 Member의 ID 연결
                job_type=parse_job_type(position_text),
                company=item.get("company", "회사 미상"),
                career_year=parse_career_year(position_text)
            )
            db.add(graduate_entry)

            # 3. TechStack(기술 스택) 생성
            for tech in item.get("tech_stack", []):
                tech_entry = TechStack(
                    member_id=member_entry.id, # 방금 만든 Member의 ID 연결
                    name=tech.upper()
                )
                db.add(tech_entry)

            inserted_count += 1

        db.commit()
        print(f"🎉 총 {inserted_count}명의 크롤링 데이터가 '가짜 선배'로 완벽하게 둔갑하여 DB에 적재되었습니다!")

    except Exception as e:
        db.rollback() 
        print(f"데이터베이스 저장 중 치명적 오류 발생: {e}")
    finally:
        db.close() 

if __name__ == "__main__":
    run_db_migration()