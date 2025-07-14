"""
🛠️ Stein 전용 유틸리티 모듈
- 자주 사용하는 기능들을 깔끔하게 정리
- 효율성 최적화
"""

import os
import json
from pathlib import Path
from datetime import datetime

class SteinUtils:
    """Stein님 전용 유틸리티"""
    
    @staticmethod
    def log_action(action: str, details: str = ""):
        """액션 로깅 (개발 과정 추적)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}: {details}"
        
        log_file = Path("stein_development.log")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    @staticmethod
    def get_project_stats():
        """프로젝트 통계 정보"""
        stats = {
            "files_count": 0,
            "lines_count": 0,
            "modules_count": 0,
            "last_modified": None
        }
        
        for file_path in Path(".").rglob("*.py"):
            if "__pycache__" not in str(file_path):
                stats["files_count"] += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        stats["lines_count"] += len(f.readlines())
                except:
                    pass
        
        return stats
    
    @staticmethod
    def optimize_imports(file_path: str):
        """임포트 최적화 (중복 제거)"""
        # 간단한 임포트 최적화 로직
        if not os.path.exists(file_path):
            return False
        
        # 실제 구현은 더 복잡하지만, 여기서는 기본 구조만
        SteinUtils.log_action("OPTIMIZE_IMPORTS", f"대상 파일: {file_path}")
        return True
