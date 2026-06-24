# recommend_model.py
# (FastAPI 라우터에 연결하기 전에, 순수하게 알고리즘만 테스트하는 파일입니다)

def calculate_job_score(user_a_job, user_b_job):
    """
    [1] 직무 점수 (jobScore) - 100점 만점
    같은 직무면 100점, 직군이 비슷하면 50점, 아예 다르면 0점
    (예: 백엔드-백엔드 = 100, 백엔드-프론트엔드 = 50, 백엔드-디자인 = 0)
    """
    if user_a_job == user_b_job:
        return 100.0
    
    # 개발 직군끼리는 50점의 기본 시너지 점수 부여
    dev_jobs = {"BACKEND", "FRONTEND", "FULLSTACK", "AI_ML", "DATA", "DEVOPS"}
    if user_a_job in dev_jobs and user_b_job in dev_jobs:
        return 50.0
        
    return 0.0

def calculate_ability_score(user_a_stacks, user_b_stacks):
    """
    [2] 역량 점수 (ability) - 100점 만점
    두 유저가 가진 기술 스택(Tech Stack)의 교집합을 활용한 자카드 유사도(Jaccard Similarity)
    """
    set_a = set(user_a_stacks)
    set_b = set(user_b_stacks)
    
    # 둘 다 스택이 없으면 비교 불가이므로 0점
    if not set_a and not set_b:
        return 0.0
        
    # 교집합(겹치는 스택) / 합집합(전체 스택) * 100
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    similarity = (intersection / union) * 100
    return round(similarity, 1)

def calculate_goal_score(user_a_goal, user_b_goal):
    """
    [3] 목표기업/관심사 점수 (goal) - 100점 만점
    목표가 완전히 같으면 100점, 아니면 0점 (추후 기업 카테고리로 확장 가능)
    """
    if user_a_goal and user_b_goal and user_a_goal == user_b_goal:
        return 100.0
    return 0.0

def get_coffeechat_match_result(user_a, user_b):
    """
    두 유저의 정보를 받아 3가지 점수를 계산하고 최종 결과를 반환합니다.
    """
    job_score = calculate_job_score(user_a["job"], user_b["job"])
    ability_score = calculate_ability_score(user_a["tech_stacks"], user_b["tech_stacks"])
    goal_score = calculate_goal_score(user_a["goal"], user_b["goal"])
    
    # (선택) 3가지 점수의 평균을 내서 최종 매칭률(Total Score)을 뽑을 수도 있습니다.
    total_score = (job_score * 0.4) + (ability_score * 0.4) + (goal_score * 0.2)
    
    return {
        "jobScore": job_score,
        "ability": ability_score,
        "goal": goal_score,
        "totalMatchRate": round(total_score, 1)
    }

# ==========================================
# [알고리즘 테스트]
# ==========================================
if __name__ == "__main__":
    # 유저 A 
    user_a_profile = {
        "user_id": 1,
        "job": "DATA",
        "tech_stacks": ["PYTHON", "SQL", "PYTORCH", "AWS"],
        "goal": "네이버"
    }
    
    # 유저 B 
    user_b_profile = {
        "user_id": 2,
        "job": "BACKEND",
        "tech_stacks": ["JAVA", "SPRING", "PYTHON", "AWS", "DOCKER"],
        "goal": "카카오"
    }
    
    print("--- 커피챗 매칭 알고리즘 결과 ---")
    result = get_coffeechat_match_result(user_a_profile, user_b_profile)
    
    for key, value in result.items():
        print(f"- {key}: {value}점")