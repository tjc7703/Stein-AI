#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stein AI 적응형 학습 시스템
Stein님의 방식에 맞춰 자동으로 학습하고 적용하는 진정한 AI 시스템
"""

import re
import json
import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from collections import defaultdict

@dataclass
class SteinLearningPattern:
    """Stein님 학습 패턴"""
    original_request: str
    enhanced_response: str
    effectiveness_score: float
    success_rate: float
    usage_frequency: int
    context_patterns: List[str]
    timestamp: str
    feedback_score: Optional[float] = None

@dataclass
class AdaptiveResponse:
    """적응형 응답"""
    original: str
    enhanced: str
    confidence_score: float
    learning_patterns: List[str]
    auto_actions: List[str]
    recommendations: List[str]
    adaptation_reason: str

class SteinAIAdaptiveLearningSystem:
    """Stein AI 적응형 학습 시스템"""
    
    def __init__(self):
        self.learning_patterns = []
        self.stein_preferences = self._load_stein_preferences()
        self.adaptation_history = []
        self.success_metrics = defaultdict(list)
        self.context_learning = {}
        self.auto_learning_enabled = True
        
    def _load_stein_preferences(self) -> Dict[str, Any]:
        """Stein님 선호도 로드"""
        return {
            "language": "korean",
            "style": "collaborative",
            "detail_level": "comprehensive",
            "auto_optimization": True,
            "test_inclusion": True,
            "documentation": True,
            "security_focus": True,
            "performance_focus": True,
            "learning_rate": 0.1,
            "confidence_threshold": 0.8
        }
    
    def learn_from_interaction(self, original: str, enhanced: str, feedback_score: float = None):
        """상호작용에서 학습"""
        pattern = SteinLearningPattern(
            original_request=original,
            enhanced_response=enhanced,
            effectiveness_score=self._calculate_effectiveness(original, enhanced),
            success_rate=feedback_score if feedback_score else 0.8,
            usage_frequency=1,
            context_patterns=self._extract_context_patterns(original),
            timestamp=datetime.now().isoformat(),
            feedback_score=feedback_score
        )
        
        self.learning_patterns.append(pattern)
        self._update_success_metrics(pattern)
        self._adapt_learning_patterns()
    
    def _calculate_effectiveness(self, original: str, enhanced: str) -> float:
        """효과성 계산"""
        # 기본 효과성 점수
        base_score = 0.5
        
        # 키워드 매칭 점수
        keyword_score = self._calculate_keyword_score(original, enhanced)
        
        # 컨텍스트 적합성 점수
        context_score = self._calculate_context_score(original, enhanced)
        
        # 복잡도 적합성 점수
        complexity_score = self._calculate_complexity_score(original, enhanced)
        
        # 가중 평균 계산
        effectiveness = (keyword_score * 0.4 + context_score * 0.3 + complexity_score * 0.3)
        
        return min(1.0, max(0.0, effectiveness))
    
    def _calculate_keyword_score(self, original: str, enhanced: str) -> float:
        """키워드 매칭 점수 계산"""
        original_lower = original.lower()
        enhanced_lower = enhanced.lower()
        
        # Stein님 특화 키워드들
        stein_keywords = [
            "함께", "협업", "분석", "최적화", "테스트", "보안", "성능",
            "문서화", "리뷰", "개선", "구현", "설계", "검증"
        ]
        
        keyword_matches = sum(1 for keyword in stein_keywords if keyword in enhanced_lower)
        return min(1.0, keyword_matches / len(stein_keywords))
    
    def _calculate_context_score(self, original: str, enhanced: str) -> float:
        """컨텍스트 적합성 점수 계산"""
        # 원본 요청의 의도 파악
        original_intent = self._extract_intent(original)
        enhanced_intent = self._extract_intent(enhanced)
        
        # 의도 일치도 계산
        intent_match = self._calculate_intent_similarity(original_intent, enhanced_intent)
        
        return intent_match
    
    def _calculate_complexity_score(self, original: str, enhanced: str) -> float:
        """복잡도 적합성 점수 계산"""
        original_complexity = len(original.split())
        enhanced_complexity = len(enhanced.split())
        
        # Stein님은 상세한 설명을 선호
        if enhanced_complexity > original_complexity * 2:
            return 0.9
        elif enhanced_complexity > original_complexity * 1.5:
            return 0.8
        else:
            return 0.6
    
    def _extract_intent(self, text: str) -> Dict[str, float]:
        """의도 추출"""
        intent_weights = {
            "code_review": 0.0,
            "bug_fixing": 0.0,
            "feature_implementation": 0.0,
            "optimization": 0.0,
            "testing": 0.0,
            "documentation": 0.0,
            "architecture": 0.0,
            "security": 0.0
        }
        
        text_lower = text.lower()
        
        # 의도별 키워드 매칭
        if any(word in text_lower for word in ["수정", "고쳐", "개선", "리뷰"]):
            intent_weights["code_review"] += 0.8
        if any(word in text_lower for word in ["버그", "에러", "오류", "문제"]):
            intent_weights["bug_fixing"] += 0.8
        if any(word in text_lower for word in ["기능", "추가", "구현", "개발"]):
            intent_weights["feature_implementation"] += 0.8
        if any(word in text_lower for word in ["최적화", "성능", "빠르게"]):
            intent_weights["optimization"] += 0.8
        if any(word in text_lower for word in ["테스트", "검증"]):
            intent_weights["testing"] += 0.8
        if any(word in text_lower for word in ["문서", "주석", "설명"]):
            intent_weights["documentation"] += 0.8
        if any(word in text_lower for word in ["구조", "아키텍처", "설계"]):
            intent_weights["architecture"] += 0.8
        if any(word in text_lower for word in ["보안", "인증", "권한"]):
            intent_weights["security"] += 0.8
        
        return intent_weights
    
    def _calculate_intent_similarity(self, intent1: Dict[str, float], intent2: Dict[str, float]) -> float:
        """의도 유사도 계산"""
        if not intent1 or not intent2:
            return 0.0
        
        # 코사인 유사도 계산
        dot_product = sum(intent1[k] * intent2[k] for k in intent1.keys())
        norm1 = sum(v**2 for v in intent1.values()) ** 0.5
        norm2 = sum(v**2 for v in intent2.values()) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _extract_context_patterns(self, text: str) -> List[str]:
        """컨텍스트 패턴 추출"""
        patterns = []
        text_lower = text.lower()
        
        # 기술 스택 패턴
        if any(word in text_lower for word in ["python", "파이썬"]):
            patterns.append("python_stack")
        if any(word in text_lower for word in ["javascript", "js"]):
            patterns.append("javascript_stack")
        if any(word in text_lower for word in ["react", "리액트"]):
            patterns.append("react_stack")
        
        # 복잡도 패턴
        if any(word in text_lower for word in ["간단", "기본"]):
            patterns.append("low_complexity")
        elif any(word in text_lower for word in ["복잡", "고급"]):
            patterns.append("high_complexity")
        else:
            patterns.append("medium_complexity")
        
        # 긴급도 패턴
        if any(word in text_lower for word in ["급함", "빨리", "urgent"]):
            patterns.append("high_urgency")
        else:
            patterns.append("normal_urgency")
        
        return patterns
    
    def _update_success_metrics(self, pattern: SteinLearningPattern):
        """성공 메트릭 업데이트"""
        for context_pattern in pattern.context_patterns:
            self.success_metrics[context_pattern].append({
                "effectiveness": pattern.effectiveness_score,
                "success_rate": pattern.success_rate,
                "timestamp": pattern.timestamp
            })
    
    def _adapt_learning_patterns(self):
        """학습 패턴 적응"""
        if len(self.learning_patterns) < 5:
            return
        
        # 성공률이 높은 패턴들 분석
        successful_patterns = [p for p in self.learning_patterns if p.success_rate > 0.7]
        
        if successful_patterns:
            # 성공 패턴에서 공통 요소 추출
            common_elements = self._extract_common_elements(successful_patterns)
            
            # 새로운 패턴 생성
            self._generate_adaptive_patterns(common_elements)
    
    def _extract_common_elements(self, patterns: List[SteinLearningPattern]) -> Dict[str, Any]:
        """공통 요소 추출"""
        common_elements = {
            "keywords": defaultdict(int),
            "context_patterns": defaultdict(int),
            "response_structures": defaultdict(int)
        }
        
        for pattern in patterns:
            # 키워드 빈도 분석
            for word in pattern.enhanced_response.split():
                if len(word) > 2:
                    common_elements["keywords"][word] += 1
            
            # 컨텍스트 패턴 빈도
            for context in pattern.context_patterns:
                common_elements["context_patterns"][context] += 1
        
        return common_elements
    
    def _generate_adaptive_patterns(self, common_elements: Dict[str, Any]):
        """적응형 패턴 생성"""
        # 가장 자주 사용되는 키워드들
        top_keywords = sorted(common_elements["keywords"].items(), 
                            key=lambda x: x[1], reverse=True)[:10]
        
        # 가장 성공적인 컨텍스트 패턴들
        top_contexts = sorted(common_elements["context_patterns"].items(),
                            key=lambda x: x[1], reverse=True)[:5]
        
        # 새로운 적응형 패턴 생성
        adaptive_pattern = {
            "keywords": [kw[0] for kw in top_keywords],
            "context_patterns": [ctx[0] for ctx in top_contexts],
            "confidence_score": 0.85,
            "generated_at": datetime.now().isoformat()
        }
        
        self.adaptation_history.append(adaptive_pattern)
    
    def generate_adaptive_response(self, request: str) -> AdaptiveResponse:
        """적응형 응답 생성"""
        # 기존 학습 패턴에서 가장 유사한 패턴 찾기
        best_pattern = self._find_best_matching_pattern(request)
        
        if best_pattern and best_pattern.effectiveness_score > 0.8:
            # 학습된 패턴 사용
            enhanced_response = self._adapt_response_to_context(request, best_pattern.enhanced_response)
            confidence_score = best_pattern.effectiveness_score
            adaptation_reason = "학습된 패턴 적용"
        else:
            # 새로운 패턴 생성
            enhanced_response = self._generate_new_response(request)
            confidence_score = 0.6
            adaptation_reason = "새로운 패턴 생성"
        
        # 자동 액션 생성
        auto_actions = self._generate_auto_actions(request, enhanced_response)
        
        # 권장사항 생성
        recommendations = self._generate_recommendations(request, enhanced_response)
        
        return AdaptiveResponse(
            original=request,
            enhanced=enhanced_response,
            confidence_score=confidence_score,
            learning_patterns=self._extract_context_patterns(request),
            auto_actions=auto_actions,
            recommendations=recommendations,
            adaptation_reason=adaptation_reason
        )
    
    def _find_best_matching_pattern(self, request: str) -> Optional[SteinLearningPattern]:
        """최적 매칭 패턴 찾기"""
        if not self.learning_patterns:
            return None
        
        request_intent = self._extract_intent(request)
        request_context = self._extract_context_patterns(request)
        
        best_pattern = None
        best_score = 0.0
        
        for pattern in self.learning_patterns:
            pattern_intent = self._extract_intent(pattern.original_request)
            pattern_context = pattern.context_patterns
            
            # 의도 유사도
            intent_similarity = self._calculate_intent_similarity(request_intent, pattern_intent)
            
            # 컨텍스트 유사도
            context_similarity = len(set(request_context) & set(pattern_context)) / max(len(request_context), len(pattern_context), 1)
            
            # 종합 점수
            total_score = (intent_similarity * 0.7 + context_similarity * 0.3) * pattern.effectiveness_score
            
            if total_score > best_score:
                best_score = total_score
                best_pattern = pattern
        
        return best_pattern if best_score > 0.6 else None
    
    def _adapt_response_to_context(self, request: str, base_response: str) -> str:
        """컨텍스트에 맞게 응답 적응"""
        context_patterns = self._extract_context_patterns(request)
        
        # 컨텍스트별 적응
        if "python_stack" in context_patterns:
            base_response += " Python의 best practice를 적용해서 구현해줘."
        if "react_stack" in context_patterns:
            base_response += " React의 최신 패턴과 TypeScript를 활용해서 구현해줘."
        if "high_complexity" in context_patterns:
            base_response += " 복잡한 로직을 모듈화하고 설계 패턴을 적용해줘."
        if "high_urgency" in context_patterns:
            base_response += " 빠른 해결을 위해 핵심 기능부터 우선 구현해줘."
        
        return base_response
    
    def _generate_new_response(self, request: str) -> str:
        """새로운 응답 생성"""
        intent = self._extract_intent(request)
        context_patterns = self._extract_context_patterns(request)
        
        # 의도별 기본 응답
        base_responses = {
            "code_review": "코드 리뷰하면서 개선점을 찾아보자. 성능, 가독성, 보안을 모두 고려해서 최적화해줘.",
            "bug_fixing": "이 에러를 함께 분석해보자. 원인을 찾고 방어 코드도 추가해서 비슷한 문제가 재발하지 않도록 해줘.",
            "feature_implementation": "이 기능을 TDD 방식으로 구현해줘. 먼저 테스트를 작성하고, 그 다음 구현하고, 마지막에 통합 테스트도 추가해줘.",
            "optimization": "성능 프로파일링을 해보고 병목 지점을 찾아서 최적화해줘. 메모리 사용량과 실행 시간을 모두 고려해줘.",
            "testing": "단위 테스트, 통합 테스트, E2E 테스트를 모두 작성해줘. 테스트 커버리지 90% 이상을 목표로 해줘.",
            "documentation": "코드에 상세한 주석을 추가하고, README와 API 문서도 작성해줘. 한국어로 명확하게 설명해줘.",
            "architecture": "클린 아키텍처 원칙에 따라 시스템을 설계하고, 의존성 주입과 SOLID 원칙을 적용해줘.",
            "security": "보안 취약점을 분석하고, 인증/인가 시스템을 강화해줘. OWASP Top 10을 고려해서 보안을 강화해줘."
        }
        
        # 가장 높은 의도 선택
        max_intent = max(intent.items(), key=lambda x: x[1])
        if max_intent[1] > 0.3:
            base_response = base_responses.get(max_intent[0], "요청을 분석해서 최적의 방법으로 처리해드리겠습니다.")
        else:
            base_response = "요청을 분석해서 최적의 방법으로 처리해드리겠습니다."
        
        return self._adapt_response_to_context(request, base_response)
    
    def _generate_auto_actions(self, request: str, enhanced_response: str) -> List[str]:
        """자동 액션 생성"""
        actions = []
        intent = self._extract_intent(request)
        
        if intent["code_review"] > 0.5:
            actions.extend([
                "코드 품질 분석 및 메트릭 수집",
                "보안 취약점 검사 실행",
                "성능 프로파일링 수행"
            ])
        if intent["bug_fixing"] > 0.5:
            actions.extend([
                "에러 로그 분석 및 원인 파악",
                "디버깅 및 문제점 식별",
                "방어 코드 및 예외 처리 추가"
            ])
        if intent["feature_implementation"] > 0.5:
            actions.extend([
                "요구사항 분석 및 설계",
                "테스트 코드 먼저 작성 (TDD)",
                "기능 구현 및 최적화"
            ])
        
        return actions[:6]  # 최대 6개 액션
    
    def _generate_recommendations(self, request: str, enhanced_response: str) -> List[str]:
        """권장사항 생성"""
        recommendations = []
        context_patterns = self._extract_context_patterns(request)
        
        if "python_stack" in context_patterns:
            recommendations.append("Python 타입 힌트와 docstring 추가")
        if "react_stack" in context_patterns:
            recommendations.append("React Hook과 TypeScript 활용")
        if "high_complexity" in context_patterns:
            recommendations.append("모듈화 및 단위 테스트 강화")
        
        return recommendations[:3]
    
    def get_learning_status(self) -> Dict[str, Any]:
        """학습 상태 반환"""
        return {
            "total_patterns": len(self.learning_patterns),
            "successful_patterns": len([p for p in self.learning_patterns if p.success_rate > 0.7]),
            "average_effectiveness": np.mean([p.effectiveness_score for p in self.learning_patterns]) if self.learning_patterns else 0,
            "adaptation_count": len(self.adaptation_history),
            "confidence_threshold": self.stein_preferences["confidence_threshold"]
        }

def main():
    """테스트 실행"""
    system = SteinAIAdaptiveLearningSystem()
    
    # 학습 데이터 추가
    learning_data = [
        ("코드 수정해줘", "코드 리뷰하면서 개선점을 찾아보자. 성능, 가독성, 보안을 모두 고려해서 최적화해줘.", 0.9),
        ("버그 수정", "이 에러를 함께 분석해보자. 원인을 찾고 방어 코드도 추가해서 비슷한 문제가 재발하지 않도록 해줘.", 0.95),
        ("기능 추가", "이 기능을 TDD 방식으로 구현해줘. 먼저 테스트를 작성하고, 그 다음 구현하고, 마지막에 통합 테스트도 추가해줘.", 0.85),
        ("최적화", "성능 프로파일링을 해보고 병목 지점을 찾아서 최적화해줘. 메모리 사용량과 실행 시간을 모두 고려해줘.", 0.8),
        ("테스트", "단위 테스트, 통합 테스트, E2E 테스트를 모두 작성해줘. 테스트 커버리지 90% 이상을 목표로 해줘.", 0.9)
    ]
    
    # 학습 실행
    for original, enhanced, feedback in learning_data:
        system.learn_from_interaction(original, enhanced, feedback)
    
    # 적응형 응답 테스트
    test_requests = [
        "코드 수정해줘",
        "버그 수정",
        "새로운 기능 구현",
        "성능 개선",
        "테스트 코드 작성"
    ]
    
    print("🎯 Stein AI 적응형 학습 시스템")
    print("=" * 60)
    
    for request in test_requests:
        response = system.generate_adaptive_response(request)
        print(f"\n📝 원본: {response.original}")
        print(f"🚀 향상: {response.enhanced}")
        print(f"📊 신뢰도: {response.confidence_score:.2f}")
        print(f"🎯 적응 이유: {response.adaptation_reason}")
        print(f"🔧 자동 액션: {', '.join(response.auto_actions[:3])}")
        print("-" * 40)
    
    # 학습 상태 출력
    status = system.get_learning_status()
    print(f"\n📈 학습 상태:")
    print(f"- 총 패턴: {status['total_patterns']}")
    print(f"- 성공 패턴: {status['successful_patterns']}")
    print(f"- 평균 효과성: {status['average_effectiveness']:.2f}")
    print(f"- 적응 횟수: {status['adaptation_count']}")

if __name__ == "__main__":
    main() 