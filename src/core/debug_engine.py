import traceback
import sys
import time
import psutil
import logging
import json
import re
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import ast
import inspect
from contextlib import contextmanager
import threading
import queue

class ErrorType(Enum):
    """오류 유형"""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    MEMORY = "memory"
    NETWORK = "network"
    DATABASE = "database"
    API = "api"

class DebugLevel(Enum):
    """디버그 레벨"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"

@dataclass
class DebugInfo:
    """디버그 정보"""
    timestamp: datetime
    error_type: ErrorType
    level: DebugLevel
    message: str
    file_path: str
    line_number: int
    function_name: str
    stack_trace: str
    variables: Dict[str, Any]
    suggestions: List[str]
    auto_fixable: bool

@dataclass
class PerformanceMetrics:
    """성능 메트릭"""
    execution_time: float
    memory_usage: float
    cpu_usage: float
    io_operations: int
    network_calls: int
    database_queries: int

class DebugEngine:
    """🔧 고급 디버깅 및 오류 해결 엔진"""
    
    def __init__(self):
        self.debug_history = []
        self.performance_history = []
        self.error_patterns = self._load_error_patterns()
        self.auto_fixes = self._load_auto_fixes()
        self.monitoring_enabled = False
        self.log_queue = queue.Queue()
        self.setup_logging()
        
    def setup_logging(self):
        """로깅 설정"""
        self.logger = logging.getLogger('stein_debug')
        self.logger.setLevel(logging.DEBUG)
        
        # 핸들러 설정
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    @contextmanager
    def debug_context(self, function_name: str = None):
        """디버그 컨텍스트 관리자"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            yield
        except Exception as e:
            # 오류 발생 시 자동 디버깅
            error_info = self.analyze_error(e, function_name)
            self.debug_history.append(error_info)
            
            # 자동 수정 시도
            if error_info.auto_fixable:
                self.apply_auto_fix(error_info)
            
            raise
        finally:
            # 성능 메트릭 수집
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            metrics = PerformanceMetrics(
                execution_time=end_time - start_time,
                memory_usage=end_memory - start_memory,
                cpu_usage=psutil.cpu_percent(),
                io_operations=0,  # 실제 구현에서는 psutil로 측정
                network_calls=0,
                database_queries=0
            )
            
            self.performance_history.append({
                'timestamp': datetime.now(),
                'function': function_name,
                'metrics': metrics
            })
    
    def analyze_error(self, error: Exception, function_name: str = None) -> DebugInfo:
        """🔍 오류 심층 분석"""
        
        # 스택 트레이스 분석
        tb = traceback.extract_tb(error.__traceback__)
        stack_trace = traceback.format_exc()
        
        # 오류 위치 정보
        if tb:
            last_frame = tb[-1]
            file_path = last_frame.filename
            line_number = last_frame.lineno
            function_name = function_name or last_frame.name
        else:
            file_path = "unknown"
            line_number = 0
            function_name = function_name or "unknown"
        
        # 오류 유형 분류
        error_type = self._classify_error_type(error)
        
        # 로컬 변수 수집
        variables = self._collect_variables(error)
        
        # 오류 메시지 분석
        message = str(error)
        
        # 개선 제안 생성
        suggestions = self._generate_error_suggestions(error, error_type, message)
        
        # 자동 수정 가능 여부 판단
        auto_fixable = self._is_auto_fixable(error_type, message)
        
        return DebugInfo(
            timestamp=datetime.now(),
            error_type=error_type,
            level=DebugLevel.ERROR,
            message=message,
            file_path=file_path,
            line_number=line_number,
            function_name=function_name,
            stack_trace=stack_trace,
            variables=variables,
            suggestions=suggestions,
            auto_fixable=auto_fixable
        )
    
    def _classify_error_type(self, error: Exception) -> ErrorType:
        """오류 유형 분류"""
        
        error_mappings = {
            SyntaxError: ErrorType.SYNTAX,
            NameError: ErrorType.RUNTIME,
            TypeError: ErrorType.RUNTIME,
            ValueError: ErrorType.RUNTIME,
            AttributeError: ErrorType.RUNTIME,
            IndexError: ErrorType.RUNTIME,
            KeyError: ErrorType.RUNTIME,
            ImportError: ErrorType.RUNTIME,
            ModuleNotFoundError: ErrorType.RUNTIME,
            MemoryError: ErrorType.MEMORY,
            RecursionError: ErrorType.LOGIC,
            ConnectionError: ErrorType.NETWORK,
            TimeoutError: ErrorType.NETWORK,
        }
        
        return error_mappings.get(type(error), ErrorType.RUNTIME)
    
    def _collect_variables(self, error: Exception) -> Dict[str, Any]:
        """로컬 변수 수집"""
        variables = {}
        
        try:
            # 현재 프레임의 변수들 수집
            frame = inspect.currentframe()
            if frame and frame.f_back:
                local_vars = frame.f_back.f_locals
                for name, value in local_vars.items():
                    if not name.startswith('_'):
                        try:
                            # 직렬화 가능한 값만 저장
                            json.dumps(value)
                            variables[name] = value
                        except (TypeError, ValueError):
                            variables[name] = str(type(value))
        except Exception:
            pass
        
        return variables
    
    def _generate_error_suggestions(self, error: Exception, error_type: ErrorType, message: str) -> List[str]:
        """오류 개선 제안 생성"""
        suggestions = []
        
        # 일반적인 오류 패턴 매칭
        for pattern, suggestion in self.error_patterns.items():
            if re.search(pattern, message, re.IGNORECASE):
                suggestions.append(suggestion)
        
        # 오류 유형별 제안
        if error_type == ErrorType.SYNTAX:
            suggestions.append("구문 오류를 확인하고 수정하세요.")
            suggestions.append("괄호, 따옴표, 들여쓰기를 확인하세요.")
        
        elif error_type == ErrorType.RUNTIME:
            if isinstance(error, NameError):
                suggestions.append("변수나 함수 이름을 확인하세요.")
                suggestions.append("import 문이 누락되었는지 확인하세요.")
            
            elif isinstance(error, TypeError):
                suggestions.append("함수 인수의 타입을 확인하세요.")
                suggestions.append("None 값 처리를 확인하세요.")
            
            elif isinstance(error, IndexError):
                suggestions.append("리스트나 배열의 인덱스 범위를 확인하세요.")
                suggestions.append("빈 리스트에 대한 접근을 확인하세요.")
        
        elif error_type == ErrorType.MEMORY:
            suggestions.append("메모리 사용량을 최적화하세요.")
            suggestions.append("불필요한 객체를 제거하세요.")
            suggestions.append("데이터 처리를 청크 단위로 나누세요.")
        
        elif error_type == ErrorType.NETWORK:
            suggestions.append("네트워크 연결을 확인하세요.")
            suggestions.append("타임아웃 설정을 조정하세요.")
            suggestions.append("재시도 메커니즘을 구현하세요.")
        
        # 기본 제안
        if not suggestions:
            suggestions.append("오류 메시지를 자세히 확인하세요.")
            suggestions.append("관련 문서를 참조하세요.")
        
        return suggestions
    
    def _is_auto_fixable(self, error_type: ErrorType, message: str) -> bool:
        """자동 수정 가능 여부 판단"""
        
        # 간단한 자동 수정 가능 패턴
        auto_fixable_patterns = [
            r"missing \d+ required positional argument",
            r"unexpected keyword argument",
            r"name '.*' is not defined",
            r"module '.*' has no attribute"
        ]
        
        for pattern in auto_fixable_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        
        return False
    
    def apply_auto_fix(self, debug_info: DebugInfo) -> Dict[str, Any]:
        """자동 수정 적용"""
        
        try:
            # 오류 유형별 자동 수정
            if debug_info.error_type == ErrorType.SYNTAX:
                return self._fix_syntax_error(debug_info)
            
            elif debug_info.error_type == ErrorType.RUNTIME:
                return self._fix_runtime_error(debug_info)
            
            else:
                return {'success': False, 'message': '자동 수정 불가능'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _fix_syntax_error(self, debug_info: DebugInfo) -> Dict[str, Any]:
        """구문 오류 자동 수정"""
        
        try:
            with open(debug_info.file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # 간단한 구문 오류 수정
            fixed_code = code
            
            # 누락된 괄호 수정
            if "unexpected EOF" in debug_info.message:
                # 괄호 균형 확인 및 수정
                open_parens = code.count('(') - code.count(')')
                if open_parens > 0:
                    fixed_code += ')' * open_parens
            
            # 수정된 코드 저장
            if fixed_code != code:
                backup_path = f"{debug_info.file_path}.backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                with open(debug_info.file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                
                return {'success': True, 'message': '구문 오류 수정 완료'}
            
            return {'success': False, 'message': '수정할 내용 없음'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _fix_runtime_error(self, debug_info: DebugInfo) -> Dict[str, Any]:
        """런타임 오류 자동 수정"""
        
        # 간단한 런타임 오류 수정 제안
        fixes = []
        
        if "name" in debug_info.message and "not defined" in debug_info.message:
            # 변수명 오타 수정 제안
            undefined_name = re.search(r"name '(.+)' is not defined", debug_info.message)
            if undefined_name:
                name = undefined_name.group(1)
                fixes.append(f"변수 '{name}'을 정의하거나 import하세요.")
        
        return {'success': True, 'suggestions': fixes}
    
    def monitor_performance(self, duration: int = 60):
        """성능 모니터링"""
        
        self.monitoring_enabled = True
        
        def monitor():
            start_time = time.time()
            
            while self.monitoring_enabled and (time.time() - start_time) < duration:
                # 시스템 메트릭 수집
                cpu_percent = psutil.cpu_percent()
                memory_info = psutil.virtual_memory()
                
                # 성능 임계값 체크
                if cpu_percent > 80:
                    self.logger.warning(f"CPU 사용률이 높습니다: {cpu_percent}%")
                
                if memory_info.percent > 85:
                    self.logger.warning(f"메모리 사용률이 높습니다: {memory_info.percent}%")
                
                time.sleep(1)
        
        # 별도 스레드에서 모니터링 실행
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring_enabled = False
    
    def generate_debug_report(self) -> str:
        """디버그 보고서 생성"""
        
        if not self.debug_history:
            return "🔧 디버그 히스토리가 없습니다."
        
        report = f"""
🔧 디버그 분석 보고서
=====================================

📊 총 디버그 이벤트: {len(self.debug_history)}개

📈 오류 유형별 통계:
"""
        
        # 오류 유형별 집계
        error_counts = {}
        for debug_info in self.debug_history:
            error_type = debug_info.error_type.value
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        for error_type, count in error_counts.items():
            report += f"- {error_type}: {count}개\n"
        
        # 최근 오류들
        recent_errors = self.debug_history[-5:]
        report += f"\n🔍 최근 오류 ({len(recent_errors)}개):\n"
        
        for i, debug_info in enumerate(recent_errors, 1):
            report += f"{i}. {debug_info.message}\n"
            report += f"   파일: {debug_info.file_path}:{debug_info.line_number}\n"
            report += f"   시간: {debug_info.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            if debug_info.suggestions:
                report += f"   제안: {debug_info.suggestions[0]}\n"
            report += "\n"
        
        # 성능 요약
        if self.performance_history:
            avg_time = sum(p['metrics'].execution_time for p in self.performance_history) / len(self.performance_history)
            report += f"📊 평균 실행 시간: {avg_time:.3f}초\n"
        
        return report
    
    def get_performance_insights(self) -> Dict[str, Any]:
        """성능 인사이트 제공"""
        
        if not self.performance_history:
            return {}
        
        # 성능 메트릭 분석
        execution_times = [p['metrics'].execution_time for p in self.performance_history]
        memory_usages = [p['metrics'].memory_usage for p in self.performance_history]
        
        return {
            'total_measurements': len(self.performance_history),
            'avg_execution_time': sum(execution_times) / len(execution_times),
            'max_execution_time': max(execution_times),
            'avg_memory_usage': sum(memory_usages) / len(memory_usages),
            'max_memory_usage': max(memory_usages),
            'performance_trend': self._calculate_performance_trend(),
            'bottlenecks': self._identify_bottlenecks()
        }
    
    def _calculate_performance_trend(self) -> str:
        """성능 트렌드 계산"""
        
        if len(self.performance_history) < 2:
            return "insufficient_data"
        
        recent_avg = sum(p['metrics'].execution_time for p in self.performance_history[-5:]) / min(5, len(self.performance_history))
        early_avg = sum(p['metrics'].execution_time for p in self.performance_history[:5]) / min(5, len(self.performance_history))
        
        if recent_avg < early_avg * 0.9:
            return "improving"
        elif recent_avg > early_avg * 1.1:
            return "degrading"
        else:
            return "stable"
    
    def _identify_bottlenecks(self) -> List[str]:
        """병목지점 식별"""
        
        bottlenecks = []
        
        if self.performance_history:
            # 실행 시간이 긴 함수들 식별
            slow_functions = []
            for p in self.performance_history:
                if p['metrics'].execution_time > 1.0:  # 1초 이상
                    slow_functions.append(p['function'])
            
            if slow_functions:
                bottlenecks.append(f"느린 함수: {', '.join(set(slow_functions))}")
            
            # 메모리 사용량이 높은 함수들 식별
            memory_intensive = []
            for p in self.performance_history:
                if p['metrics'].memory_usage > 100:  # 100MB 이상
                    memory_intensive.append(p['function'])
            
            if memory_intensive:
                bottlenecks.append(f"메모리 집약적 함수: {', '.join(set(memory_intensive))}")
        
        return bottlenecks
    
    def _load_error_patterns(self) -> Dict[str, str]:
        """오류 패턴 로드"""
        
        return {
            r"module '.*' has no attribute": "모듈 이름이나 속성 이름을 확인하세요.",
            r"list index out of range": "리스트 인덱스가 범위를 벗어났습니다.",
            r"division by zero": "0으로 나누기 오류입니다. 조건문을 추가하세요.",
            r"connection.*refused": "서버 연결이 거부되었습니다. 서버 상태를 확인하세요.",
            r"permission denied": "권한이 없습니다. 파일 권한을 확인하세요.",
            r"no such file or directory": "파일이나 디렉토리가 존재하지 않습니다.",
            r"invalid syntax": "구문 오류입니다. 문법을 확인하세요.",
            r"indentation error": "들여쓰기 오류입니다. 공백과 탭을 확인하세요."
        }
    
    def _load_auto_fixes(self) -> Dict[str, Callable]:
        """자동 수정 함수 로드"""
        
        return {
            'syntax_error': self._fix_syntax_error,
            'runtime_error': self._fix_runtime_error
        }
    
    def smart_trace(self, func):
        """스마트 함수 추적 데코레이터"""
        
        def wrapper(*args, **kwargs):
            with self.debug_context(func.__name__):
                return func(*args, **kwargs)
        
        return wrapper 