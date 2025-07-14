import psutil
import time
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import threading
import asyncio
import subprocess

class OptimizationLevel(Enum):
    """최적화 수준"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"  
    ADVANCED = "advanced"
    AGGRESSIVE = "aggressive"

class ResourceType(Enum):
    """자원 유형"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    DATABASE = "database"

class PerformanceIssue(Enum):
    """성능 이슈 유형"""
    HIGH_CPU_USAGE = "high_cpu_usage"
    MEMORY_LEAK = "memory_leak"
    SLOW_QUERY = "slow_query"
    NETWORK_BOTTLENECK = "network_bottleneck"
    DISK_IO_ISSUE = "disk_io_issue"

@dataclass
class SystemMetrics:
    """시스템 메트릭"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    process_count: int
    active_connections: int
    response_time: float

@dataclass
class FeatureMetadata:
    """기능 메타데이터"""
    name: str
    version: str
    dependencies: List[str]
    resource_usage: Dict[str, float]
    performance_impact: float
    maintenance_cost: float
    usage_frequency: float
    business_value: float

@dataclass
class OptimizationSuggestion:
    """최적화 제안"""
    category: str
    priority: str
    description: str
    expected_improvement: float
    implementation_cost: float
    risk_level: str
    steps: List[str]

class SystemOptimizationEngine:
    """🔧 시스템 최적화 엔진"""
    
    def __init__(self):
        self.metrics_history = []
        self.features_registry = {}
        self.optimization_rules = self._load_optimization_rules()
        self.monitoring_active = False
        self.performance_baselines = {}
        self.compatibility_matrix = {}
        
    def monitor_system_health(self, duration_minutes: int = 60):
        """시스템 건강 상태 모니터링"""
        
        self.monitoring_active = True
        
        def monitor():
            start_time = time.time()
            
            while self.monitoring_active and (time.time() - start_time) < duration_minutes * 60:
                try:
                    # 시스템 메트릭 수집
                    metrics = self._collect_system_metrics()
                    self.metrics_history.append(metrics)
                    
                    # 성능 이슈 감지
                    issues = self._detect_performance_issues(metrics)
                    
                    if issues:
                        self._handle_performance_issues(issues)
                    
                    # 메트릭 히스토리 크기 제한 (최근 1000개만 유지)
                    if len(self.metrics_history) > 1000:
                        self.metrics_history = self.metrics_history[-1000:]
                    
                    time.sleep(30)  # 30초마다 모니터링
                    
                except Exception as e:
                    print(f"모니터링 오류: {e}")
                    time.sleep(60)  # 오류 시 1분 대기
        
        # 별도 스레드에서 모니터링 실행
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        
        return {
            "status": "monitoring_started",
            "duration_minutes": duration_minutes,
            "thread_id": monitor_thread.ident
        }
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """시스템 메트릭 수집"""
        
        # CPU 사용률
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # 메모리 사용률
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # 디스크 사용률
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        
        # 네트워크 I/O
        network = psutil.net_io_counters()
        network_io = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv
        }
        
        # 프로세스 수
        process_count = len(psutil.pids())
        
        # 활성 연결 수 (근사치)
        active_connections = len(psutil.net_connections())
        
        # 응답 시간 (간단한 테스트)
        response_time = self._measure_response_time()
        
        return SystemMetrics(
            timestamp=datetime.now(),
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_io=network_io,
            process_count=process_count,
            active_connections=active_connections,
            response_time=response_time
        )
    
    def _measure_response_time(self) -> float:
        """응답 시간 측정"""
        
        try:
            start_time = time.time()
            # 간단한 로컬 연산으로 응답 시간 측정
            sum(range(1000))
            end_time = time.time()
            return (end_time - start_time) * 1000  # 밀리초 단위
        except Exception:
            return 0.0
    
    def _detect_performance_issues(self, metrics: SystemMetrics) -> List[Tuple[PerformanceIssue, float]]:
        """성능 이슈 감지"""
        
        issues = []
        
        # CPU 사용률 체크
        if metrics.cpu_usage > 80:
            issues.append((PerformanceIssue.HIGH_CPU_USAGE, metrics.cpu_usage))
        
        # 메모리 사용률 체크
        if metrics.memory_usage > 85:
            issues.append((PerformanceIssue.MEMORY_LEAK, metrics.memory_usage))
        
        # 응답 시간 체크
        if metrics.response_time > 100:  # 100ms 초과
            issues.append((PerformanceIssue.SLOW_QUERY, metrics.response_time))
        
        # 디스크 사용률 체크
        if metrics.disk_usage > 90:
            issues.append((PerformanceIssue.DISK_IO_ISSUE, metrics.disk_usage))
        
        return issues
    
    def _handle_performance_issues(self, issues: List[Tuple[PerformanceIssue, float]]):
        """성능 이슈 처리"""
        
        for issue_type, severity in issues:
            if issue_type == PerformanceIssue.HIGH_CPU_USAGE:
                self._optimize_cpu_usage()
            elif issue_type == PerformanceIssue.MEMORY_LEAK:
                self._optimize_memory_usage()
            elif issue_type == PerformanceIssue.SLOW_QUERY:
                self._optimize_response_time()
            elif issue_type == PerformanceIssue.DISK_IO_ISSUE:
                self._optimize_disk_usage()
    
    def _optimize_cpu_usage(self):
        """CPU 사용률 최적화"""
        
        try:
            # 불필요한 프로세스 정리
            import gc
            gc.collect()
            
            # CPU 집약적 작업 조절
            print("🔧 CPU 사용률 최적화 수행 중...")
            
        except Exception as e:
            print(f"CPU 최적화 오류: {e}")
    
    def _optimize_memory_usage(self):
        """메모리 사용률 최적화"""
        
        try:
            # 가비지 컬렉션 강제 실행
            import gc
            gc.collect()
            
            # 캐시 정리
            if hasattr(self, 'cache'):
                self.cache.clear()
            
            print("🔧 메모리 사용률 최적화 수행 중...")
            
        except Exception as e:
            print(f"메모리 최적화 오류: {e}")
    
    def _optimize_response_time(self):
        """응답 시간 최적화"""
        
        try:
            # 데이터베이스 연결 풀 최적화
            # 캐시 워밍업
            # 쿼리 최적화
            print("🔧 응답 시간 최적화 수행 중...")
            
        except Exception as e:
            print(f"응답 시간 최적화 오류: {e}")
    
    def _optimize_disk_usage(self):
        """디스크 사용률 최적화"""
        
        try:
            # 임시 파일 정리
            # 로그 파일 로테이션
            # 불필요한 파일 삭제
            print("🔧 디스크 사용률 최적화 수행 중...")
            
        except Exception as e:
            print(f"디스크 최적화 오류: {e}")
    
    def register_feature(self, feature: FeatureMetadata):
        """기능 등록"""
        
        self.features_registry[feature.name] = feature
        
        # 호환성 체크
        compatibility_issues = self._check_feature_compatibility(feature)
        
        if compatibility_issues:
            return {
                "success": False,
                "issues": compatibility_issues,
                "recommendations": self._suggest_compatibility_fixes(compatibility_issues)
            }
        
        # 성능 영향 평가
        performance_impact = self._assess_performance_impact(feature)
        
        return {
            "success": True,
            "feature_name": feature.name,
            "performance_impact": performance_impact,
            "resource_requirements": feature.resource_usage,
            "dependencies_resolved": feature.dependencies
        }
    
    def _check_feature_compatibility(self, feature: FeatureMetadata) -> List[str]:
        """기능 호환성 체크"""
        
        issues = []
        
        # 의존성 체크
        for dependency in feature.dependencies:
            if dependency not in self.features_registry:
                if not self._is_external_dependency_available(dependency):
                    issues.append(f"의존성 '{dependency}' 을 찾을 수 없습니다.")
        
        # 리소스 충돌 체크
        total_cpu_usage = sum(f.resource_usage.get('cpu', 0) for f in self.features_registry.values())
        if total_cpu_usage + feature.resource_usage.get('cpu', 0) > 80:
            issues.append("CPU 사용률이 임계치를 초과할 수 있습니다.")
        
        total_memory_usage = sum(f.resource_usage.get('memory', 0) for f in self.features_registry.values())
        if total_memory_usage + feature.resource_usage.get('memory', 0) > 85:
            issues.append("메모리 사용률이 임계치를 초과할 수 있습니다.")
        
        # 버전 호환성 체크
        for existing_feature in self.features_registry.values():
            if self._has_version_conflict(feature, existing_feature):
                issues.append(f"기능 '{existing_feature.name}'과 버전 충돌이 있습니다.")
        
        return issues
    
    def _is_external_dependency_available(self, dependency: str) -> bool:
        """외부 의존성 가용성 체크"""
        
        try:
            # 패키지 import 시도
            __import__(dependency)
            return True
        except ImportError:
            return False
    
    def _has_version_conflict(self, feature1: FeatureMetadata, feature2: FeatureMetadata) -> bool:
        """버전 충돌 체크"""
        
        # 간단한 버전 충돌 검사
        common_deps = set(feature1.dependencies) & set(feature2.dependencies)
        
        for dep in common_deps:
            # 실제로는 더 정교한 버전 비교 로직 필요
            if feature1.version != feature2.version:
                return True
        
        return False
    
    def _assess_performance_impact(self, feature: FeatureMetadata) -> Dict[str, Any]:
        """성능 영향 평가"""
        
        # 현재 시스템 상태
        current_metrics = self._collect_system_metrics()
        
        # 예상 성능 영향 계산
        estimated_cpu_impact = feature.resource_usage.get('cpu', 0)
        estimated_memory_impact = feature.resource_usage.get('memory', 0)
        
        return {
            "cpu_impact": f"+{estimated_cpu_impact}%",
            "memory_impact": f"+{estimated_memory_impact}%",
            "response_time_impact": f"+{feature.performance_impact}ms",
            "overall_impact": self._calculate_overall_impact(feature),
            "recommendations": self._generate_performance_recommendations(feature)
        }
    
    def _calculate_overall_impact(self, feature: FeatureMetadata) -> str:
        """전체 영향 계산"""
        
        impact_score = (
            feature.resource_usage.get('cpu', 0) * 0.3 +
            feature.resource_usage.get('memory', 0) * 0.3 +
            feature.performance_impact * 0.2 +
            feature.maintenance_cost * 0.2
        )
        
        if impact_score < 10:
            return "Low"
        elif impact_score < 30:
            return "Medium"
        else:
            return "High"
    
    def _suggest_compatibility_fixes(self, issues: List[str]) -> List[str]:
        """호환성 수정 제안"""
        
        suggestions = []
        
        for issue in issues:
            if "의존성" in issue:
                suggestions.append("필요한 패키지를 설치하거나 버전을 업데이트하세요.")
            elif "CPU" in issue:
                suggestions.append("CPU 집약적인 기능을 비동기로 처리하거나 캐싱을 추가하세요.")
            elif "메모리" in issue:
                suggestions.append("메모리 사용량을 최적화하거나 가비지 컬렉션을 개선하세요.")
            elif "버전 충돌" in issue:
                suggestions.append("의존성 버전을 조정하거나 호환성 레이어를 추가하세요.")
        
        return suggestions
    
    def _generate_performance_recommendations(self, feature: FeatureMetadata) -> List[str]:
        """성능 권장사항 생성"""
        
        recommendations = []
        
        # CPU 사용률이 높은 경우
        if feature.resource_usage.get('cpu', 0) > 20:
            recommendations.append("CPU 집약적 작업을 별도 스레드나 프로세스로 분리하세요.")
            recommendations.append("알고리즘을 최적화하여 연산 복잡도를 줄이세요.")
        
        # 메모리 사용률이 높은 경우
        if feature.resource_usage.get('memory', 0) > 20:
            recommendations.append("메모리 풀링이나 객체 재사용을 고려하세요.")
            recommendations.append("큰 데이터는 스트리밍 방식으로 처리하세요.")
        
        # 성능 영향이 큰 경우
        if feature.performance_impact > 50:
            recommendations.append("데이터베이스 쿼리를 최적화하세요.")
            recommendations.append("캐싱 전략을 구현하세요.")
        
        return recommendations
    
    def optimize_feature_balance(self) -> Dict[str, Any]:
        """기능 균형 최적화"""
        
        # 모든 기능의 가치 vs 비용 분석
        feature_analysis = []
        
        for name, feature in self.features_registry.items():
            value_score = self._calculate_feature_value(feature)
            cost_score = self._calculate_feature_cost(feature)
            efficiency = value_score / max(cost_score, 1)
            
            feature_analysis.append({
                "name": name,
                "value_score": value_score,
                "cost_score": cost_score,
                "efficiency": efficiency,
                "usage_frequency": feature.usage_frequency,
                "maintenance_cost": feature.maintenance_cost
            })
        
        # 효율성 기준으로 정렬
        feature_analysis.sort(key=lambda x: x["efficiency"], reverse=True)
        
        # 최적화 제안 생성
        suggestions = self._generate_balance_suggestions(feature_analysis)
        
        return {
            "feature_analysis": feature_analysis,
            "optimization_suggestions": suggestions,
            "current_balance_score": self._calculate_balance_score(feature_analysis),
            "recommended_actions": self._recommend_balance_actions(feature_analysis)
        }
    
    def _calculate_feature_value(self, feature: FeatureMetadata) -> float:
        """기능 가치 계산"""
        
        return (
            feature.business_value * 0.4 +
            feature.usage_frequency * 0.3 +
            (100 - feature.maintenance_cost) * 0.2 +
            (100 - feature.performance_impact) * 0.1
        )
    
    def _calculate_feature_cost(self, feature: FeatureMetadata) -> float:
        """기능 비용 계산"""
        
        resource_cost = sum(feature.resource_usage.values())
        
        return (
            resource_cost * 0.3 +
            feature.maintenance_cost * 0.3 +
            feature.performance_impact * 0.2 +
            len(feature.dependencies) * 5 * 0.2  # 의존성당 5점
        )
    
    def _calculate_balance_score(self, analysis: List[Dict[str, Any]]) -> float:
        """균형 점수 계산"""
        
        if not analysis:
            return 0.0
        
        total_efficiency = sum(item["efficiency"] for item in analysis)
        avg_efficiency = total_efficiency / len(analysis)
        
        # 효율성의 표준편차를 고려한 균형 점수
        efficiency_variance = sum((item["efficiency"] - avg_efficiency) ** 2 for item in analysis) / len(analysis)
        balance_score = max(0, 100 - efficiency_variance)
        
        return balance_score
    
    def _generate_balance_suggestions(self, analysis: List[Dict[str, Any]]) -> List[OptimizationSuggestion]:
        """균형 최적화 제안 생성"""
        
        suggestions = []
        
        # 효율성이 낮은 기능들 식별
        low_efficiency_features = [item for item in analysis if item["efficiency"] < 0.5]
        
        for feature in low_efficiency_features:
            if feature["usage_frequency"] < 10:  # 사용 빈도가 낮음
                suggestions.append(OptimizationSuggestion(
                    category="feature_removal",
                    priority="medium",
                    description=f"기능 '{feature['name']}'의 사용빈도가 낮습니다. 제거를 고려하세요.",
                    expected_improvement=feature["cost_score"],
                    implementation_cost=20.0,
                    risk_level="low",
                    steps=[
                        "사용자 피드백 수집",
                        "기능 사용 통계 재확인",
                        "단계적 제거 계획 수립"
                    ]
                ))
            
            elif feature["cost_score"] > 70:  # 비용이 높음
                suggestions.append(OptimizationSuggestion(
                    category="cost_optimization",
                    priority="high",
                    description=f"기능 '{feature['name']}'의 비용이 높습니다. 최적화가 필요합니다.",
                    expected_improvement=30.0,
                    implementation_cost=50.0,
                    risk_level="medium",
                    steps=[
                        "리소스 사용량 프로파일링",
                        "알고리즘 최적화",
                        "캐싱 전략 구현",
                        "성능 테스트"
                    ]
                ))
        
        # 고효율 기능들에 대한 확장 제안
        high_efficiency_features = [item for item in analysis if item["efficiency"] > 2.0]
        
        for feature in high_efficiency_features[:3]:  # 상위 3개만
            suggestions.append(OptimizationSuggestion(
                category="feature_enhancement",
                priority="low",
                description=f"기능 '{feature['name']}'의 효율성이 높습니다. 확장을 고려하세요.",
                expected_improvement=feature["efficiency"] * 10,
                implementation_cost=40.0,
                risk_level="low",
                steps=[
                    "기능 확장 계획 수립",
                    "사용자 요구사항 수집",
                    "프로토타입 개발",
                    "A/B 테스트"
                ]
            ))
        
        return suggestions
    
    def _recommend_balance_actions(self, analysis: List[Dict[str, Any]]) -> List[str]:
        """균형 액션 권장"""
        
        actions = []
        
        total_features = len(analysis)
        high_cost_features = len([f for f in analysis if f["cost_score"] > 60])
        low_usage_features = len([f for f in analysis if f["usage_frequency"] < 20])
        
        if high_cost_features > total_features * 0.3:
            actions.append("비용이 높은 기능들의 최적화를 우선적으로 진행하세요.")
        
        if low_usage_features > total_features * 0.2:
            actions.append("사용 빈도가 낮은 기능들의 제거를 검토하세요.")
        
        actions.append("정기적으로 기능 효율성을 모니터링하세요.")
        actions.append("새 기능 추가 시 기존 기능과의 균형을 고려하세요.")
        
        return actions
    
    def generate_comprehensive_optimization_report(self) -> str:
        """종합 최적화 보고서 생성"""
        
        if not self.metrics_history:
            return "📊 충분한 메트릭 데이터가 없습니다. 모니터링을 먼저 시작하세요."
        
        # 최근 시스템 성능 분석
        recent_metrics = self.metrics_history[-10:] if len(self.metrics_history) >= 10 else self.metrics_history
        
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_response = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        
        # 기능 균형 분석
        balance_analysis = self.optimize_feature_balance()
        
        # 최적화 제안
        optimization_suggestions = self._generate_system_optimization_suggestions()
        
        report = f"""
