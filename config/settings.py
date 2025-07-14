"""
⚙️ Stein AI - 프로젝트 설정
환경 변수 및 설정 값들
"""

import os
from typing import Optional
from pathlib import Path

# 📁 프로젝트 경로
BASE_DIR = Path(__file__).parent.parent

# 🎯 애플리케이션 설정
APP_NAME = "Stein AI"
VERSION = "1.0.0"
DESCRIPTION = "천재 Stein님을 위한 혁신적인 AI 어시스턴트"

# 🌐 서버 설정
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
RELOAD = os.getenv("RELOAD", "True").lower() == "true"

# 🔐 보안 설정
SECRET_KEY = os.getenv("SECRET_KEY", "stein-ai-super-secret-key-for-development")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# 📊 데이터베이스 설정 (향후 확장용)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stein_ai.db")

# 🤖 AI 모델 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
AI_MODEL_PROVIDER = os.getenv("AI_MODEL_PROVIDER", "openai")  # openai, anthropic

# 📝 로깅 설정
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 🚀 성능 설정
WORKERS = int(os.getenv("WORKERS", 1))
MAX_REQUESTS = int(os.getenv("MAX_REQUESTS", 1000))
TIMEOUT = int(os.getenv("TIMEOUT", 30))

# 📁 파일 업로드 설정
UPLOAD_DIR = BASE_DIR / "uploads"
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
ALLOWED_FILE_TYPES = [".txt", ".pdf", ".docx", ".png", ".jpg", ".jpeg"]

# 🎨 Stein님 개인화 설정
STEIN_PREFERENCES = {
    "language": "korean",
    "response_style": "friendly_professional",
    "code_style": "clean_and_efficient",
    "innovation_level": "maximum",
    "explanation_depth": "detailed"
}

# 🔧 개발 도구 설정
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080"
]

# 📈 모니터링 설정
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "True").lower() == "true"
METRICS_PORT = int(os.getenv("METRICS_PORT", 8001))

def get_database_url() -> str:
    """데이터베이스 URL 반환"""
    return DATABASE_URL

def get_cors_origins() -> list:
    """CORS 허용 도메인 목록 반환"""
    return CORS_ORIGINS if DEBUG else ["https://yourdomain.com"]

def get_log_config() -> dict:
    """로깅 설정 딕셔너리 반환"""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": LOG_LEVEL,
            "handlers": ["default"],
        },
    } 