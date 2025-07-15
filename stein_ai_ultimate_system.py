#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stein AI 궁극 시스템
Stein님의 방식에 완벽하게 적응하는 진정한 AI 시스템
"""

import re
import json
import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter

@dataclass
class SteinBehaviorPattern:
    """Stein님 행동 패턴"""
    request_type: str
    preferred_style: str
    detail_level: str
    auto_actions: List[str]
    success_rate: float
    usage_count: int
    last_used: str
    adaptation_score: float

@dataclass
class UltimateResponse:
    """궁극 응답"""
    original: str
    enhanced: str
    confidence: float
    adaptation_reason: str
    auto_execution_plan: List[str]
    next_learning_target: str
    stein_satisfaction_prediction: float

class SteinAIUltimateSystem:
    """Stein AI 궁극 시스템"""
    
    def __init__(self):
        self.behavior_patterns = self._initialize_behavior_patterns()
        self.stein_preferences = self._load_stein_preferences()
        self.learning_history = []
        self.adaptation_engine = self._initialize_adaptation_engine()
        self.satisfaction_tracker = defaultdict(list)
        self.auto_learning_enabled = True
        
    def _initialize_behavior_patterns(self) -> Dict[str, SteinBehaviorPattern]:
        """Stein님 행동 패턴 초기화"""
        return {
            "code_review": SteinBehaviorPattern(
                request_type="코드 수정/개선",
                preferred_style="협업 중심, 함께 분석",
                detail_level="포괄적 (성능, 보안, 가독성 모두)",
                auto_actions=[
                    "코드 품질 분석 및 메트릭 수집",
                    "보안 취약점 검사 실행",
                    "성능 프로파일링 수행",
                    "테스트 커버리지 확인",
                    "개선사항 자동 적용",
                    "최종 검증 및 문서화"
                ],
                success_rate=0.95,
                usage_count=0,
                last_used="",
                adaptation_score=0.9
            ),
            
            "bug_fixing": SteinBehaviorPattern(
                request_type="버그 수정/디버깅",
                preferred_style="근본 원인 분석, 방어 코드 추가",
                detail_level="상세한 에러 분석",
                auto_actions=[
                    "에러 로그 분석 및 원인 파악",
                    "디버깅 및 문제점 식별",
                    "방어 코드 및 예외 처리 추가",
                    "단위 테스트 작성 및 실행",
                    "로깅 시스템 강화",
                    "모니터링 설정 추가"
                ],
                success_rate=0.92,
                usage_count=0,
                last_used="",
                adaptation_score=0.88
            ),
            
            "feature_development": SteinBehaviorPattern(
                request_type="기능 개발/구현",
                preferred_style="TDD 방식, 테스트 우선",
                detail_level="완전한 개발 사이클",
                auto_actions=[
                    "요구사항 분석 및 설계",
                    "테스트 코드 먼저 작성 (TDD)",
                    "기능 구현 및 최적화",
                    "통합 테스트 및 검증",
                    "문서화 및 API 스펙 생성",
                    "배포 준비 및 컨테이너화"
                ],
                success_rate=0.89,
                usage_count=0,
                last_used="",
                adaptation_score=0.85
            ),
            
            "performance_optimization": SteinBehaviorPattern(
                request_type="성능 최적화",
                preferred_style="프로파일링 기반, 데이터 중심",
                detail_level="정량적 성능 분석",
                auto_actions=[
                    "성능 프로파일링 실행",
                    "병목 지점 식별 및 분석",
                    "알고리즘 최적화 적용",
                    "메모리 사용량 최적화",
                    "벤치마크 테스트 실행",
                    "성능 모니터링 설정"
                ],
                success_rate=0.87,
                usage_count=0,
                last_used="",
                adaptation_score=0.83
            ),
            
            "testing_strategy": SteinBehaviorPattern(
                request_type="테스트 전략",
                preferred_style="포괄적 테스트, 자동화",
                detail_level="다층 테스트 구조",
                auto_actions=[
                    "테스트 전략 수립",
                    "단위 테스트 작성",
                    "통합 테스트 작성",
                    "E2E 테스트 작성",
                    "테스트 커버리지 측정",
                    "테스트 자동화 설정"
                ],
                success_rate=0.94,
                usage_count=0,
                last_used="",
                adaptation_score=0.91
            ),
            
            "documentation": SteinBehaviorPattern(
                request_type="문서화",
                preferred_style="한국어 중심, 실용적",
                detail_level="완전한 문서 체계",
                auto_actions=[
                    "코드 주석 분석 및 개선",
                    "README 문서 작성",
                    "API 문서 생성",
                    "아키텍처 문서 작성",
                    "사용자 가이드 작성",
                    "설치 가이드 작성"
                ],
                success_rate=0.86,
                usage_count=0,
                last_used="",
                adaptation_score=0.82
            ),
            
            "architecture_design": SteinBehaviorPattern(
                request_type="아키텍처 설계",
                preferred_style="클린 아키텍처, SOLID 원칙",
                detail_level="확장 가능한 설계",
                auto_actions=[
                    "시스템 요구사항 분석",
                    "아키텍처 패턴 선택",
                    "모듈 설계 및 분리",
                    "의존성 주입 설정",
                    "데이터베이스 설계",
                    "API 설계 및 문서화"
                ],
                success_rate=0.90,
                usage_count=0,
                last_used="",
                adaptation_score=0.87
            ),
            
            "security_enhancement": SteinBehaviorPattern(
                request_type="보안 강화",
                preferred_style="방어적 프로그래밍, OWASP 기준",
                detail_level="다층 보안 구조",
                auto_actions=[
                    "보안 취약점 분석",
                    "인증 시스템 강화",
                    "권한 관리 시스템 구현",
                    "데이터 암호화 적용",
                    "보안 테스트 작성",
                    "보안 모니터링 설정"
                ],
                success_rate=0.93,
                usage_count=0,
                last_used="",
                adaptation_score=0.89
            )
        }
    
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
            "learning_rate": 0.15,
            "confidence_threshold": 0.85,
            "satisfaction_threshold": 0.8,
            "auto_execution": True,
            "continuous_learning": True
        }
    
    def _initialize_adaptation_engine(self) -> Dict[str, Any]:
        """적응 엔진 초기화"""
        return {
            "pattern_recognition": {
                "keyword_weights": defaultdict(float),
                "context_weights": defaultdict(float),
                "style_weights": defaultdict(float)
            },
            "learning_algorithm": {
                "success_rate_threshold": 0.8,
                "adaptation_speed": 0.1,
                "forgetting_factor": 0.05
            },
            "satisfaction_prediction": {
                "response_quality_weight": 0.4,
                "execution_speed_weight": 0.3,
                "completeness_weight": 0.3
            }
        }
    
    def analyze_stein_request(self, request: str) -> Dict[str, Any]:
        """Stein님 요청 분석"""
        analysis = {
            "intent": self._extract_intent(request),
            "context": self._extract_context(request),
            "complexity": self._assess_complexity(request),
            "urgency": self._assess_urgency(request),
            "preferred_style": self._determine_preferred_style(request),
            "expected_detail_level": self._determine_detail_level(request)
        }
        
        return analysis
    
    def _extract_intent(self, request: str) -> Dict[str, float]:
        """의도 추출"""
        intent_weights = {
            "code_review": 0.0,
            "bug_fixing": 0.0,
            "feature_development": 0.0,
            "performance_optimization": 0.0,
            "testing_strategy": 0.0,
            "documentation": 0.0,
            "architecture_design": 0.0,
            "security_enhancement": 0.0
        }
        
        request_lower = request.lower()
        
        # 의도별 키워드 매칭
        intent_keywords = {
            "code_review": ["수정", "고쳐", "개선", "리뷰", "바꿔", "변경"],
            "bug_fixing": ["버그", "에러", "오류", "문제", "디버깅", "에러"],
            "feature_development": ["기능", "추가", "구현", "개발", "새로운", "작성"],
            "performance_optimization": ["최적화", "성능", "빠르게", "효율", "속도"],
            "testing_strategy": ["테스트", "검증", "단위", "통합", "E2E"],
            "documentation": ["문서", "주석", "설명", "README", "API"],
            "architecture_design": ["구조", "아키텍처", "설계", "패턴", "모듈"],
            "security_enhancement": ["보안", "인증", "권한", "암호화", "토큰"]
        }
        
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in request_lower:
                    intent_weights[intent] += 0.3
        
        # 정규화
        total_weight = sum(intent_weights.values())
        if total_weight > 0:
            for intent in intent_weights:
                intent_weights[intent] /= total_weight
        
        return intent_weights
    
    def _extract_context(self, request: str) -> Dict[str, Any]:
        """컨텍스트 추출"""
        context = {
            "technology_stack": [],
            "complexity_level": "medium",
            "urgency_level": "normal",
            "domain_specific": [],
            "constraints": []
        }
        
        request_lower = request.lower()
        
        # 기술 스택 추출
        tech_stack_keywords = {
            "python": ["python", "파이썬", "fastapi", "django"],
            "javascript": ["javascript", "js", "node", "react", "vue"],
            "typescript": ["typescript", "ts"],
            "java": ["java", "자바", "spring"],
            "docker": ["docker", "도커", "컨테이너"],
            "database": ["postgresql", "mysql", "mongodb", "redis"]
        }
        
        for tech, keywords in tech_stack_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                context["technology_stack"].append(tech)
        
        # 복잡도 레벨
        if any(word in request_lower for word in ["간단", "기본", "simple"]):
            context["complexity_level"] = "low"
        elif any(word in request_lower for word in ["복잡", "고급", "advanced"]):
            context["complexity_level"] = "high"
        
        # 긴급도
        if any(word in request_lower for word in ["급함", "빨리", "urgent", "즉시"]):
            context["urgency_level"] = "high"
        
        return context
    
    def _assess_complexity(self, request: str) -> str:
        """복잡도 평가"""
        words = request.split()
        if len(words) <= 3:
            return "low"
        elif len(words) <= 8:
            return "medium"
        else:
            return "high"
    
    def _assess_urgency(self, request: str) -> str:
        """긴급도 평가"""
        urgency_keywords = ["급함", "빨리", "urgent", "즉시", "긴급"]
        if any(keyword in request.lower() for keyword in urgency_keywords):
            return "high"
        return "normal"
    
    def _determine_preferred_style(self, request: str) -> str:
        """선호 스타일 결정"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["함께", "협업", "분석"]):
            return "collaborative"
        elif any(word in request_lower for word in ["빠르게", "간단하게"]):
            return "efficient"
        elif any(word in request_lower for word in ["자세히", "상세히"]):
            return "detailed"
        else:
            return "collaborative"  # 기본값
    
    def _determine_detail_level(self, request: str) -> str:
        """상세도 레벨 결정"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["간단", "기본", "요약"]):
            return "basic"
        elif any(word in request_lower for word in ["자세히", "상세히", "완전히"]):
            return "comprehensive"
        else:
            return "comprehensive"  # Stein님 기본 선호도
    
    def generate_ultimate_response(self, request: str) -> UltimateResponse:
        """궁극 응답 생성"""
        # 요청 분석
        analysis = self.analyze_stein_request(request)
        
        # 최적 패턴 선택
        best_pattern = self._select_best_pattern(analysis)
        
        # 응답 생성
        enhanced_response = self._generate_enhanced_response(request, analysis, best_pattern)
        
        # 신뢰도 계산
        confidence = self._calculate_confidence(analysis, best_pattern)
        
        # 적응 이유
        adaptation_reason = self._determine_adaptation_reason(analysis, best_pattern)
        
        # 자동 실행 계획
        auto_execution_plan = self._generate_auto_execution_plan(best_pattern, analysis)
        
        # 다음 학습 목표
        next_learning_target = self._determine_next_learning_target(analysis)
        
        # 만족도 예측
        satisfaction_prediction = self._predict_satisfaction(enhanced_response, analysis)
        
        # 패턴 사용 통계 업데이트
        self._update_pattern_usage(best_pattern.request_type)
        
        return UltimateResponse(
            original=request,
            enhanced=enhanced_response,
            confidence=confidence,
            adaptation_reason=adaptation_reason,
            auto_execution_plan=auto_execution_plan,
            next_learning_target=next_learning_target,
            stein_satisfaction_prediction=satisfaction_prediction
        )
    
    def _select_best_pattern(self, analysis: Dict[str, Any]) -> SteinBehaviorPattern:
        """최적 패턴 선택"""
        intent = analysis["intent"]
        context = analysis["context"]
        
        # 의도별 점수 계산
        pattern_scores = {}
        
        for pattern_name, pattern in self.behavior_patterns.items():
            score = 0.0
            
            # 의도 매칭 점수
            if pattern_name in intent:
                score += intent[pattern_name] * 0.4
            
            # 성공률 점수
            score += pattern.success_rate * 0.3
            
            # 적응 점수
            score += pattern.adaptation_score * 0.2
            
            # 사용 빈도 점수 (너무 자주 사용된 패턴은 페널티)
            usage_penalty = min(pattern.usage_count * 0.05, 0.1)
            score -= usage_penalty
            
            pattern_scores[pattern_name] = score
        
        # 최고 점수 패턴 선택
        best_pattern_name = max(pattern_scores.keys(), key=lambda k: pattern_scores[k])
        return self.behavior_patterns[best_pattern_name]
    
    def _generate_enhanced_response(self, request: str, analysis: Dict[str, Any], pattern: SteinBehaviorPattern) -> str:
        """향상된 응답 생성"""
        base_responses = {
            "code_review": "코드 리뷰하면서 개선점을 찾아보자. 성능, 가독성, 보안, 테스트 커버리지를 모두 고려해서 최적화해줘.",
            "bug_fixing": "이 에러를 함께 분석해보자. 원인을 찾고 방어 코드도 추가해서 비슷한 문제가 재발하지 않도록 해줘.",
            "feature_development": "이 기능을 TDD 방식으로 구현해줘. 먼저 테스트를 작성하고, 그 다음 구현하고, 마지막에 통합 테스트도 추가해줘.",
            "performance_optimization": "성능 프로파일링을 해보고 병목 지점을 찾아서 최적화해줘. 메모리 사용량과 실행 시간을 모두 고려해줘.",
            "testing_strategy": "단위 테스트, 통합 테스트, E2E 테스트를 모두 작성해줘. 테스트 커버리지 90% 이상을 목표로 해줘.",
            "documentation": "코드에 상세한 주석을 추가하고, README와 API 문서도 작성해줘. 한국어로 명확하게 설명해줘.",
            "architecture_design": "클린 아키텍처 원칙에 따라 시스템을 설계하고, 의존성 주입과 SOLID 원칙을 적용해줘.",
            "security_enhancement": "보안 취약점을 분석하고, 인증/인가 시스템을 강화해줘. OWASP Top 10을 고려해서 보안을 강화해줘."
        }
        
        # 기본 응답 선택
        pattern_key = None
        for key, value in self.behavior_patterns.items():
            if value == pattern:
                pattern_key = key
                break
        
        base_response = base_responses.get(pattern_key, "요청을 분석해서 최적의 방법으로 처리해드리겠습니다.")
        
        # 컨텍스트에 맞게 적응
        enhanced_response = self._adapt_response_to_context(base_response, analysis)
        
        return enhanced_response
    
    def _adapt_response_to_context(self, base_response: str, analysis: Dict[str, Any]) -> str:
        """컨텍스트에 맞게 응답 적응"""
        context = analysis["context"]
        complexity = analysis["complexity"]
        urgency = analysis["urgency"]
        
        # 기술 스택 적응
        if "python" in context["technology_stack"]:
            base_response += " Python의 best practice와 타입 힌트를 적용해서 구현해줘."
        if "javascript" in context["technology_stack"]:
            base_response += " JavaScript ES6+ 문법과 모던 패턴을 활용해서 구현해줘."
        if "react" in context["technology_stack"]:
            base_response += " React Hook과 TypeScript를 활용해서 구현해줘."
        
        # 복잡도 적응
        if complexity == "high":
            base_response += " 복잡한 로직을 모듈화하고 설계 패턴을 적용해줘."
        elif complexity == "low":
            base_response += " 간단하고 명확하게 구현해줘."
        
        # 긴급도 적응
        if urgency == "high":
            base_response += " 빠른 해결을 위해 핵심 기능부터 우선 구현해줘."
        
        return base_response
    
    def _calculate_confidence(self, analysis: Dict[str, Any], pattern: SteinBehaviorPattern) -> float:
        """신뢰도 계산"""
        intent = analysis["intent"]
        
        # 의도 매칭 점수
        intent_match = 0.0
        for pattern_name, pattern_obj in self.behavior_patterns.items():
            if pattern_obj == pattern:
                intent_match = intent.get(pattern_name, 0.0)
                break
        
        # 성공률 점수
        success_score = pattern.success_rate
        
        # 적응 점수
        adaptation_score = pattern.adaptation_score
        
        # 가중 평균
        confidence = (intent_match * 0.4 + success_score * 0.4 + adaptation_score * 0.2)
        
        return min(1.0, max(0.0, confidence))
    
    def _determine_adaptation_reason(self, analysis: Dict[str, Any], pattern: SteinBehaviorPattern) -> str:
        """적응 이유 결정"""
        intent = analysis["intent"]
        context = analysis["context"]
        
        # 의도 기반 적응
        max_intent = max(intent.items(), key=lambda x: x[1])
        if max_intent[1] > 0.5:
            return f"'{max_intent[0]}' 의도에 최적화된 패턴 적용"
        
        # 컨텍스트 기반 적응
        if context["technology_stack"]:
            return f"{', '.join(context['technology_stack'])} 기술 스택에 맞춘 적응"
        
        # 성공률 기반 적응
        if pattern.success_rate > 0.9:
            return f"높은 성공률({pattern.success_rate:.1%}) 패턴 적용"
        
        return "Stein님 선호도 기반 적응"
    
    def _generate_auto_execution_plan(self, pattern: SteinBehaviorPattern, analysis: Dict[str, Any]) -> List[str]:
        """자동 실행 계획 생성"""
        plan = pattern.auto_actions.copy()
        
        # 컨텍스트에 따른 추가 액션
        context = analysis["context"]
        
        if "python" in context["technology_stack"]:
            plan.append("Python 타입 힌트와 docstring 추가")
        if "react" in context["technology_stack"]:
            plan.append("React Hook과 TypeScript 활용")
        if context["complexity_level"] == "high":
            plan.append("모듈화 및 단위 테스트 강화")
        if context["urgency_level"] == "high":
            plan.append("핵심 기능 우선 구현")
        
        return plan[:8]  # 최대 8개 액션
    
    def _determine_next_learning_target(self, analysis: Dict[str, Any]) -> str:
        """다음 학습 목표 결정"""
        intent = analysis["intent"]
        context = analysis["context"]
        
        # 낮은 의도 점수 영역 찾기
        low_intent_areas = [area for area, score in intent.items() if score < 0.3]
        
        if low_intent_areas:
            return f"{low_intent_areas[0]} 영역 학습 강화"
        
        # 새로운 기술 스택 학습
        if not context["technology_stack"]:
            return "기술 스택 인식 능력 향상"
        
        return "전체적인 응답 품질 향상"
    
    def _predict_satisfaction(self, response: str, analysis: Dict[str, Any]) -> float:
        """만족도 예측"""
        # 응답 품질 점수
        response_quality = self._assess_response_quality(response, analysis)
        
        # 실행 속도 점수
        execution_speed = 0.8  # 기본값
        
        # 완성도 점수
        completeness = 0.9  # 기본값
        
        # 가중 평균
        satisfaction = (
            response_quality * 0.4 +
            execution_speed * 0.3 +
            completeness * 0.3
        )
        
        return min(1.0, max(0.0, satisfaction))
    
    def _assess_response_quality(self, response: str, analysis: Dict[str, Any]) -> float:
        """응답 품질 평가"""
        # Stein님 선호 키워드 포함 여부
        stein_keywords = ["함께", "협업", "분석", "최적화", "테스트", "보안", "성능"]
        keyword_score = sum(1 for keyword in stein_keywords if keyword in response) / len(stein_keywords)
        
        # 응답 길이 적절성
        word_count = len(response.split())
        length_score = 1.0 if 10 <= word_count <= 50 else 0.7
        
        # 컨텍스트 적합성
        context_score = 0.8  # 기본값
        
        return (keyword_score * 0.4 + length_score * 0.3 + context_score * 0.3)
    
    def _update_pattern_usage(self, pattern_type: str):
        """패턴 사용 통계 업데이트"""
        for pattern_name, pattern in self.behavior_patterns.items():
            if pattern.request_type == pattern_type:
                pattern.usage_count += 1
                pattern.last_used = datetime.now().isoformat()
                break
    
    def learn_from_feedback(self, request: str, response: str, satisfaction_score: float):
        """피드백에서 학습"""
        # 학습 히스토리에 추가
        learning_record = {
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "response": response,
            "satisfaction_score": satisfaction_score,
            "analysis": self.analyze_stein_request(request)
        }
        
        self.learning_history.append(learning_record)
        
        # 패턴 성공률 업데이트
        self._update_pattern_success_rates()
        
        # 적응 엔진 업데이트
        self._update_adaptation_engine(learning_record)
    
    def _update_pattern_success_rates(self):
        """패턴 성공률 업데이트"""
        # 최근 학습 기록에서 성공률 계산
        recent_records = self.learning_history[-10:]  # 최근 10개
        
        for record in recent_records:
            analysis = record["analysis"]
            satisfaction = record["satisfaction_score"]
            
            # 해당하는 패턴 찾기
            for pattern_name, pattern in self.behavior_patterns.items():
                if pattern.request_type in record["request"]:
                    # 성공률 업데이트 (이동 평균)
                    pattern.success_rate = (pattern.success_rate * 0.9 + satisfaction * 0.1)
                    break
    
    def _update_adaptation_engine(self, learning_record: Dict[str, Any]):
        """적응 엔진 업데이트"""
        satisfaction = learning_record["satisfaction_score"]
        analysis = learning_record["analysis"]
        
        # 키워드 가중치 업데이트
        for word in learning_record["request"].split():
            if len(word) > 2:
                self.adaptation_engine["pattern_recognition"]["keyword_weights"][word] += satisfaction * 0.1
        
        # 컨텍스트 가중치 업데이트
        for tech in analysis["context"]["technology_stack"]:
            self.adaptation_engine["pattern_recognition"]["context_weights"][tech] += satisfaction * 0.1
    
    def get_system_status(self) -> Dict[str, Any]:
        """시스템 상태 반환"""
        return {
            "total_patterns": len(self.behavior_patterns),
            "learning_records": len(self.learning_history),
            "average_satisfaction": np.mean([r["satisfaction_score"] for r in self.learning_history]) if self.learning_history else 0,
            "most_used_pattern": max(self.behavior_patterns.values(), key=lambda p: p.usage_count).request_type if self.behavior_patterns else "none",
            "highest_success_pattern": max(self.behavior_patterns.values(), key=lambda p: p.success_rate).request_type if self.behavior_patterns else "none",
            "adaptation_count": len(self.adaptation_engine["pattern_recognition"]["keyword_weights"])
        }

def main():
    """테스트 실행"""
    system = SteinAIUltimateSystem()
    
    # 테스트 요청들
    test_requests = [
        "코드 수정해줘",
        "버그 수정",
        "새로운 기능 구현",
        "성능 개선",
        "테스트 코드 작성",
        "문서화",
        "구조 개선",
        "보안 강화"
    ]
    
    print("🎯 Stein AI 궁극 시스템")
    print("=" * 70)
    
    for request in test_requests:
        response = system.generate_ultimate_response(request)
        print(f"\n📝 원본: {response.original}")
        print(f"🚀 향상: {response.enhanced}")
        print(f"📊 신뢰도: {response.confidence:.2f}")
        print(f"🎯 적응 이유: {response.adaptation_reason}")
        print(f"🔧 자동 실행: {', '.join(response.auto_execution_plan[:3])}")
        print(f"📈 만족도 예측: {response.stein_satisfaction_prediction:.2f}")
        print(f"🎓 다음 학습: {response.next_learning_target}")
        print("-" * 50)
    
    # 피드백 학습 시뮬레이션
    print("\n🧠 피드백 학습 시뮬레이션")
    for i, request in enumerate(test_requests[:3]):
        satisfaction = 0.8 + (i * 0.05)  # 시뮬레이션 만족도
        system.learn_from_feedback(request, f"향상된 응답 {i+1}", satisfaction)
        print(f"학습 완료: {request} -> 만족도 {satisfaction:.2f}")
    
    # 시스템 상태 출력
    status = system.get_system_status()
    print(f"\n📊 시스템 상태:")
    print(f"- 총 패턴: {status['total_patterns']}")
    print(f"- 학습 기록: {status['learning_records']}")
    print(f"- 평균 만족도: {status['average_satisfaction']:.2f}")
    print(f"- 가장 사용된 패턴: {status['most_used_pattern']}")
    print(f"- 최고 성공 패턴: {status['highest_success_pattern']}")

if __name__ == "__main__":
    main() 