🔧 시스템 종합 최적화 보고서
=====================================

📊 현재 시스템 성능:
- 평균 CPU 사용률: {avg_cpu:.1f}%
- 평균 메모리 사용률: {avg_memory:.1f}%
- 평균 응답 시간: {avg_response:.1f}ms
- 등록된 기능 수: {len(self.features_registry)}개

⚖️ 기능 균형 분석:
- 균형 점수: {balance_analysis['current_balance_score']:.1f}/100
- 고효율 기능: {len([f for f in balance_analysis['feature_analysis'] if f['efficiency'] > 1.5])}개
- 저효율 기능: {len([f for f in balance_analysis['feature_analysis'] if f['efficiency'] < 0.5])}개

🎯 주요 최적화 기회:
"""
        
        # 상위 3개 최적화 제안
        top_suggestions = sorted(optimization_suggestions, key=lambda x: x.expected_improvement, reverse=True)[:3]
        
        for i, suggestion in enumerate(top_suggestions, 1):
            report += f"""
{i}. {suggestion.description}
   - 예상 개선: {suggestion.expected_improvement:.1f}%
   - 구현 비용: {suggestion.implementation_cost:.1f}점
   - 리스크: {suggestion.risk_level}
"""
        
        report += f"""
📈 권장 액션:
"""
        for action in balance_analysis['recommended_actions']:
            report += f"- {action}\n"
        
        report += f"""
