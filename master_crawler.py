import requests
import json
import time
import re

# 1. 목록 가져오기: 지역(region)과 구/시(district)를 미리 분리해서 가져옵니다.
def get_job_list(limit=50): 
    url = f"https://www.wanted.co.kr/api/v4/jobs?country=kr&locations=all&years=-1&limit={limit}&job_group_id=518" 
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print(f" 원티드에서 최신 개발자 공고 {limit}개 목록을 불러옵니다...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        jobs = response.json().get("data", [])
        result = []
        for job in jobs:
            address = job.get("address", {})
            reg = address.get("location", "")     # 예: "서울"
            dist = address.get("district", "")   # 예: "강남구"
            
            result.append({
                "id": job["id"],
                "company": job.get("company", {}).get("name", ""),
                "region_val": reg,
                "location_val": dist
            })
        return result
    return []

# 2. 상세 정보 추출 (기술스택, 풀주소, 로고 이미지, 마감일)
def get_job_details(job_id):
    url = f"https://www.wanted.co.kr/api/v4/jobs/{job_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            job_data = response.json().get("job", {})
            detail = job_data.get("detail", {})
            address = job_data.get("address", {})
            
            # 기술 스택 추출
            raw_text = detail.get("requirements", "") + " " + detail.get("preferred_points", "")
            english_words = re.findall(r'[A-Za-z]+', raw_text)
            clean_stack = list(set([word.lower() for word in english_words]))
            
            # 상세 정보 추출
            full_location = address.get("full_location", "") if address else ""
            deadline = job_data.get("due_time")
            company_image = job_data.get("logo_img", {}).get("thumb", "")
            
            return {
                "tech_stack": clean_stack,
                "full_location": full_location,
                "company_image": company_image,
                "deadline": deadline if deadline else None
            }
        return None
    except Exception as e:
        print(f"[{job_id}] 상세 정보 추출 에러: {e}")
        return None

# 3. 메인 실행 함수
def run_crawling():
    print("--- 크롤링 시작 ---")
    job_list = get_job_list(limit=20)
    final_data = [] 
    
    for job in job_list:
        details = get_job_details(job["id"])
        if details:
            # DB 컬럼과 1:1 매핑되는 최종 데이터 구조
            final_data.append({
                "companyName": job["company"],
                "region": job["region_val"],          # 예: "서울"
                "location": job["location_val"],      # 예: "강남구"
                "fullLocation": details["full_location"],
                "companyImage": details["company_image"],
                "preferredLanguages": details["tech_stack"],
                "detailUrl": f"https://www.wanted.co.kr/wd/{job['id']}",
                "jobType": "BACKEND",
                "careerType": "JUNIOR",
                "deadline": details["deadline"]
            })
        time.sleep(0.5)
        
    # JSON 파일 저장
    with open("final_jobs_data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print(f"🎉 크롤링 완료! {len(final_data)}개의 데이터가 준비되었습니다.")
    return final_data

if __name__ == "__main__":
    run_crawling()