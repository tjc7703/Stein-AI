#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stein AI 연속 개선 시스템
패턴과 효과성을 지속적으로 높이는 자동 개선 시스템
"""

import re
import json
import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import random

@dataclass
class ImprovementPattern:
    """개선 패턴"""
    pattern_id: str
    original_request: str
    enhanced_response: str
    effectiveness_score: float
    success_rate: float
    usage_count: int
    improvement_count: int
    last_improved: str
    improvement_history: List[Dict[str, Any]]
    context_patterns: List[str]
    created_at: str

@dataclass
class ImprovementMetrics:
    """개선 메트릭"""
    total_patterns: int
    average_effectiveness: float
    improvement_rate: float
    best_pattern_id: str
    total_improvements: int
    learning_velocity: float

class SteinAIContinuousImprovementSystem:
    """Stein AI 연속 개선 시스템"""
    
    def __init__(self):
        self.improvement_patterns = {}
        self.improvement_history = []
        self.stein_preferences = self._load_improvement_preferences()
        self.learning_engine = self._initialize_learning_engine()
        self.improvement_metrics = self._initialize_improvement_metrics()
        self.auto_improvement_enabled = True
        
    def _load_improvement_preferences(self) -> Dict[str, Any]:
        """개선 선호도 로드"""
        return {
            "improvement_threshold": 0.1,  # 10% 이상 개선 시 적용
            "learning_rate": 0.15,
            "improvement_frequency": 5,  # 5번 사용마다 개선 시도
            "max_improvement_attempts": 3,
            "effectiveness_target": 0.95,
            "success_rate_target": 0.9,
            "auto_optimization": True,
            "continuous_learning": True
        }
    
    def _initialize_learning_engine(self) -> Dict[str, Any]:
        """학습 엔진 초기화"""
        return {
            "pattern_analysis": {
                "keyword_effectiveness": defaultdict(float),
                "context_effectiveness": defaultdict(float),
                "style_effectiveness": defaultdict(float)
            },
            "improvement_strategies": {
                "keyword_enhancement": 0.3,
                "context_adaptation": 0.3,
                "style_optimization": 0.4
            },
            "learning_algorithms": {
                "reinforcement_learning": True,
                "pattern_matching": True,
                "context_learning": True
            }
        }
    
    def _initialize_improvement_metrics(self) -> ImprovementMetrics:
        """개선 메트릭 초기화"""
        return ImprovementMetrics(
            total_patterns=0,
            average_effectiveness=0.0,
            improvement_rate=0.0,
            best_pattern_id="",
            total_improvements=0,
            learning_velocity=0.0
        )
    
    def create_initial_patterns(self):
        """초기 패턴 생성"""
        base_patterns = [
            {
                "request": "코드 수정해줘",
                "response": "코드 리뷰하면서 개선점을 찾아보자. 성능, 가독성, 보안, 테스트 커버리지를 모두 고려해서 최적화해줘.",
                "effectiveness": 0.85,
                "context": ["code_review", "optimization"]
            },
            {
                "request": "버그 수정",
                "response": "이 에러를 함께 분석해보자. 원인을 찾고 방어 코드도 추가해서 비슷한 문제가 재발하지 않도록 해줘.",
                "effectiveness": 0.90,
                "context": ["bug_fixing", "debugging"]
            },
            {
                "request": "기능 추가",
                "response": "이 기능을 TDD 방식으로 구현해줘. 먼저 테스트를 작성하고, 그 다음 구현하고, 마지막에 통합 테스트도 추가해줘.",
                "effectiveness": 0.88,
                "context": ["feature_development", "tdd"]
            },
            {
                "request": "최적화",
                "response": "성능 프로파일링을 해보고 병목 지점을 찾아서 최적화해줘. 메모리 사용량과 실행 시간을 모두 고려해줘.",
                "effectiveness": 0.87,
                "context": ["performance", "optimization"]
            },
            {
                "request": "테스트",
                "response": "단위 테스트, 통합 테스트, E2E 테스트를 모두 작성해줘. 테스트 커버리지 90% 이상을 목표로 해줘.",
                "effectiveness": 0.92,
                "context": ["testing", "coverage"]
            }
        ]
        
        for i, pattern_data in enumerate(base_patterns):
            pattern_id = f"pattern_{i+1}"
            pattern = ImprovementPattern(
                pattern_id=pattern_id,
                original_request=pattern_data["request"],
                enhanced_response=pattern_data["response"],
                effectiveness_score=pattern_data["effectiveness"],
                success_rate=pattern_data["effectiveness"],
                usage_count=0,
                improvement_count=0,
                last_improved="",
                improvement_history=[],
                context_patterns=pattern_data["context"],
                created_at=datetime.now().isoformat()
            )
            
            self.improvement_patterns[pattern_id] = pattern
        
        self.improvement_metrics.total_patterns = len(self.improvement_patterns)
    
    def find_best_pattern(self, request: str) -> Optional[ImprovementPattern]:
        """최적 패턴 찾기"""
        if not self.improvement_patterns:
            return None
        
        request_lower = request.lower()
        best_pattern = None
        best_score = 0.0
        
        for pattern in self.improvement_patterns.values():
            # 요청 유사도 계산
            similarity = self._calculate_request_similarity(request_lower, pattern.original_request.lower())
            
            # 효과성과 유사도의 가중 평균
            score = (similarity * 0.6 + pattern.effectiveness_score * 0.4)
            
            if score > best_score:
                best_score = score
                best_pattern = pattern
        
        return best_pattern if best_score > 0.3 else None
    
    def _calculate_request_similarity(self, request1: str, request2: str) -> float:
        """요청 유사도 계산"""
        words1 = set(request1.split())
        words2 = set(request2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def learn_from_interaction(self, request: str, response: str, satisfaction: float):
        """상호작용에서 학습"""
        # 사용된 패턴 찾기
        best_pattern = self.find_best_pattern(request)
        
        if best_pattern:
            # 패턴 사용 통계 업데이트
            best_pattern.usage_count += 1
            best_pattern.success_rate = (best_pattern.success_rate * 0.9 + satisfaction * 0.1)
            
            # 개선 조건 확인
            if (best_pattern.usage_count % self.stein_preferences["improvement_frequency"] == 0 and
                best_pattern.improvement_count < self.stein_preferences["max_improvement_attempts"]):
                
                # 패턴 개선 시도
                improved_pattern = self._improve_pattern(best_pattern, satisfaction)
                if improved_pattern:
                    self.improvement_patterns[improved_pattern.pattern_id] = improved_pattern
                    self.improvement_metrics.total_improvements += 1
        
        # 학습 기록 추가
        learning_record = {
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "response": response,
            "satisfaction": satisfaction,
            "pattern_used": best_pattern.pattern_id if best_pattern else None,
            "improvement_applied": best_pattern is not None and best_pattern.improvement_count > 0
        }
        
        self.improvement_history.append(learning_record)
        
        # 메트릭 업데이트
        self._update_improvement_metrics()
    
    def _improve_pattern(self, pattern: ImprovementPattern, satisfaction: float) -> Optional[ImprovementPattern]:
        """패턴 개선"""
        # 현재 효과성
        current_effectiveness = pattern.effectiveness_score
        
        # 개선 전략 선택
        improvement_strategy = self._select_improvement_strategy(pattern)
        
        # 개선된 응답 생성
        improved_response = self._apply_improvement_strategy(pattern.enhanced_response, improvement_strategy)
        
        # 개선된 효과성 예측
        predicted_effectiveness = self._predict_improved_effectiveness(pattern, improved_response, satisfaction)
        
        # 개선 임계값 확인
        improvement_gain = predicted_effectiveness - current_effectiveness
        
        if improvement_gain >= self.stein_preferences["improvement_threshold"]:
            # 개선 적용
            improved_pattern = ImprovementPattern(
                pattern_id=f"{pattern.pattern_id}_improved_{pattern.improvement_count + 1}",
                original_request=pattern.original_request,
                enhanced_response=improved_response,
                effectiveness_score=predicted_effectiveness,
                success_rate=pattern.success_rate,
                usage_count=pattern.usage_count,
                improvement_count=pattern.improvement_count + 1,
                last_improved=datetime.now().isoformat(),
                improvement_history=pattern.improvement_history + [{
                    "strategy": improvement_strategy,
                    "improvement_gain": improvement_gain,
                    "timestamp": datetime.now().isoformat()
                }],
                context_patterns=pattern.context_patterns,
                created_at=pattern.created_at
            )
            
            return improved_pattern
        
        return None
    
    def _select_improvement_strategy(self, pattern: ImprovementPattern) -> str:
        """개선 전략 선택"""
        strategies = ["keyword_enhancement", "context_adaptation", "style_optimization"]
        weights = [
            self.learning_engine["improvement_strategies"]["keyword_enhancement"],
            self.learning_engine["improvement_strategies"]["context_adaptation"],
            self.learning_engine["improvement_strategies"]["style_optimization"]
        ]
        
        return random.choices(strategies, weights=weights)[0]
    
    def _apply_improvement_strategy(self, response: str, strategy: str) -> str:
        """개선 전략 적용"""
        if strategy == "keyword_enhancement":
            return self._enhance_keywords(response)
        elif strategy == "context_adaptation":
            return self._adapt_context(response)
        else:  # style_optimization
            return self._optimize_style(response)
    
    def _enhance_keywords(self, response: str) -> str:
        """키워드 강화"""
        stein_keywords = [
            "함께", "협업", "분석", "최적화", "테스트", "보안", "성능",
            "문서화", "리뷰", "개선", "구현", "설계", "검증", "모니터링"
        ]
        
        # 랜덤하게 키워드 추가
        missing_keywords = [kw for kw in stein_keywords if kw not in response]
        if missing_keywords:
            new_keyword = random.choice(missing_keywords)
            response += f" {new_keyword}도 고려해서 구현해줘."
        
        return response
    
    def _adapt_context(self, response: str) -> str:
        """컨텍스트 적응"""
        context_adaptations = [
            " Stein님의 개발 스타일에 맞춰서",
            " 최고 효율적으로",
            " 혁신적인 방식으로",
            " Stein님만의 방식으로",
            " 창의적으로"
        ]
        
        adaptation = random.choice(context_adaptations)
        response = f"{adaptation} {response}"
        
        return response
    
    def _optimize_style(self, response: str) -> str:
        """스타일 최적화"""
        # 더 구체적이고 실용적인 표현으로 변경
        style_improvements = {
            "코드 리뷰하면서": "Stein님과 함께 코드를 분석하면서",
            "이 에러를 함께": "이 문제를 Stein님과 함께",
            "이 기능을 TDD": "이 기능을 Stein님 스타일의 TDD",
            "성능 프로파일링": "Stein님 방식의 성능 프로파일링",
            "단위 테스트": "Stein님 품질 기준의 단위 테스트"
        }
        
        for old_phrase, new_phrase in style_improvements.items():
            if old_phrase in response:
                response = response.replace(old_phrase, new_phrase)
                break
        
        return response
    
    def _predict_improved_effectiveness(self, pattern: ImprovementPattern, improved_response: str, satisfaction: float) -> float:
        """개선된 효과성 예측"""
        # 기본 개선 효과
        base_improvement = 0.05
        
        # 만족도 기반 개선
        satisfaction_improvement = max(0, satisfaction - pattern.success_rate) * 0.1
        
        # 키워드 다양성 기반 개선
        stein_keywords = ["함께", "협업", "분석", "최적화", "테스트", "보안", "성능"]
        keyword_diversity = sum(1 for kw in stein_keywords if kw in improved_response) / len(stein_keywords)
        keyword_improvement = keyword_diversity * 0.03
        
        # 응답 길이 기반 개선 (적절한 길이)
        word_count = len(improved_response.split())
        length_improvement = 0.02 if 15 <= word_count <= 60 else -0.01
        
        predicted_effectiveness = (
            pattern.effectiveness_score +
            base_improvement +
            satisfaction_improvement +
            keyword_improvement +
            length_improvement
        )
        
        return min(1.0, max(0.0, predicted_effectiveness))
    
    def generate_improved_response(self, request: str) -> Dict[str, Any]:
        """개선된 응답 생성"""
        best_pattern = self.find_best_pattern(request)
        
        if best_pattern:
            # 패턴 기반 응답
            enhanced_response = self._adapt_pattern_to_request(request, best_pattern)
            confidence = best_pattern.effectiveness_score
            pattern_id = best_pattern.pattern_id
            improvement_count = best_pattern.improvement_count
        else:
            # 새로운 패턴 생성
            enhanced_response = self._generate_new_pattern_response(request)
            confidence = 0.6
            pattern_id = "new_pattern"
            improvement_count = 0
        
        return {
            "original": request,
            "enhanced": enhanced_response,
            "confidence": confidence,
            "pattern_id": pattern_id,
            "improvement_count": improvement_count,
            "improvement_metrics": self._get_current_metrics()
        }
    
    def _adapt_pattern_to_request(self, request: str, pattern: ImprovementPattern) -> str:
        """요청에 맞게 패턴 적응"""
        response = pattern.enhanced_response
        
        # 컨텍스트 적응
        context_patterns = self._extract_context_from_request(request)
        
        for context in context_patterns:
            if context == "python_stack":
                response += " Python의 best practice와 타입 힌트를 적용해서 구현해줘."
            elif context == "react_stack":
                response += " React Hook과 TypeScript를 활용해서 구현해줘."
            elif context == "high_complexity":
                response += " 복잡한 로직을 모듈화하고 설계 패턴을 적용해줘."
            elif context == "high_urgency":
                response += " 빠른 해결을 위해 핵심 기능부터 우선 구현해줘."
        
        return response
    
    def _extract_context_from_request(self, request: str) -> List[str]:
        """요청에서 컨텍스트 추출"""
        context_patterns = []
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["python", "파이썬"]):
            context_patterns.append("python_stack")
        if any(word in request_lower for word in ["react", "리액트"]):
            context_patterns.append("react_stack")
        if any(word in request_lower for word in ["복잡", "고급"]):
            context_patterns.append("high_complexity")
        if any(word in request_lower for word in ["급함", "빨리"]):
            context_patterns.append("high_urgency")
        
        return context_patterns
    
    def _generate_new_pattern_response(self, request: str) -> str:
        """새로운 패턴 응답 생성"""
        base_responses = [
            "Stein님 스타일에 맞춰서 구현해드리겠습니다.",
            "혁신적인 방식으로 접근해서 해결해드리겠습니다.",
            "Stein님만의 창의적인 방법으로 처리해드리겠습니다."
        ]
        
        return random.choice(base_responses)
    
    def _get_current_metrics(self) -> Dict[str, Any]:
        """현재 메트릭 반환"""
        if not self.improvement_patterns:
            return {}
        
        effectiveness_scores = [p.effectiveness_score for p in self.improvement_patterns.values()]
        
        return {
            "total_patterns": len(self.improvement_patterns),
            "average_effectiveness": np.mean(effectiveness_scores),
            "best_effectiveness": max(effectiveness_scores),
            "total_improvements": self.improvement_metrics.total_improvements,
            "improvement_rate": len([p for p in self.improvement_patterns.values() if p.improvement_count > 0]) / len(self.improvement_patterns)
        }
    
    def _update_improvement_metrics(self):
        """개선 메트릭 업데이트"""
        if not self.improvement_patterns:
            return
        
        effectiveness_scores = [p.effectiveness_score for p in self.improvement_patterns.values()]
        best_pattern = max(self.improvement_patterns.values(), key=lambda p: p.effectiveness_score)
        
        self.improvement_metrics.total_patterns = len(self.improvement_patterns)
        self.improvement_metrics.average_effectiveness = np.mean(effectiveness_scores)
        self.improvement_metrics.best_pattern_id = best_pattern.pattern_id
        self.improvement_metrics.improvement_rate = len([p for p in self.improvement_patterns.values() if p.improvement_count > 0]) / len(self.improvement_patterns)
        self.improvement_metrics.learning_velocity = len(self.improvement_history) / max(1, len(self.improvement_patterns))
    
    def get_improvement_report(self) -> Dict[str, Any]:
        """개선 리포트 생성"""
        return {
            "improvement_metrics": asdict(self.improvement_metrics),
            "top_improved_patterns": self._get_top_improved_patterns(5),
            "learning_trends": self._get_learning_trends(),
            "improvement_progress": self._get_improvement_progress()
        }
    
    def _get_top_improved_patterns(self, count: int) -> List[Dict[str, Any]]:
        """상위 개선 패턴들 반환"""
        sorted_patterns = sorted(
            self.improvement_patterns.values(),
            key=lambda p: p.effectiveness_score,
            reverse=True
        )
        
        return [
            {
                "pattern_id": p.pattern_id,
                "original_request": p.original_request,
                "enhanced_response": p.enhanced_response,
                "effectiveness_score": p.effectiveness_score,
                "improvement_count": p.improvement_count,
                "usage_count": p.usage_count
            }
            for p in sorted_patterns[:count]
        ]
    
    def _get_learning_trends(self) -> Dict[str, Any]:
        """학습 트렌드 반환"""
        if len(self.improvement_history) < 5:
            return {"trend": "insufficient_data"}
        
        recent_satisfaction = [r["satisfaction"] for r in self.improvement_history[-10:]]
        recent_improvements = [r["improvement_applied"] for r in self.improvement_history[-10:]]
        
        return {
            "average_satisfaction": np.mean(recent_satisfaction),
            "satisfaction_trend": "improving" if recent_satisfaction[-1] > recent_satisfaction[0] else "declining",
            "improvement_frequency": np.mean(recent_improvements),
            "learning_speed": len(self.improvement_history) / max(1, len(self.improvement_patterns))
        }
    
    def _get_improvement_progress(self) -> Dict[str, Any]:
        """개선 진행도 반환"""
        if not self.improvement_patterns:
            return {"progress": 0.0}
        
        effectiveness_scores = [p.effectiveness_score for p in self.improvement_patterns.values()]
        improvement_counts = [p.improvement_count for p in self.improvement_patterns.values()]
        
        return {
            "average_effectiveness": np.mean(effectiveness_scores),
            "best_effectiveness": max(effectiveness_scores),
            "average_improvements": np.mean(improvement_counts),
            "improvement_progress": np.mean(effectiveness_scores) / self.stein_preferences["effectiveness_target"]
        }

def main():
    """테스트 실행"""
    system = SteinAIContinuousImprovementSystem()
    
    # 초기 패턴 생성
    system.create_initial_patterns()
    
    print("🎯 Stein AI 연속 개선 시스템")
    print("=" * 60)
    
    # 테스트 요청들
    test_requests = [
        "코드 수정해줘",
        "버그 수정",
        "새로운 기능 구현",
        "성능 개선",
        "테스트 코드 작성"
    ]
    
    # 연속 개선 시뮬레이션
    for cycle in range(3):  # 3주기 개선
        print(f"\n🔄 개선 주기 {cycle + 1}")
        
        for i, request in enumerate(test_requests):
            # 응답 생성
            response = system.generate_improved_response(request)
            print(f"📝 원본: {response['original']}")
            print(f"🚀 향상: {response['enhanced']}")
            print(f"📊 신뢰도: {response['confidence']:.2f}")
            print(f"🎯 패턴 ID: {response['pattern_id']}")
            print(f"🔧 개선 횟수: {response['improvement_count']}")
            
            # 학습 시뮬레이션
            satisfaction = 0.8 + (cycle * 0.05) + (i * 0.02) + random.uniform(-0.1, 0.1)
            system.learn_from_interaction(request, response['enhanced'], satisfaction)
            print(f"📈 만족도: {satisfaction:.2f}")
            
            print("-" * 40)
        
        # 개선 리포트 출력
        report = system.get_improvement_report()
        print(f"\n📊 개선 리포트 (주기 {cycle + 1}):")
        print(f"- 총 패턴: {report['improvement_metrics']['total_patterns']}")
        print(f"- 평균 효과성: {report['improvement_metrics']['average_effectiveness']:.2f}")
        print(f"- 개선률: {report['improvement_metrics']['improvement_rate']:.2f}")
        print(f"- 총 개선 횟수: {report['improvement_metrics']['total_improvements']}")
    
    # 최종 개선 리포트
    final_report = system.get_improvement_report()
    print(f"\n🏆 최종 개선 결과:")
    print(f"- 최고 효과성: {final_report['improvement_metrics']['average_effectiveness']:.2f}")
    print(f"- 개선된 패턴 수: {len([p for p in system.improvement_patterns.values() if p.improvement_count > 0])}")
    print(f"- 평균 개선 횟수: {np.mean([p.improvement_count for p in system.improvement_patterns.values()]):.1f}")
    
    # 상위 개선 패턴들
    print(f"\n🏆 상위 개선 패턴들:")
    for i, pattern in enumerate(final_report['top_improved_patterns'][:3]):
        print(f"{i+1}. {pattern['pattern_id']} (효과성: {pattern['effectiveness_score']:.2f}, 개선: {pattern['improvement_count']}회)")
        print(f"   요청: {pattern['original_request']}")
        print(f"   응답: {pattern['enhanced_response'][:50]}...")

if __name__ == "__main__":
    main() 