🔍 성능 트렌드:
- 시스템 안정성: {"양호" if avg_cpu < 70 and avg_memory < 80 else "주의 필요"}
- 응답 시간: {"우수" if avg_response < 100 else "개선 필요"}
- 리소스 효율성: {"높음" if balance_analysis['current_balance_score'] > 70 else "보통"}

💡 다음 단계:
1. 고우선순위 최적화 항목부터 차례로 적용
2. 정기적인 성능 모니터링 지속
3. 새로운 기능 추가 시 영향 평가 수행
4. 사용자 피드백을 통한 기능 가치 재평가
        """
        
        return report
    
    def _generate_system_optimization_suggestions(self) -> List[OptimizationSuggestion]:
        """시스템 최적화 제안 생성"""
        
        suggestions = []
        
        if not self.metrics_history:
            return suggestions
        
        recent_metrics = self.metrics_history[-10:] if len(self.metrics_history) >= 10 else self.metrics_history
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_response = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        
        # CPU 최적화 제안
        if avg_cpu > 70:
            suggestions.append(OptimizationSuggestion(
                category="cpu_optimization",
                priority="high",
                description="CPU 사용률이 높습니다. 병목 지점을 찾아 최적화하세요.",
                expected_improvement=20.0,
                implementation_cost=60.0,
                risk_level="medium",
                steps=[
                    "CPU 프로파일링 수행",
                    "비효율적인 알고리즘 식별",
                    "비동기 처리 도입",
                    "캐싱 전략 구현"
                ]
            ))
        
        # 메모리 최적화 제안
        if avg_memory > 80:
            suggestions.append(OptimizationSuggestion(
                category="memory_optimization",
                priority="high",
                description="메모리 사용률이 높습니다. 메모리 누수를 확인하세요.",
                expected_improvement=25.0,
                implementation_cost=40.0,
                risk_level="low",
                steps=[
                    "메모리 프로파일링",
                    "불필요한 객체 정리",
                    "가비지 컬렉션 최적화",
                    "메모리 풀링 고려"
                ]
            ))
        
        # 응답 시간 최적화 제안
        if avg_response > 100:
            suggestions.append(OptimizationSuggestion(
                category="response_time_optimization",
                priority="medium",
                description="응답 시간이 느립니다. 쿼리와 알고리즘을 최적화하세요.",
                expected_improvement=30.0,
                implementation_cost=50.0,
                risk_level="medium",
                steps=[
                    "느린 쿼리 식별",
                    "데이터베이스 인덱스 최적화",
                    "API 응답 캐싱",
                    "CDN 활용 검토"
                ]
            ))
        
        return suggestions
    
    def _load_optimization_rules(self) -> Dict[str, Any]:
        """최적화 규칙 로드"""
        
        return {
            "cpu_threshold": 70,
            "memory_threshold": 80,
            "response_time_threshold": 100,
            "disk_threshold": 85,
            "feature_efficiency_threshold": 0.5,
            "auto_optimization_enabled": True,
            "monitoring_interval": 30,  # 초
            "alert_thresholds": {
                "cpu": 90,
                "memory": 95,
                "disk": 95,
                "response_time": 1000
            }
        }
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring_active = False
        return {"status": "monitoring_stopped"}
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """최적화 상태 조회"""
        
        current_metrics = self._collect_system_metrics() if self.monitoring_active else None
        
        return {
            "monitoring_active": self.monitoring_active,
            "metrics_collected": len(self.metrics_history),
            "features_registered": len(self.features_registry),
            "current_metrics": {
                "cpu_usage": current_metrics.cpu_usage if current_metrics else None,
                "memory_usage": current_metrics.memory_usage if current_metrics else None,
                "response_time": current_metrics.response_time if current_metrics else None
            } if current_metrics else None,
            "optimization_recommendations": len(self._generate_system_optimization_suggestions()),
            "system_health": self._assess_system_health()
        }
    
    def _assess_system_health(self) -> str:
        """시스템 건강 상태 평가"""
        
        if not self.metrics_history:
            return "unknown"
        
        recent_metrics = self.metrics_history[-5:] if len(self.metrics_history) >= 5 else self.metrics_history
        
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_response = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        
        if avg_cpu < 50 and avg_memory < 60 and avg_response < 50:
            return "excellent"
        elif avg_cpu < 70 and avg_memory < 80 and avg_response < 100:
            return "good"
        elif avg_cpu < 85 and avg_memory < 90 and avg_response < 200:
            return "fair"
        else:
            return "poor" 