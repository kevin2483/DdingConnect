from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True) 
    nickname = Column(String(255))                       
    password = Column(String(255))                       
    student_number = Column(String(255))                 
    department = Column(String(255))                     
    
    # OCR 성공 시 "VERIFIED"가 들어갈 인증 컬럼
    certificate = Column(String(255), default="NONE", nullable=True) 
    
    is_deleted = Column(Boolean, default=False)          

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    roadmaps = relationship("Roadmap", back_populates="owner")

    #--추가--#
    name = Column(String(255))  # UI에 이선배(이름)를 띄우기 위해 필수!
    github_link = Column(String(255), name="github_link")
    linkedin_link = Column(String(255), name="linkedin_link")
    portfolio = Column(String(255))
    profile_image = Column(String(255), name="profile_image")
    point = Column(Integer)
    role = Column(String(20), default="UNKNOWN")

    #--추가--#
    # 새로 만든 하단 테이블들(기술스택, 선배, 재학생)과의 관계(relationship) 연결고리
    tech_stacks = relationship("TechStack", back_populates="member")
    graduate = relationship("Graduate", back_populates="member", uselist=False)
    student = relationship("Student", back_populates="member", uselist=False)

class Roadmap(Base):
    __tablename__ = "roadmap" 

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False) 
    content = Column(Text)  
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("Member", back_populates="roadmaps")



###-----추가---------
# 1. 기술 스택 테이블 (선배의 역량 비교용)
class TechStack(Base):
    __tablename__ = "tech_stack"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    name = Column(String(50), nullable=False) # JAVA, SPRING 등

    # BaseEntity 규격에 맞춘 시간 컬럼 추가
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    member = relationship("Member", back_populates="tech_stacks")


# 2. 선배(졸업생) 테이블 (매칭 결과 UI에 띄워줄 회사, 직무 등)
class Graduate(Base):
    __tablename__ = "graduate"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    business_card_image = Column(String(255), name="business_card_image")
    job_type = Column(String(50), name="job_type")
    company = Column(String(255))
    career_year = Column(Integer, name="career_year")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    member = relationship("Member", back_populates="graduate")


# 3. 재학생 테이블 (정보 입력 화면에서 학년 데이터 저장용)
class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    grade = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    member = relationship("Member", back_populates="student")