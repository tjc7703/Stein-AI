#!/usr/bin/env python3
"""
🛡️ Stein 간단 안전 종료 시스템 v3.0
- 모든 상황에서 확실한 종료
- 시그널 핸들러 자동 등록
- 데이터 백업 보장
- 에러 없는 안정적 작동
"""

import os
import signal
import subprocess
import time
import json
import atexit
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class SteinSimpleSafeShutdown:
    """Stein님 전용 간단 안전 종료 시스템"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.shutdown_in_progress = False
        self.backup_enabled = True
        
        # 시그널 핸들러 등록
        self.register_signal_handlers()
        
        # 종료 훅 등록
        atexit.register(self.emergency_shutdown)
        
        print("🛡️ Stein 간단 안전 종료 시스템이 활성화되었습니다!")
    
    def register_signal_handlers(self):
        """시그널 핸들러 등록"""
        def signal_handler(signum, frame):
            signal_names = {
                signal.SIGINT: "SIGINT (Ctrl+C)",
                signal.SIGTERM: "SIGTERM (종료 요청)",
                signal.SIGHUP: "SIGHUP (터미널 종료)",
                signal.SIGQUIT: "SIGQUIT (종료)"
            }
            
            print(f"\n🚨 {signal_names.get(signum, f'Signal {signum}')} 감지!")
            print("🛡️ 안전 종료 프로세스 시작...")
            self.safe_shutdown_all()
            exit(0)
        
        try:
            signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
            signal.signal(signal.SIGTERM, signal_handler)  # 종료 요청
            signal.signal(signal.SIGHUP, signal_handler)   # 터미널 종료
            signal.signal(signal.SIGQUIT, signal_handler)  # 종료
            print("🔗 모든 시그널 핸들러 등록 완료")
        except Exception as e:
            print(f"⚠️ 시그널 핸들러 등록 중 오류: {e}")
    
    def find_stein_processes(self):
        """Stein 관련 프로세스 찾기 (간단한 방법)"""
        print("🔍 Stein 관련 프로세스 검색 중...")
        
        try:
            # ps 명령어로 프로세스 찾기
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            
            if result.returncode != 0:
                print("❌ 프로세스 조회 실패")
                return []
            
            processes = []
            lines = result.stdout.split('\n')
            
            # Stein 관련 키워드
            keywords = [
                'simple_server.py',
                'stein_smart_system.py',
                'stein_master_system.py',
                'stein_optimized_server.py',
                'stein_balance_analyzer.py',
                'run_stein_ai.py',
                'quick_start.py',
                ':8000'  # 포트 8000 사용하는 프로세스
            ]
            
            for line in lines:
                if any(keyword in line for keyword in keywords):
                    # PID 추출
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            pid = int(parts[1])
                            process_name = "Unknown"
                            
                            # 프로세스 이름 추출
                            for keyword in keywords:
                                if keyword in line:
                                    process_name = keyword
                                    break
                            
                            processes.append({
                                'pid': pid,
                                'name': process_name,
                                'cmdline': line
                            })
                        except ValueError:
                            continue
            
            return processes
            
        except Exception as e:
            print(f"❌ 프로세스 검색 중 오류: {e}")
            return []
    
    def create_backup(self):
        """데이터 백업 생성"""
        if not self.backup_enabled:
            return
        
        print("💾 데이터 백업 생성 중...")
        
        try:
            backup_dir = Path("safe_backups")
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_subdir = backup_dir / f"backup_{timestamp}"
            backup_subdir.mkdir(exist_ok=True)
            
            # 백업할 파일 목록
            backup_files = [
                "stein_development.log",
                "stein_config.json",
                "STEIN_BALANCE_REPORT.md",
                "STEIN_EFFICIENCY_REPORT.md",
                "PROJECT_STATUS.md",
                "ai_context_brief.json",
                "evolution.log",
                "last_session.json"
            ]
            
            backup_count = 0
            for file in backup_files:
                if os.path.exists(file):
                    try:
                        import shutil
                        shutil.copy2(file, backup_subdir / file)
                        backup_count += 1
                        print(f"  ✅ {file} 백업 완료")
                    except Exception as e:
                        print(f"  ❌ {file} 백업 실패: {e}")
            
            # 백업 요약 저장
            backup_summary = {
                "timestamp": timestamp,
                "files_backed_up": backup_count,
                "backup_path": str(backup_subdir),
                "status": "completed"
            }
            
            with open(backup_subdir / "backup_summary.json", "w", encoding="utf-8") as f:
                json.dump(backup_summary, f, indent=2, ensure_ascii=False)
            
            print(f"🎯 백업 완료: {backup_count}개 파일 → {backup_subdir}")
            
        except Exception as e:
            print(f"❌ 백업 생성 중 오류: {e}")
    
    def safe_terminate_process(self, pid, name):
        """프로세스 안전 종료"""
        try:
            print(f"🛡️ {name} (PID: {pid}) 안전 종료 중...")
            
            # 1단계: SIGTERM (우아한 종료)
            os.kill(pid, signal.SIGTERM)
            print(f"  📤 SIGTERM 신호 전송됨")
            
            # 2단계: 3초 대기
            time.sleep(3)
            
            # 3단계: 프로세스 확인
            try:
                os.kill(pid, 0)  # 프로세스 존재 확인
                print(f"  ⏰ 응답 없음, 강제 종료...")
                os.kill(pid, signal.SIGKILL)
                time.sleep(1)
                print(f"  🔴 강제 종료 완료")
            except ProcessLookupError:
                print(f"  ✅ 우아하게 종료됨")
            
            return True
            
        except ProcessLookupError:
            print(f"  ℹ️ {name} (PID: {pid}) 이미 종료됨")
            return True
        except Exception as e:
            print(f"  ❌ {name} 종료 중 오류: {e}")
            return False
    
    def safe_shutdown_all(self):
        """모든 Stein 프로세스 안전 종료"""
        if self.shutdown_in_progress:
            print("⚠️ 종료 프로세스가 이미 진행 중입니다!")
            return
        
        self.shutdown_in_progress = True
        
        print("🛡️ Stein 간단 안전 종료 시스템 시작!")
        print("=" * 50)
        
        # 1. 데이터 백업
        self.create_backup()
        
        # 2. 세션 정보 저장
        self.save_session_info()
        
        # 3. 프로세스 찾기
        processes = self.find_stein_processes()
        
        if not processes:
            print("✅ 종료할 프로세스가 없습니다!")
            return True
        
        print(f"\n🎯 발견된 프로세스: {len(processes)}개")
        print("-" * 40)
        for i, proc in enumerate(processes, 1):
            print(f"{i}. PID: {proc['pid']} - {proc['name']}")
        print("-" * 40)
        
        # 4. 순차적 종료
        print("\n🛡️ 안전 종료 실행:")
        success_count = 0
        
        for i, proc in enumerate(processes, 1):
            print(f"\n[{i}/{len(processes)}] 종료 중...")
            if self.safe_terminate_process(proc['pid'], proc['name']):
                success_count += 1
        
        print("\n" + "=" * 50)
        print(f"🎯 종료 결과: {success_count}/{len(processes)} 성공")
        
        if success_count == len(processes):
            print("🎉 모든 프로세스가 안전하게 종료되었습니다!")
        else:
            print("⚠️ 일부 프로세스 종료에 실패했습니다.")
        
        return success_count == len(processes)
    
    def save_session_info(self):
        """세션 정보 저장"""
        try:
            session_info = {
                "shutdown_time": datetime.now().isoformat(),
                "shutdown_method": "safe_shutdown",
                "user": "Stein",
                "status": "completed"
            }
            
            with open("last_session.json", "w", encoding="utf-8") as f:
                json.dump(session_info, f, indent=2, ensure_ascii=False)
            
            print("💾 세션 정보 저장 완료")
        except Exception as e:
            print(f"❌ 세션 정보 저장 실패: {e}")
    
    def emergency_shutdown(self):
        """응급 종료"""
        if not self.shutdown_in_progress:
            print("\n🚨 응급 종료 프로세스 실행!")
            self.safe_shutdown_all()
    
    def status_check(self):
        """현재 상태 확인"""
        print("🔍 Stein 시스템 상태 확인")
        print("=" * 30)
        
        processes = self.find_stein_processes()
        
        if not processes:
            print("✅ 실행 중인 프로세스 없음")
            print("🟢 시스템 안전 상태")
        else:
            print(f"🟡 실행 중인 프로세스: {len(processes)}개")
            for i, proc in enumerate(processes, 1):
                print(f"  {i}. {proc['name']} (PID: {proc['pid']})")
        
        print("=" * 30)
        return processes
    
    def interactive_shutdown(self):
        """대화형 종료"""
        print("🛡️ Stein 간단 안전 종료 시스템")
        print("=" * 40)
        
        processes = self.status_check()
        
        if not processes:
            print("\n🎉 종료할 프로세스가 없습니다!")
            return
        
        print(f"\n🤔 {len(processes)}개의 프로세스를 어떻게 종료하시겠습니까?")
        print("1. 🛡️ 안전 종료 (권장)")
        print("2. ⚡ 빠른 종료")
        print("3. 📊 상태 확인만")
        print("0. 취소")
        
        choice = input("\n선택하세요 (0-3): ").strip()
        
        if choice == "1":
            self.safe_shutdown_all()
        elif choice == "2":
            self.quick_shutdown()
        elif choice == "3":
            self.status_check()
        elif choice == "0":
            print("👋 종료를 취소했습니다.")
        else:
            print("❌ 올바른 선택지를 입력해주세요.")
    
    def quick_shutdown(self):
        """빠른 종료"""
        print("⚡ 빠른 종료 실행 중...")
        processes = self.find_stein_processes()
        
        for proc in processes:
            try:
                os.kill(proc['pid'], signal.SIGKILL)
                print(f"🔴 {proc['name']} (PID: {proc['pid']}) 즉시 종료")
            except:
                print(f"❌ {proc['name']} 종료 실패")

def install_global_safe_shutdown():
    """전역 안전 종료 시스템 설치"""
    return SteinSimpleSafeShutdown()

def main():
    """메인 실행 함수"""
    print("🛡️ Stein 간단 안전 종료 시스템 v3.0")
    print("=" * 50)
    
    shutdown_system = SteinSimpleSafeShutdown()
    shutdown_system.interactive_shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛡️ Ctrl+C 감지 - 안전 종료 실행 중...")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("안전 종료 프로세스를 시도합니다...")
        try:
            emergency = SteinSimpleSafeShutdown()
            emergency.safe_shutdown_all()
        except:
            print("⚠️ 수동 종료가 필요합니다.") 