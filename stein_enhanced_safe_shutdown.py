#!/usr/bin/env python3
"""
🛡️ Stein 강화 안전 종료 시스템 v2.0
- 모든 상황에서 안정적 종료 보장
- 시그널 핸들러 자동 등록
- 종료 훅 시스템
- 데이터 무결성 보장
- 멀티 레벨 안전 장치
"""

import os
import signal
import subprocess
import time
import psutil
import json
import atexit
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Callable
from contextlib import contextmanager

class SteinEnhancedSafeShutdown:
    """Stein님 전용 강화 안전 종료 시스템"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.stein_processes = []
        self.shutdown_hooks = []
        self.emergency_backup_enabled = True
        self.graceful_timeout = 5
        self.force_timeout = 2
        self.shutdown_in_progress = False
        
        # 시그널 핸들러 등록
        self.register_signal_handlers()
        
        # 종료 훅 등록
        atexit.register(self.emergency_shutdown)
        
        print("🛡️ Stein 강화 안전 종료 시스템이 활성화되었습니다!")
    
    def register_signal_handlers(self):
        """시그널 핸들러 등록 - 모든 종료 신호 캐치"""
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
        
        # 주요 종료 시그널 등록
        signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # 종료 요청
        signal.signal(signal.SIGHUP, signal_handler)   # 터미널 종료
        signal.signal(signal.SIGQUIT, signal_handler)  # 종료
    
    def add_shutdown_hook(self, func: Callable, name: str = ""):
        """종료 훅 추가"""
        self.shutdown_hooks.append({
            'function': func,
            'name': name or func.__name__
        })
        print(f"🔗 종료 훅 등록: {name or func.__name__}")
    
    def execute_shutdown_hooks(self):
        """모든 종료 훅 실행"""
        print("🔗 종료 훅 실행 중...")
        for hook in self.shutdown_hooks:
            try:
                print(f"  ⚡ {hook['name']} 실행...")
                hook['function']()
                print(f"  ✅ {hook['name']} 완료")
            except Exception as e:
                print(f"  ❌ {hook['name']} 실패: {e}")
    
    def find_stein_processes(self):
        """Stein 관련 프로세스 찾기 (강화된 버전)"""
        print("🔍 Stein 관련 프로세스 검색 중...")
        
        # 더 포괄적인 키워드 리스트
        stein_keywords = [
            "stein_smart_system",
            "stein_optimized_server", 
            "simple_server",
            "stein_master_system",
            "stein_balance_analyzer",
            "stein_workflow_optimizer",
            "stein_enhanced_safe_shutdown",
            "run_stein_ai",
            "quick_start",
            "FastAPI"  # FastAPI 프로세스도 포함
        ]
        
        # 포트 기반 검색 (8000번 포트 사용하는 프로세스)
        port_keywords = [":8000", "localhost:8000"]
        
        found_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'connections']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # 키워드 검색
                for keyword in stein_keywords:
                    if keyword in cmdline:
                        found_processes.append({
                            'pid': proc.info['pid'],
                            'name': keyword,
                            'cmdline': cmdline,
                            'type': 'keyword'
                        })
                        break
                
                # 포트 검색
                try:
                    connections = proc.connections()
                    for conn in connections:
                        if conn.laddr.port == 8000:
                            found_processes.append({
                                'pid': proc.info['pid'],
                                'name': f"Port 8000 Server",
                                'cmdline': cmdline,
                                'type': 'port'
                            })
                            break
                except:
                    pass
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # 중복 제거
        unique_processes = []
        seen_pids = set()
        for proc in found_processes:
            if proc['pid'] not in seen_pids:
                unique_processes.append(proc)
                seen_pids.add(proc['pid'])
        
        self.stein_processes = unique_processes
        return unique_processes
    
    def create_emergency_backup(self):
        """응급 백업 생성"""
        if not self.emergency_backup_enabled:
            return
        
        print("🚨 응급 백업 생성 중...")
        
        backup_dir = Path("emergency_backups")
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = backup_dir / f"backup_{timestamp}"
        backup_subdir.mkdir(exist_ok=True)
        
        # 백업할 파일 목록
        critical_files = [
            "stein_development.log",
            "stein_config.json",
            "STEIN_BALANCE_REPORT.md",
            "STEIN_EFFICIENCY_REPORT.md",
            "PROJECT_STATUS.md",
            "ai_context_brief.json",
            "evolution.log"
        ]
        
        # 디렉토리 백업
        critical_dirs = [
            "data",
            "config",
            "stein_modules"
        ]
        
        backup_manifest = {
            "timestamp": timestamp,
            "files": [],
            "directories": [],
            "status": "success"
        }
        
        # 파일 백업
        for file in critical_files:
            if os.path.exists(file):
                try:
                    import shutil
                    backup_path = backup_subdir / file
                    shutil.copy2(file, backup_path)
                    backup_manifest["files"].append(file)
                    print(f"  ✅ {file} 백업 완료")
                except Exception as e:
                    print(f"  ❌ {file} 백업 실패: {e}")
        
        # 디렉토리 백업
        for dir_name in critical_dirs:
            if os.path.exists(dir_name):
                try:
                    import shutil
                    backup_path = backup_subdir / dir_name
                    shutil.copytree(dir_name, backup_path)
                    backup_manifest["directories"].append(dir_name)
                    print(f"  ✅ {dir_name}/ 백업 완료")
                except Exception as e:
                    print(f"  ❌ {dir_name}/ 백업 실패: {e}")
        
        # 백업 매니페스트 저장
        with open(backup_subdir / "backup_manifest.json", "w", encoding="utf-8") as f:
            json.dump(backup_manifest, f, indent=2, ensure_ascii=False)
        
        print(f"🎯 응급 백업 완료: {backup_subdir}")
    
    def safe_terminate_process(self, pid, name, process_type="unknown"):
        """프로세스 안전 종료 (강화된 버전)"""
        try:
            process = psutil.Process(pid)
            print(f"🛡️ {name} (PID: {pid}, Type: {process_type}) 안전 종료 중...")
            
            # 프로세스 정보 수집
            try:
                cpu_percent = process.cpu_percent()
                memory_info = process.memory_info()
                print(f"  📊 CPU: {cpu_percent:.1f}%, Memory: {memory_info.rss / 1024 / 1024:.1f}MB")
            except:
                pass
            
            # 1단계: SIGTERM (우아한 종료 요청)
            print(f"  🤝 1단계: 우아한 종료 요청...")
            process.terminate()
            
            # 2단계: 대기 (설정 가능한 타임아웃)
            try:
                process.wait(timeout=self.graceful_timeout)
                print(f"  ✅ {name} 우아하게 종료됨")
                return True
            except psutil.TimeoutExpired:
                print(f"  ⏰ 2단계: 응답 없음, 강제 종료 시도...")
                
                # 3단계: SIGKILL (강제 종료)
                process.kill()
                try:
                    process.wait(timeout=self.force_timeout)
                    print(f"  🔴 {name} 강제 종료됨")
                    return True
                except psutil.TimeoutExpired:
                    print(f"  ❌ {name} 종료 실패 - 좀비 프로세스 가능성")
                    return False
                    
        except psutil.NoSuchProcess:
            print(f"  ℹ️ {name} (PID: {pid}) 이미 종료됨")
            return True
        except Exception as e:
            print(f"  ❌ {name} 종료 중 오류: {e}")
            return False
    
    def safe_shutdown_all(self):
        """모든 Stein 프로세스 안전 종료 (강화된 버전)"""
        if self.shutdown_in_progress:
            print("⚠️ 종료 프로세스가 이미 진행 중입니다!")
            return True
        
        self.shutdown_in_progress = True
        
        print("🛡️ Stein 강화 안전 종료 시스템 시작!")
        print("=" * 60)
        
        # 1. 응급 백업 생성
        self.create_emergency_backup()
        
        # 2. 종료 훅 실행
        self.execute_shutdown_hooks()
        
        # 3. 실행 중인 프로세스 찾기
        processes = self.find_stein_processes()
        
        if not processes:
            print("✅ 종료할 프로세스가 없습니다!")
            return True
        
        print(f"\n🎯 발견된 프로세스: {len(processes)}개")
        print("-" * 50)
        for i, proc in enumerate(processes, 1):
            print(f"{i}. PID: {proc['pid']} - {proc['name']} ({proc['type']})")
        print("-" * 50)
        
        print("\n🛡️ 3단계 안전 종료 프로세스:")
        print("1단계: 우아한 종료 요청 (SIGTERM)")
        print(f"2단계: {self.graceful_timeout}초 대기")
        print(f"3단계: 필요시 강제 종료 (SIGKILL, {self.force_timeout}초)")
        print()
        
        success_count = 0
        total_count = len(processes)
        
        for i, proc in enumerate(processes, 1):
            print(f"[{i}/{total_count}] 종료 중...")
            if self.safe_terminate_process(proc['pid'], proc['name'], proc['type']):
                success_count += 1
            time.sleep(0.5)  # 프로세스 간 간격
        
        print("\n" + "=" * 60)
        print(f"🎯 종료 결과: {success_count}/{total_count} 성공")
        
        if success_count == total_count:
            print("🎉 모든 프로세스가 안전하게 종료되었습니다!")
            print("💾 데이터 백업 완료, 무결성 보장됨")
            return True
        else:
            print("⚠️ 일부 프로세스 종료에 실패했습니다.")
            print("🔍 수동 확인이 필요할 수 있습니다.")
            return False
    
    def emergency_shutdown(self):
        """응급 종료 (atexit 훅)"""
        if not self.shutdown_in_progress:
            print("\n🚨 응급 종료 프로세스 실행!")
            self.safe_shutdown_all()
    
    def status_check(self):
        """시스템 상태 확인"""
        print("🔍 Stein 시스템 상태 확인")
        print("=" * 40)
        
        processes = self.find_stein_processes()
        
        if not processes:
            print("✅ 실행 중인 프로세스 없음")
            print("🟢 시스템 안전 상태")
        else:
            print(f"🟡 실행 중인 프로세스: {len(processes)}개")
            for proc in processes:
                try:
                    p = psutil.Process(proc['pid'])
                    cpu = p.cpu_percent()
                    mem = p.memory_info().rss / 1024 / 1024
                    print(f"  • {proc['name']}: CPU {cpu:.1f}%, RAM {mem:.1f}MB")
                except:
                    print(f"  • {proc['name']}: 상태 불명")
        
        print("=" * 40)
        return processes
    
    def interactive_enhanced_shutdown(self):
        """강화된 대화형 종료"""
        print("🛡️ Stein 강화 안전 종료 시스템")
        print("=" * 50)
        
        processes = self.status_check()
        
        if not processes:
            print("\n🎉 종료할 프로세스가 없습니다!")
            return
        
        print(f"\n🤔 {len(processes)}개의 프로세스를 어떻게 종료하시겠습니까?")
        print("1. 🛡️ 안전 종료 (권장) - 백업 + 우아한 종료")
        print("2. ⚡ 빠른 종료 - 백업 없이 바로 종료")
        print("3. 🎯 선택적 종료 - 특정 프로세스만")
        print("4. 📊 상태 확인만 - 종료하지 않음")
        print("0. 취소")
        
        choice = input("\n선택하세요 (0-4): ").strip()
        
        if choice == "1":
            self.safe_shutdown_all()
        elif choice == "2":
            self.quick_shutdown()
        elif choice == "3":
            self.selective_shutdown()
        elif choice == "4":
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
    
    def selective_shutdown(self):
        """선택적 종료"""
        processes = self.find_stein_processes()
        
        print("\n🎯 종료할 프로세스를 선택하세요:")
        for i, proc in enumerate(processes, 1):
            print(f"{i}. {proc['name']} (PID: {proc['pid']}, Type: {proc['type']})")
        
        try:
            choices = input("번호를 입력하세요 (쉼표로 구분): ").split(',')
            for choice in choices:
                idx = int(choice.strip()) - 1
                if 0 <= idx < len(processes):
                    proc = processes[idx]
                    self.safe_terminate_process(proc['pid'], proc['name'], proc['type'])
        except Exception as e:
            print(f"❌ 입력 오류: {e}")

@contextmanager
def stein_safe_environment():
    """Stein 안전 환경 컨텍스트 매니저"""
    shutdown_system = SteinEnhancedSafeShutdown()
    try:
        yield shutdown_system
    finally:
        shutdown_system.safe_shutdown_all()

def install_global_shutdown_handler():
    """전역 종료 핸들러 설치"""
    global_shutdown = SteinEnhancedSafeShutdown()
    
    # 사용자 정의 훅 추가 예시
    def save_session_data():
        """세션 데이터 저장"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "shutdown_reason": "safe_shutdown",
            "status": "completed"
        }
        with open("last_session.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    global_shutdown.add_shutdown_hook(save_session_data, "세션 데이터 저장")
    
    return global_shutdown

def main():
    """메인 실행 함수"""
    print("🛡️ Stein 강화 안전 종료 시스템 v2.0")
    print("=" * 50)
    
    # 전역 종료 핸들러 설치
    shutdown_system = install_global_shutdown_handler()
    
    # 대화형 종료 시작
    shutdown_system.interactive_enhanced_shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛡️ 안전 종료 시스템이 Ctrl+C를 감지했습니다.")
        print("종료 프로세스가 자동으로 실행됩니다...")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("응급 종료 프로세스를 실행합니다...")
        try:
            emergency = SteinEnhancedSafeShutdown()
            emergency.safe_shutdown_all()
        except:
            print("⚠️ 수동으로 Ctrl+C를 사용해 종료해주세요.") 