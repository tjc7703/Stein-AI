"""
🚀 Stein GitHub 자동 관리 시스템
Stein님의 깃허브 저장소를 자동으로 관리하는 시스템
"""

import json
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SteinGitHubManager:
    """🚀 Stein GitHub 자동 관리 시스템"""
    
    def __init__(self, config_file: str = "stein_github_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        
        # 깃허브 저장소 정보
        self.repo_url = self.config['github_repository']['url']
        self.repo_owner = self.config['github_repository']['owner']
        self.repo_name = self.config['github_repository']['repository']
        self.default_branch = self.config['development_settings']['default_branch']
        self.local_path = self.config['development_settings']['local_repository_path']
        
        logger.info(f"🚀 Stein GitHub 관리자 초기화 완료: {self.repo_url}")

    def load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"❌ 설정 파일을 찾을 수 없습니다: {self.config_file}")
            return {}

    def save_config(self):
        """설정 파일 저장"""
        self.config['updated_at'] = datetime.now().isoformat()
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 설정 파일 저장 완료: {self.config_file}")

    def run_git_command(self, command: List[str]) -> Dict[str, Any]:
        """Git 명령어 실행"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=self.local_path
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            logger.error(f"❌ Git 명령어 실행 실패: {e}")
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }

    def check_git_status(self) -> Dict[str, Any]:
        """Git 상태 확인"""
        result = self.run_git_command(['git', 'status', '--porcelain'])
        
        if result['success']:
            files = result['stdout'].strip().split('\n') if result['stdout'] else []
            return {
                'has_changes': len(files) > 0,
                'modified_files': [f for f in files if f.startswith('M')],
                'new_files': [f for f in files if f.startswith('A')],
                'deleted_files': [f for f in files if f.startswith('D')],
                'untracked_files': [f for f in files if f.startswith('??')]
            }
        else:
            return {'has_changes': False, 'error': result['stderr']}

    def auto_commit_and_push(self, commit_message: str = None) -> Dict[str, Any]:
        """자동 커밋 및 푸시"""
        if not commit_message:
            commit_message = f"Stein AI 자동 업데이트 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 1. 상태 확인
        status = self.check_git_status()
        if not status.get('has_changes', False):
            return {'success': True, 'message': '변경사항이 없습니다.'}
        
        # 2. 모든 파일 추가
        add_result = self.run_git_command(['git', 'add', '.'])
        if not add_result['success']:
            return {'success': False, 'error': f'파일 추가 실패: {add_result["stderr"]}'}
        
        # 3. 커밋
        commit_result = self.run_git_command(['git', 'commit', '-m', commit_message])
        if not commit_result['success']:
            return {'success': False, 'error': f'커밋 실패: {commit_result["stderr"]}'}
        
        # 4. 푸시
        push_result = self.run_git_command(['git', 'push', 'origin', self.default_branch])
        if not push_result['success']:
            return {'success': False, 'error': f'푸시 실패: {push_result["stderr"]}'}
        
        logger.info(f"✅ 자동 커밋 및 푸시 완료: {commit_message}")
        return {
            'success': True,
            'message': '자동 커밋 및 푸시가 성공적으로 완료되었습니다.',
            'commit_message': commit_message,
            'files_changed': len(status.get('modified_files', [])) + len(status.get('new_files', []))
        }

    def create_backup(self) -> Dict[str, Any]:
        """백업 생성"""
        backup_dir = f"stein_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # 백업 디렉토리 생성
            os.makedirs(backup_dir, exist_ok=True)
            
            # 중요 파일들 복사
            important_files = [
                'stein_ai_*.py',
                'stein_ai_*.md',
                '*.json',
                'requirements.txt',
                'README.md'
            ]
            
            copied_files = []
            for pattern in important_files:
                import glob
                files = glob.glob(pattern)
                for file in files:
                    if os.path.isfile(file):
                        import shutil
                        shutil.copy2(file, backup_dir)
                        copied_files.append(file)
            
            # 백업 정보 저장
            backup_info = {
                'backup_time': datetime.now().isoformat(),
                'files_copied': copied_files,
                'backup_dir': backup_dir,
                'config': self.config
            }
            
            with open(f"{backup_dir}/backup_info.json", 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 백업 생성 완료: {backup_dir}")
            return {
                'success': True,
                'backup_dir': backup_dir,
                'files_copied': len(copied_files)
            }
            
        except Exception as e:
            logger.error(f"❌ 백업 생성 실패: {e}")
            return {'success': False, 'error': str(e)}

    def get_repository_info(self) -> Dict[str, Any]:
        """저장소 정보 조회"""
        return {
            'repository_url': self.repo_url,
            'owner': self.repo_owner,
            'name': self.repo_name,
            'branch': self.default_branch,
            'local_path': self.local_path,
            'config': self.config
        }

    def update_config(self, updates: Dict[str, Any]):
        """설정 업데이트"""
        for key, value in updates.items():
            if isinstance(value, dict):
                if key not in self.config:
                    self.config[key] = {}
                self.config[key].update(value)
            else:
                self.config[key] = value
        
        self.save_config()
        logger.info(f"⚙️ 설정 업데이트 완료")

    def sync_with_remote(self) -> Dict[str, Any]:
        """원격 저장소와 동기화"""
        # 1. 원격 변경사항 가져오기
        fetch_result = self.run_git_command(['git', 'fetch', 'origin'])
        if not fetch_result['success']:
            return {'success': False, 'error': f'fetch 실패: {fetch_result["stderr"]}'}
        
        # 2. 로컬 변경사항 확인
        status = self.check_git_status()
        
        # 3. 충돌이 없다면 pull
        if not status.get('has_changes', False):
            pull_result = self.run_git_command(['git', 'pull', 'origin', self.default_branch])
            if not pull_result['success']:
                return {'success': False, 'error': f'pull 실패: {pull_result["stderr"]}'}
        
        logger.info("🔄 원격 저장소와 동기화 완료")
        return {'success': True, 'message': '동기화가 완료되었습니다.'}

    def get_commit_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """커밋 히스토리 조회"""
        result = self.run_git_command([
            'git', 'log', 
            f'--max-count={limit}',
            '--pretty=format:%H|%an|%ad|%s',
            '--date=short'
        ])
        
        if not result['success']:
            return []
        
        commits = []
        for line in result['stdout'].strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 4:
                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'date': parts[2],
                        'message': parts[3]
                    })
        
        return commits

# 🚀 실행 예시
if __name__ == "__main__":
    # Stein GitHub 관리자 초기화
    github_manager = SteinGitHubManager()
    
    # 저장소 정보 출력
    repo_info = github_manager.get_repository_info()
    print("🚀 Stein GitHub 관리자 정보:")
    print(f"   저장소: {repo_info['repository_url']}")
    print(f"   소유자: {repo_info['owner']}")
    print(f"   브랜치: {repo_info['branch']}")
    print(f"   로컬 경로: {repo_info['local_path']}")
    
    # Git 상태 확인
    status = github_manager.check_git_status()
    print(f"\n📊 Git 상태:")
    print(f"   변경사항 있음: {status.get('has_changes', False)}")
    if status.get('has_changes'):
        print(f"   수정된 파일: {len(status.get('modified_files', []))}")
        print(f"   새 파일: {len(status.get('new_files', []))}")
    
    # 최근 커밋 히스토리
    commits = github_manager.get_commit_history(5)
    print(f"\n📝 최근 커밋 히스토리:")
    for commit in commits:
        print(f"   {commit['date']} - {commit['message']}")
    
    print("\n✨ Stein GitHub 관리자가 준비되었습니다!")
    print("💡 자동 커밋/푸시: github_manager.auto_commit_and_push()")
    print("💡 백업 생성: github_manager.create_backup()")
    print("💡 동기화: github_manager.sync_with_remote()") 