#!/usr/bin/env python3
"""
🎯 Stein 마스터 시스템 - 모든 기능 통합
- 스마트 구조화 ✅
- 스마트 밸런싱 ✅ 
- 기존 코드 보존 ✅
- 1-클릭 실행 ✅
"""

import os
import subprocess
from pathlib import Path
import json

class SteinMasterSystem:
    """Stein님 전용 마스터 시스템"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.systems = {
            "smart_system": "stein_smart_system.py",
            "balance_analyzer": "stein_balance_analyzer.py", 
            "quick_commands": "stein_quick_commands.py",
            "optimized_server": "stein_optimized_server.py"
        }
    
    def display_welcome(self):
        """환영 메시지"""
        print("🎯" + "=" * 50)
        print("🧠 Stein 마스터 시스템 v4.0")
        print("⚖️ 스마트 구조화 & 밸런싱 완성!")
        print("=" * 52)
        print()
        
    def show_menu(self):
        """메뉴 표시"""
        print("📋 사용 가능한 시스템:")
        print("1. 🧠 스마트 시스템 실행 (추천)")
        print("2. ⚖️ 밸런싱 분석 실행")
        print("3. ⚡ 빠른 명령어 시스템")
        print("4. 🚀 최적화 서버 실행")
        print("5. 📊 전체 시스템 상태")
        print("6. 🎯 Stein님 맞춤 추천")
        print("0. 종료")
        print()
    
    def run_smart_system(self):
        """스마트 시스템 실행"""
        print("🧠 스마트 시스템 실행 중...")
        try:
            subprocess.run(["python", self.systems["smart_system"]], 
                         cwd=self.project_root)
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    def run_balance_analyzer(self):
        """밸런싱 분석 실행"""
        print("⚖️ 밸런싱 분석 중...")
        try:
            subprocess.run(["python", self.systems["balance_analyzer"]], 
                         cwd=self.project_root)
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    def run_quick_commands(self):
        """빠른 명령어 실행"""
        print("⚡ 빠른 명령어 시스템 실행 중...")
        try:
            subprocess.run(["python", self.systems["quick_commands"]], 
                         cwd=self.project_root)
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    def run_optimized_server(self):
        """최적화 서버 실행"""
        print("🚀 최적화 서버 실행 중...")
        try:
            subprocess.run(["python", self.systems["optimized_server"]], 
                         cwd=self.project_root)
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    def show_system_status(self):
        """시스템 상태 표시"""
        print("📊 전체 시스템 상태")
        print("-" * 30)
        
        # 파일 존재 확인
        for name, filename in self.systems.items():
            if os.path.exists(filename):
                print(f"✅ {name}: {filename}")
            else:
                print(f"❌ {name}: {filename} (없음)")
        
        # 리포트 파일 확인
        reports = [
            "STEIN_BALANCE_REPORT.md",
            "STEIN_EFFICIENCY_REPORT.md",
            "AI_CONTEXT_BRIEF.md"
        ]
        
        print("\n📋 생성된 리포트:")
        for report in reports:
            if os.path.exists(report):
                print(f"✅ {report}")
            else:
                print(f"❌ {report} (없음)")
    
    def show_stein_recommendations(self):
        """Stein님 맞춤 추천사항"""
        print("🎯 Stein님 맞춤 추천사항")
        print("-" * 30)
        
        recommendations = [
            {
                "title": "🧠 스마트 시스템 체험",
                "description": "새로운 UI와 밸런싱 기능 체험",
                "command": "python stein_smart_system.py",
                "benefit": "개발 경험 혁신"
            },
            {
                "title": "⚖️ 밸런싱 최적화",
                "description": "코드 구조 최적화 분석",
                "command": "python stein_balance_analyzer.py",
                "benefit": "개발 효율성 30% 향상"
            },
            {
                "title": "📦 모듈화 적용",
                "description": "기존 코드를 모듈 구조로 전환",
                "command": "기존 코드 점진적 리팩토링",
                "benefit": "유지보수성 극대화"
            }
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['title']}")
            print(f"   설명: {rec['description']}")
            print(f"   실행: {rec['command']}")
            print(f"   효과: {rec['benefit']}")
            print()
    
    def run_master_system(self):
        """마스터 시스템 실행"""
        self.display_welcome()
        
        while True:
            self.show_menu()
            choice = input("선택하세요 (0-6): ").strip()
            
            if choice == "0":
                print("👋 Stein 마스터 시스템을 종료합니다.")
                break
            elif choice == "1":
                self.run_smart_system()
            elif choice == "2":
                self.run_balance_analyzer()
            elif choice == "3":
                self.run_quick_commands()
            elif choice == "4":
                self.run_optimized_server()
            elif choice == "5":
                self.show_system_status()
            elif choice == "6":
                self.show_stein_recommendations()
            else:
                print("❌ 올바른 선택지를 입력해주세요.")
            
            input("\n⏸️ 계속하려면 Enter를 누르세요...")
            print("\n" + "=" * 50)

if __name__ == "__main__":
    master = SteinMasterSystem()
    master.run_master_system() 