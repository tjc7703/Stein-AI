#!/usr/bin/env python3
"""
🚀 Stein AI 시스템 실행 스크립트
천재 개발자 Stein님을 위한 맞춤형 AI 시스템 시작
"""

import os
import sys
import subprocess
import uvicorn
from pathlib import Path

def check_python_version():
    """Python 버전 확인"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} 감지")
    return True

def check_dependencies():
    """의존성 패키지 확인"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 설치됨")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 누락")
    
    if missing_packages:
        print("\n📦 누락된 패키지 설치:")
        print("pip install", " ".join(missing_packages))
        return False
    
    return True

def create_directories():
    """필요한 디렉토리 생성"""
    directories = [
        "src",
        "src/api",
        "src/core",
        "src/utils",
        "static",
        "docs",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 {directory} 디렉토리 확인")

def create_init_files():
    """__init__.py 파일 생성"""
    init_files = [
        "src/__init__.py",
        "src/api/__init__.py",
        "src/core/__init__.py",
        "src/utils/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"📄 {init_file} 생성")

def main():
    """메인 실행 함수"""
    print("🤖 Stein AI 시스템 시작 중...")
    print("=" * 50)
    
    # 1. Python 버전 확인
    if not check_python_version():
        sys.exit(1)
    
    # 2. 의존성 확인
    if not check_dependencies():
        print("\n💡 의존성 설치 후 다시 실행해주세요:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # 3. 디렉토리 구조 생성
    create_directories()
    create_init_files()
    
    print("\n🚀 Stein AI 서버 시작!")
    print("=" * 50)
    print("🌐 URL: http://localhost:8000")
    print("📖 API 문서: http://localhost:8000/docs")
    print("🏥 시스템 상태: http://localhost:8000/stein/health")
    print("🎯 질문 패턴: http://localhost:8000/stein/question-patterns")
    print("=" * 50)
    
    # 4. 서버 실행
    try:
        # 포트 충돌 방지를 위한 자동 포트 찾기
        port = 8000
        while port <= 8010:
            try:
                uvicorn.run(
                    "src.main:app",
                    host="0.0.0.0",
                    port=port,
                    reload=True,
                    log_level="info"
                )
                break
            except OSError as e:
                if "Address already in use" in str(e):
                    port += 1
                    print(f"⚠️  포트 {port-1} 사용 중. 포트 {port}로 재시도...")
                    continue
                else:
                    raise
    except ImportError as e:
        print(f"❌ 모듈 임포트 오류: {e}")
        print("💡 현재 디렉토리에서 실행하고 있는지 확인해주세요.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Stein AI 시스템 종료")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 