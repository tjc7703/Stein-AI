"""
🔧 Stein AI - 헬퍼 함수들
공통으로 사용되는 유틸리티 함수들
"""

from datetime import datetime
from typing import Dict, Any, Optional
import re

def get_current_timestamp() -> str:
    """
    현재 시간을 문자열로 반환하는 함수
    
    Returns:
        str: 포맷된 현재 시간 문자열
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_email(email: str) -> bool:
    """
    이메일 유효성 검사 함수
    
    Args:
        email: 검사할 이메일 주소
        
    Returns:
        bool: 유효한 이메일이면 True, 아니면 False
    """
    try:
        # 기본적인 이메일 패턴 검사
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    except Exception:
        return False

def format_response(success: bool, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """
    표준 API 응답 형식으로 포맷하는 함수
    
    Args:
        success: 성공 여부
        message: 응답 메시지
        data: 응답 데이터 (선택사항)
        
    Returns:
        Dict: 포맷된 응답 딕셔너리
    """
    response = {
        "success": success,
        "message": message,
        "timestamp": get_current_timestamp()
    }
    
    if data is not None:
        response["data"] = data
        
    return response

def sanitize_string(text: str) -> str:
    """
    문자열에서 특수문자 제거 및 정리
    
    Args:
        text: 정리할 문자열
        
    Returns:
        str: 정리된 문자열
    """
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    
    # 연속된 공백을 하나로 변경
    text = re.sub(r'\s+', ' ', text)
    
    # 앞뒤 공백 제거
    return text.strip()

def calculate_age_from_birthdate(birthdate: str) -> int:
    """
    생년월일로부터 나이 계산
    
    Args:
        birthdate: 생년월일 (YYYY-MM-DD 형식)
        
    Returns:
        int: 계산된 나이
    """
    try:
        birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth_date.year
        
        # 생일이 지나지 않았으면 1살 빼기
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
            
        return age
    except ValueError:
        return 0

def generate_unique_id() -> str:
    """
    고유 ID 생성 (타임스탬프 기반)
    
    Returns:
        str: 생성된 고유 ID
    """
    return f"stein_{int(datetime.now().timestamp() * 1000)}"

def format_file_size(size_bytes: int) -> str:
    """
    바이트 크기를 읽기 쉬운 형태로 변환
    
    Args:
        size_bytes: 바이트 크기
        
    Returns:
        str: 포맷된 파일 크기 (예: "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}" 