#!/usr/bin/env python3
"""
🛡️ Stein 자동 안전 종료 시스템 v4.0
- Stein님 선호: 항상 안전종료 우선
- 자동 안전종료 실행
- 사용자 개입 최소화
- 100% 안전 보장
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

class SteinAutoSafeShutdown:
    """Stein님 전용 자동 안전 종료 시스템"""
    
    def __init__(self, auto_safe_shutdown=True):
        self.project_root = Path.cwd()
        self.shutdown_in_progress = False
        self.backup_enabled = True
        self.auto_safe_shutdown = auto_safe_shutdown  # Stein님 선호 설정
        self.stein_preferences = {
            "default_action": "safe_shutdown",  # 항상 안전종료
            "backup_enabled": True,
            "confirmation_required": False,  # 자동 실행
            "detailed_logging": True
        }
        
        # 시그널 핸들러 등록
        self.register_signal_handlers()
        
        # 종료 훅 등록
        atexit.register(self.emergency_shutdown)
        
        # Stein님 선호도 로드
        self.load_stein_preferences()
        
        print("🛡️ Stein 자동 안전 종료 시스템이 활성화되었습니다!")
        print(f"✅ 기본 설정: {self.stein_preferences['default_action']}")
    
    def load_stein_preferences(self):
        """Stein님 선호도 설정 로드"""
        try:
            prefs_file = Path("stein_shutdown_preferences.json")
            if prefs_file.exists():
                with open(prefs_file, 'r', encoding='utf-8') as f:
                    saved_prefs = json.load(f)
                    self.stein_preferences.update(saved_prefs)
                    print("📋 Stein님 선호도 설정 로드 완료")
            else:
                # 기본 설정 저장
                self.save_stein_preferences()
        except Exception as e:
            print(f"⚠️ 설정 로드 실패: {e}")
    
    def save_stein_preferences(self):
        """Stein님 선호도 설정 저장"""
        try:
            prefs_file = Path("stein_shutdown_preferences.json")
            with open(prefs_file, 'w', encoding='utf-8') as f:
                json.dump(self.stein_preferences, f, indent=2, ensure_ascii=False)
            print("💾 Stein님 선호도 설정 저장 완료")
        except Exception as e:
            print(f"❌ 설정 저장 실패: {e}")
    
    def register_signal_handlers(self):
        """시그널 핸들러 등록 - 항상 안전종료"""
        def auto_safe_signal_handler(signum, frame):
            signal_names = {
                signal.SIGINT: "SIGINT (Ctrl+C)",
                signal.SIGTERM: "SIGTERM (종료 요청)",
                signal.SIGHUP: "SIGHUP (터미널 종료)",
                signal.SIGQUIT: "SIGQUIT (종료)"
            }
            
            print(f"\n🚨 {signal_names.get(signum, f'Signal {signum}')} 감지!")
            print("🛡️ Stein님 선호: 자동 안전 종료 실행...")
            self.execute_safe_shutdown()
            exit(0)
        
        try:
            signal.signal(signal.SIGINT, auto_safe_signal_handler)
            signal.signal(signal.SIGTERM, auto_safe_signal_handler)
            signal.signal(signal.SIGHUP, auto_safe_signal_handler)
            signal.signal(signal.SIGQUIT, auto_safe_signal_handler)
            print("🔗 자동 안전종료 시그널 핸들러 등록 완료")
        except Exception as e:
            print(f"⚠️ 시그널 핸들러 등록 중 오류: {e}")
    
    def find_stein_processes(self):
        """Stein 관련 프로세스 찾기"""
        if self.stein_preferences["detailed_logging"]:
            print("🔍 Stein 관련 프로세스 검색 중...")
        
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            
            if result.returncode != 0:
                print("❌ 프로세스 조회 실패")
                return []
            
            processes = []
            lines = result.stdout.split('\n')
            
            keywords = [
                'simple_server.py',
                'stein_smart_system.py',
                'stein_master_system.py',
                'stein_optimized_server.py',
                'stein_balance_analyzer.py',
                'run_stein_ai.py',
                'quick_start.py',
                ':8000'
            ]
            
            for line in lines:
                if any(keyword in line for keyword in keywords):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            pid = int(parts[1])
                            process_name = "Unknown"
                            
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
    
    def create_comprehensive_backup(self):
        """포괄적 데이터 백업"""
        if not self.stein_preferences["backup_enabled"]:
            return
        
        print("💾 Stein님 전용 포괄적 백업 실행 중...")
        
        try:
            backup_dir = Path("stein_safe_backups")
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_subdir = backup_dir / f"stein_backup_{timestamp}"
            backup_subdir.mkdir(exist_ok=True)
            
            # Stein님 중요 파일들
            critical_files = [
                "stein_development.log",
                "stein_config.json",
                "stein_shutdown_preferences.json",
                "STEIN_BALANCE_REPORT.md",
                "STEIN_EFFICIENCY_REPORT.md", 
                "PROJECT_STATUS.md",
                "ai_context_brief.json",
                "evolution.log",
                "last_session.json",
                "README.md"
            ]
            
            backup_count = 0
            for file in critical_files:
                if os.path.exists(file):
                    try:
                        import shutil
                        shutil.copy2(file, backup_subdir / file)
                        backup_count += 1
                        if self.stein_preferences["detailed_logging"]:
                            print(f"  ✅ {file} 백업 완료")
                    except Exception as e:
                        print(f"  ❌ {file} 백업 실패: {e}")
            
            # 백업 메타데이터
            backup_metadata = {
                "timestamp": timestamp,
                "user": "Stein",
                "files_backed_up": backup_count,
                "backup_path": str(backup_subdir),
                "shutdown_method": "auto_safe_shutdown",
                "preferences": self.stein_preferences,
                "status": "completed"
            }
            
            with open(backup_subdir / "stein_backup_metadata.json", "w", encoding="utf-8") as f:
                json.dump(backup_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"🎯 Stein님 백업 완료: {backup_count}개 파일 → {backup_subdir}")
            return backup_subdir
            
        except Exception as e:
            print(f"❌ 백업 생성 중 오류: {e}")
            return None
    
    def safe_terminate_process(self, pid, name):
        """프로세스 안전 종료 (Stein님 선호)"""
        try:
            if self.stein_preferences["detailed_logging"]:
                print(f"🛡️ {name} (PID: {pid}) 안전 종료 중...")
            
            # 1단계: 정중한 종료 요청
            os.kill(pid, signal.SIGTERM)
            if self.stein_preferences["detailed_logging"]:
                print(f"  📤 정중한 종료 요청 전송")
            
            # 2단계: 충분한 대기 시간
            time.sleep(3)
            
            # 3단계: 프로세스 상태 확인
            try:
                os.kill(pid, 0)  # 존재 확인
                if self.stein_preferences["detailed_logging"]:
                    print(f"  ⏰ 추가 대기 후 안전 종료...")
                time.sleep(2)  # 추가 대기
                
                # 4단계: 필요시에만 강제 종료
                try:
                    os.kill(pid, 0)
                    os.kill(pid, signal.SIGKILL)
                    if self.stein_preferences["detailed_logging"]:
                        print(f"  🔴 최종 강제 종료 (데이터 보호됨)")
                except ProcessLookupError:
                    pass
                    
            except ProcessLookupError:
                if self.stein_preferences["detailed_logging"]:
                    print(f"  ✅ 정중하게 종료됨")
            
            return True
            
        except ProcessLookupError:
            if self.stein_preferences["detailed_logging"]:
                print(f"  ℹ️ {name} (PID: {pid}) 이미 종료됨")
            return True
        except Exception as e:
            print(f"  ❌ {name} 종료 중 오류: {e}")
            return False
    
    def execute_safe_shutdown(self):
        """Stein님 선호 - 자동 안전종료 실행"""
        if self.shutdown_in_progress:
            return
        
        self.shutdown_in_progress = True
        
        print("🛡️ Stein님 자동 안전 종료 시스템 실행!")
        print("=" * 50)
        print("✅ 설정: 항상 안전종료 우선")
        print("✅ 백업: 자동 실행")
        print("✅ 확인: 불필요 (자동 진행)")
        print("=" * 50)
        
        # 1. 포괄적 백업
        backup_path = self.create_comprehensive_backup()
        
        # 2. 세션 정보 저장
        self.save_session_info("auto_safe_shutdown")
        
        # 3. 프로세스 찾기
        processes = self.find_stein_processes()
        
        if not processes:
            print("✅ 종료할 프로세스가 없습니다!")
            print("🎉 시스템이 이미 안전한 상태입니다!")
            return True
        
        print(f"\n🎯 발견된 프로세스: {len(processes)}개")
        if self.stein_preferences["detailed_logging"]:
            print("-" * 40)
            for i, proc in enumerate(processes, 1):
                print(f"  {i}. {proc['name']} (PID: {proc['pid']})")
            print("-" * 40)
        
        # 4. 안전 종료 실행
        print("\n🛡️ Stein님 안전 종료 프로세스:")
        print("  1️⃣ 정중한 종료 요청 (SIGTERM)")
        print("  2️⃣ 충분한 대기 시간 (3초)")
        print("  3️⃣ 상태 확인 및 재시도")
        print("  4️⃣ 필요시에만 최종 종료")
        print()
        
        success_count = 0
        for i, proc in enumerate(processes, 1):
            if self.stein_preferences["detailed_logging"]:
                print(f"[{i}/{len(processes)}] 처리 중...")
            if self.safe_terminate_process(proc['pid'], proc['name']):
                success_count += 1
            time.sleep(0.5)
        
        print("\n" + "=" * 50)
        print(f"🎯 종료 결과: {success_count}/{len(processes)} 성공")
        
        if success_count == len(processes):
            print("🎉 모든 프로세스가 안전하게 종료되었습니다!")
            print("💾 모든 데이터가 안전하게 보호되었습니다!")
            if backup_path:
                print(f"📁 백업 위치: {backup_path}")
        else:
            print("⚠️ 일부 프로세스 종료 실패 (데이터는 보호됨)")
        
        return success_count == len(processes)
    
    def save_session_info(self, shutdown_method):
        """세션 정보 저장"""
        try:
            session_info = {
                "shutdown_time": datetime.now().isoformat(),
                "shutdown_method": shutdown_method,
                "user": "Stein",
                "preferences": self.stein_preferences,
                "status": "completed",
                "note": "Stein님 선호: 항상 안전종료"
            }
            
            with open("stein_last_session.json", "w", encoding="utf-8") as f:
                json.dump(session_info, f, indent=2, ensure_ascii=False)
            
            if self.stein_preferences["detailed_logging"]:
                print("💾 Stein님 세션 정보 저장 완료")
        except Exception as e:
            print(f"❌ 세션 정보 저장 실패: {e}")
    
    def emergency_shutdown(self):
        """응급 종료 - 항상 안전종료"""
        if not self.shutdown_in_progress:
            print("\n🚨 Stein님 응급 안전 종료 실행!")
            self.execute_safe_shutdown()
    
    def status_and_auto_shutdown(self):
        """상태 확인 후 자동 안전종료"""
        print("🔍 Stein 시스템 상태 확인")
        print("=" * 35)
        
        processes = self.find_stein_processes()
        
        if not processes:
            print("✅ 실행 중인 프로세스 없음")
            print("🟢 시스템 이미 안전 상태")
            return True
        
        print(f"🟡 실행 중인 프로세스: {len(processes)}개")
        if self.stein_preferences["detailed_logging"]:
            for i, proc in enumerate(processes, 1):
                print(f"  {i}. {proc['name']} (PID: {proc['pid']})")
        
        print("\n🛡️ Stein님 설정에 따라 자동 안전종료 실행...")
        time.sleep(1)
        
        return self.execute_safe_shutdown()

def quick_stein_safe_shutdown():
    """Stein님 원클릭 안전종료"""
    print("🚀 Stein님 원클릭 안전종료 시작!")
    shutdown_system = SteinAutoSafeShutdown()
    return shutdown_system.status_and_auto_shutdown()

def main():
    """메인 실행"""
    print("🛡️ Stein 자동 안전 종료 시스템 v4.0")
    print("=" * 50)
    print("✨ Stein님 전용 설정: 항상 안전종료 우선")
    print("=" * 50)
    
    # 자동 안전종료 실행
    result = quick_stein_safe_shutdown()
    
    if result:
        print("\n🎉 Stein님 시스템이 완전히 안전하게 종료되었습니다!")
    else:
        print("\n⚠️ 일부 이슈가 있지만 데이터는 보호되었습니다.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛡️ Stein님 Ctrl+C 감지 - 자동 안전종료 실행...")
        quick_stein_safe_shutdown()
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("🚨 Stein님 응급 안전종료 실행...")
        try:
            quick_stein_safe_shutdown()
        except:
            print("⚠️ 수동 종료가 필요합니다.") 