#!/bin/bash

# 🚀 Stein AI 프로젝트 의존성 설치 스크립트
# 따옴표 처리 및 에러 방지 베스트 프랙티스 적용

echo "🤖 Stein AI 프로젝트 의존성 설치 시작!"
echo "=" * 50

# 🔧 Python 가상환경 활성화 확인
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  가상환경이 활성화되지 않았습니다."
    echo "다음 명령어로 활성화하세요: source stein_env/bin/activate"
    exit 1
fi

echo "✅ 가상환경 활성화됨: $VIRTUAL_ENV"

# 📦 기본 패키지 업그레이드
echo "📦 pip 업그레이드 중..."
pip install --upgrade pip

# 🔐 인증 관련 패키지 설치 (따옴표 처리 적용)
echo "🔐 인증 시스템 패키지 설치 중..."

# ✅ 올바른 방법 - 따옴표로 감싸기
pip install PyJWT==2.8.0
pip install "python-jose[cryptography]==3.3.0"  # 🛡️ 대괄호 보호
pip install "passlib[bcrypt]==1.7.4"           # 🛡️ 대괄호 보호

# 🌐 웹 프레임워크 패키지
echo "🌐 웹 프레임워크 패키지 설치 중..."
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"        # 🛡️ 대괄호 보호
pip install pydantic==2.5.0
pip install python-multipart==0.0.6

# 🗄️ 데이터베이스 패키지 (향후 사용)
echo "🗄️ 데이터베이스 패키지 설치 중..."
pip install sqlalchemy==2.0.23
pip install psycopg2-binary==2.9.9

# 🛡️ 보안 및 유틸리티
echo "🛡️ 보안 패키지 설치 중..."
pip install cryptography==41.0.7
pip install python-decouple==3.8

# 📊 로깅 및 개발 도구
echo "📊 개발 도구 설치 중..."
pip install structlog==23.2.0
pip install black==23.11.0
pip install isort==5.12.0
pip install mypy==1.7.1

# ✅ 설치 완료 확인
echo ""
echo "🎉 모든 패키지 설치 완료!"
echo "📋 설치된 패키지 목록:"
pip list | grep -E "(fastapi|uvicorn|PyJWT|python-jose|passlib)"

# 🚀 서버 실행 안내
echo ""
echo "🚀 서버 실행 명령어:"
echo "python -m uvicorn src.api.main:app --reload"
echo ""
echo "📚 API 문서 주소:"
echo "http://localhost:8000/docs" 