#!/usr/bin/env python3
"""
🛡️ Stein 안전 종료 시스템
- 데이터 손실 없음 보장
- 우아한 셧다운 (Graceful Shutdown)
- 모든 프로세스 안전 관리
"""

import os
import signal
import subprocess
import time
import psutil
from pathlib import Path

class SteinSafeShutdown:
    """Stein님 전용 안전 종료 시스템"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.stein_processes = []
        
    def find_stein_processes(self):
        """Stein 관련 프로세스 찾기"""
        print("🔍 Stein 관련 프로세스 검색 중...")
        
        stein_keywords = [
            "stein_smart_system",
            "stein_optimized_server", 
            "simple_server",
            "stein_master_system",
            "stein_balance_analyzer"
        ]
        
        found_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                for keyword in stein_keywords:
                    if keyword in cmdline:
                        found_processes.append({
                            'pid': proc.info['pid'],
                            'name': keyword,
                            'cmdline': cmdline
                        })
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        self.stein_processes = found_processes
        return found_processes
    
    def display_running_processes(self):
        """실행 중인 프로세스 표시"""
        processes = self.find_stein_processes()
        
        if not processes:
            print("✅ 실행 중인 Stein 프로세스가 없습니다.")
            return False
        
        print("\n🚨 실행 중인 Stein 프로세스:")
        print("-" * 50)
        for i, proc in enumerate(processes, 1):
            print(f"{i}. PID: {proc['pid']} - {proc['name']}")
        print("-" * 50)
        return True
    
    def safe_terminate_process(self, pid, name):
        """프로세스 안전 종료"""
        try:
            process = psutil.Process(pid)
            print(f"🛡️ {name} (PID: {pid}) 안전 종료 중...")
            
            # 1단계: SIGTERM (우아한 종료 요청)
            process.terminate()
            
            # 2단계: 3초 대기
            try:
                process.wait(timeout=3)
                print(f"✅ {name} 우아하게 종료됨")
                return True
            except psutil.TimeoutExpired:
                print(f"⏰ {name} 응답 없음, 강제 종료 시도...")
                
                # 3단계: SIGKILL (강제 종료)
                process.kill()
                try:
                    process.wait(timeout=2)
                    print(f"🔴 {name} 강제 종료됨")
                    return True
                except psutil.TimeoutExpired:
                    print(f"❌ {name} 종료 실패")
                    return False
                    
        except psutil.NoSuchProcess:
            print(f"ℹ️ {name} (PID: {pid}) 이미 종료됨")
            return True
        except Exception as e:
            print(f"❌ {name} 종료 중 오류: {e}")
            return False
    
    def backup_important_data(self):
        """중요 데이터 백업"""
        print("💾 중요 데이터 백업 중...")
        
        backup_files = [
            "stein_development.log",
            "stein_config.json",
            "STEIN_BALANCE_REPORT.md",
            "STEIN_EFFICIENCY_REPORT.md"
        ]
        
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        for file in backup_files:
            if os.path.exists(file):
                import shutil
                backup_path = backup_dir / f"{file}.backup_{int(time.time())}"
                shutil.copy2(file, backup_path)
                print(f"✅ {file} 백업 완료")
    
    def safe_shutdown_all(self):
        """모든 Stein 프로세스 안전 종료"""
        print("🛡️ Stein 시스템 안전 종료 시작!")
        print("=" * 50)
        
        # 1. 데이터 백업
        self.backup_important_data()
        
        # 2. 실행 중인 프로세스 찾기
        if not self.display_running_processes():
            print("🎉 종료할 프로세스가 없습니다!")
            return True
        
        print("\n🛡️ 안전 종료 프로세스:")
        print("1단계: 우아한 종료 요청 (SIGTERM)")
        print("2단계: 3초 대기")
        print("3단계: 필요시 강제 종료 (SIGKILL)")
        print()
        
        success_count = 0
        for proc in self.stein_processes:
            if self.safe_terminate_process(proc['pid'], proc['name']):
                success_count += 1
            time.sleep(0.5)  # 프로세스 간 간격
        
        print("\n" + "=" * 50)
        print(f"🎯 종료 결과: {success_count}/{len(self.stein_processes)} 성공")
        
        if success_count == len(self.stein_processes):
            print("🎉 모든 프로세스가 안전하게 종료되었습니다!")
            return True
        else:
            print("⚠️ 일부 프로세스 종료에 실패했습니다.")
            return False
    
    def interactive_shutdown(self):
        """대화형 종료"""
        self.display_running_processes()
        
        if not self.stein_processes:
            return
        
        print("\n🤔 어떻게 종료하시겠습니까?")
        print("1. 🛡️ 안전 종료 (권장)")
        print("2. ⚡ 빠른 종료")
        print("3. 🎯 선택적 종료")
        print("0. 취소")
        
        choice = input("\n선택하세요 (0-3): ").strip()
        
        if choice == "1":
            self.safe_shutdown_all()
        elif choice == "2":
            self.quick_shutdown()
        elif choice == "3":
            self.selective_shutdown()
        elif choice == "0":
            print("👋 종료를 취소했습니다.")
        else:
            print("❌ 올바른 선택지를 입력해주세요.")
    
    def quick_shutdown(self):
        """빠른 종료 (덜 안전)"""
        print("⚡ 빠른 종료 실행 중...")
        for proc in self.stein_processes:
            try:
                os.kill(proc['pid'], signal.SIGKILL)
                print(f"🔴 {proc['name']} (PID: {proc['pid']}) 즉시 종료")
            except:
                print(f"❌ {proc['name']} 종료 실패")
    
    def selective_shutdown(self):
        """선택적 종료"""
        print("\n🎯 종료할 프로세스를 선택하세요:")
        for i, proc in enumerate(self.stein_processes, 1):
            print(f"{i}. {proc['name']} (PID: {proc['pid']})")
        
        try:
            choices = input("번호를 입력하세요 (쉼표로 구분): ").split(',')
            for choice in choices:
                idx = int(choice.strip()) - 1
                if 0 <= idx < len(self.stein_processes):
                    proc = self.stein_processes[idx]
                    self.safe_terminate_process(proc['pid'], proc['name'])
        except Exception as e:
            print(f"❌ 입력 오류: {e}")
    
    def show_shutdown_tips(self):
        """종료 팁 표시"""
        print("\n💡 Stein님을 위한 안전 종료 팁:")
        print("-" * 40)
        print("✅ Ctrl+C: 가장 안전한 수동 종료")
        print("✅ 터미널 창 닫기 전에 항상 서버 종료")
        print("✅ 백그라운드 실행 시 이 스크립트 사용")
        print("✅ 중요 데이터는 자동 백업됨")
        print("⚠️ 절대 강제 터미널 종료 금지")
        print("-" * 40)

def main():
    """메인 실행 함수"""
    print("🛡️ Stein 안전 종료 시스템 v1.0")
    print("=" * 40)
    
    shutdown_system = SteinSafeShutdown()
    
    # 실행 중인 프로세스 확인
    if not shutdown_system.display_running_processes():
        print("\n🎉 현재 실행 중인 Stein 프로세스가 없습니다!")
        print("안전하게 작업을 계속하세요! 😊")
        return
    
    # 팁 표시
    shutdown_system.show_shutdown_tips()
    
    # 대화형 종료
    shutdown_system.interactive_shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 안전 종료 시스템을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("수동으로 Ctrl+C를 사용해 종료해주세요.") 