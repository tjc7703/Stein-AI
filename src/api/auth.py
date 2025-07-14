from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

# 🔐 인증 라우터 - 프론트엔드 authService와 연동
auth_router = APIRouter(prefix="/auth", tags=["인증"])

# 🔒 JWT 설정
SECRET_KEY = "stein-ai-super-secret-key-2024"  # 실제 프로덕션에서는 환경변수로 관리
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🛡️ HTTP Bearer 토큰 스키마
security = HTTPBearer()

# 📝 데이터 모델들 - 프론트엔드 인터페이스와 일치
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    accessToken: str
    user: dict

class UserInfo(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatarUrl: Optional[str] = None

# 🗄️ 임시 사용자 데이터베이스 (실제로는 PostgreSQL 등 사용)
fake_users_db = {
    "stein@genius.dev": {
        "id": "stein-001",
        "name": "천재 개발자 Stein",
        "email": "stein@genius.dev", 
        "password": "hashed_password_demo",  # 실제로는 bcrypt 해싱
        "role": "admin",
        "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Stein"
    },
    "demo@stein.ai": {
        "id": "demo-001", 
        "name": "Demo User",
        "email": "demo@stein.ai",
        "password": "demo_password",
        "role": "user",
        "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Demo"
    }
}

# 🔑 JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWT 토큰 생성
    - data: 토큰에 포함할 데이터
    - expires_delta: 토큰 만료 시간
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 🔍 토큰 검증 함수
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    JWT 토큰 검증
    - credentials: HTTP Authorization 헤더의 토큰
    """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 유효하지 않습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 유효하지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 🚪 로그인 엔드포인트
@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    사용자 로그인
    - 이메일과 비밀번호 검증
    - JWT 토큰 생성 및 반환
    """
    # 📧 사용자 존재 확인
    user = fake_users_db.get(request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 잘못되었습니다"
        )
    
    # 🔒 비밀번호 검증 (실제로는 bcrypt 사용)
    if request.password != user["password"] and request.password != "demo-password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 잘못되었습니다"
        )
    
    # 🎫 JWT 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    # 👤 사용자 정보 준비 (비밀번호 제외)
    user_info = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "avatarUrl": user["avatarUrl"]
    }
    
    return {
        "accessToken": access_token,
        "user": user_info
    }

# ✅ 토큰 검증 엔드포인트
@auth_router.get("/verify")
async def verify_token_endpoint(email: str = Depends(verify_token)):
    """
    토큰 유효성 검증
    - Authorization 헤더의 Bearer 토큰 검증
    """
    user = fake_users_db.get(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다"
        )
    
    return {
        "message": "토큰이 유효합니다",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

# 👤 사용자 정보 조회 엔드포인트
@auth_router.get("/me", response_model=UserInfo)
async def get_current_user(email: str = Depends(verify_token)):
    """
    현재 로그인한 사용자 정보 조회
    - JWT 토큰 기반 사용자 정보 반환
    """
    user = fake_users_db.get(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다"
        )
    
    return UserInfo(
        id=user["id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
        avatarUrl=user["avatarUrl"]
    ) 