"""
🧠 Stein AI - 데이터 모델 정의
Pydantic 기반 요청/응답 모델들
"""

from pydantic import BaseModel, Field
from typing import Optional, Any

class UserRequest(BaseModel):
    """사용자 요청 데이터 모델"""
    name: str = Field(..., description="사용자 이름", min_length=1)
    age: int = Field(..., description="사용자 나이", ge=0, le=150)
    email: Optional[str] = Field(None, description="이메일 주소")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Stein",
                "age": 25,
                "email": "stein@genius.com"
            }
        }

class UserResponse(BaseModel):
    """사용자 응답 데이터 모델"""
    id: int = Field(..., description="사용자 ID")
    name: str = Field(..., description="사용자 이름")
    age: int = Field(..., description="사용자 나이")
    email: Optional[str] = Field(None, description="이메일 주소")
    created_at: str = Field(..., description="생성 시간")
    status: str = Field(default="active", description="사용자 상태")

class ApiResponse(BaseModel):
    """표준 API 응답 모델"""
    success: bool = Field(..., description="성공 여부")
    message: str = Field(..., description="응답 메시지")
    data: Optional[Any] = Field(None, description="응답 데이터")

class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    success: bool = Field(False, description="성공 여부")
    error: str = Field(..., description="에러 메시지")
    code: int = Field(..., description="에러 코드")
    details: Optional[Any] = Field(None, description="상세 정보") 