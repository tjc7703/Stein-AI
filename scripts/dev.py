#!/usr/bin/env python3
"""
🚀 Stein AI - 개발 서버 자동 실행 스크립트
"""

import os
import sys
import subprocess
from pathlib import Path

# 프로젝트 루트 디렉토리로 이동
project_root = Path(__file__).parent.parent
os.chdir(project_root)

def check_dependencies():
    """필요한 패키지가 설치되어 있는지 확인"""
    required_packages = ["fastapi", "uvicorn"]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 설치 확인")
        except ImportError:
            print(f"❌ {package} 미설치 - 설치 중...")
            subprocess.run([sys.executable, "-m", "pip", "install", package])

def run_dev_server():
    """개발 서버 실행"""
    print("🤖 Stein AI 개발 서버 시작!")
    print("🔧 개발 모드: 코드 변경 시 자동 재시작")
    print("🌐 접속: http://localhost:8000")
    print("📚 문서: http://localhost:8000/docs")
    print("⏹️  종료: Ctrl+C")
    print("-" * 50)
    
    # 환경 변수 설정
    os.environ["DEBUG"] = "True"
    os.environ["RELOAD"] = "True"
    
    try:
        # 개발 서버 실행
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n👋 개발 서버를 종료합니다!")

if __name__ == "__main__":
    check_dependencies()
    run_dev_server() 