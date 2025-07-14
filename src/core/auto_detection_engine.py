"""
🤖 Stein AI 자동 판별 및 맥락 추론 엔진
질문 의도 분석, 우선순위 예측, 상황 이해 시스템
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import asyncio

class QuestionIntent(Enum):
    """질문 의도 분류"""
    LEARNING = "learning"           # 학습 목적
    PROBLEM_SOLVING = "problem_solving"  # 문제 해결
    IMPLEMENTATION = "implementation"    # 구현 요청
    OPTIMIZATION = "optimization"       # 최적화
    COMPARISON = "comparison"          # 비교 분석
    DEBUGGING = "debugging"           # 디버깅
    ARCHITECTURE = "architecture"     # 아키텍처 설계
    BEST_PRACTICE = "best_practice"   # 베스트 프랙티스

class UrgencyLevel(Enum):
    """긴급도 수준"""
    CRITICAL = "critical"    # 즉시 처리 필요
    HIGH = "high"           # 높은 우선순위
    MEDIUM = "medium"       # 보통 우선순위
    LOW = "low"            # 낮은 우선순위

class ComplexityLevel(Enum):
    """복잡도 수준"""
    SIMPLE = "simple"       # 간단한 질문
    MODERATE = "moderate"   # 보통 복잡도
    COMPLEX = "complex"     # 복잡한 질문
    EXPERT = "expert"      # 전문가 수준

@dataclass
class ContextualInfo:
    """맥락 정보"""
    time_context: str      # 시간적 맥락
    project_context: str   # 프로젝트 맥락
    tech_context: List[str]  # 기술적 맥락
    user_mood: str         # 사용자 감정 상태
    session_history: List[str]  # 세션 히스토리

@dataclass
class AutoDetectionResult:
    """자동 판별 결과"""
    intent: QuestionIntent
    urgency: UrgencyLevel
    complexity: ComplexityLevel
    priority_score: float  # 0-100점
    context: ContextualInfo
    reasoning: str         # 판별 근거
    suggested_approach: str  # 제안하는 접근 방법
    estimated_time: str    # 예상 소요 시간

class SteinContextualReasoningEngine:
    """Stein AI 맥락 추론 엔진"""
    
    def __init__(self):
        self.intent_patterns = {
            QuestionIntent.LEARNING: [
                r"(학습|배우|이해|알고|설명|원리|개념|기초)",
                r"(어떻게.*작동|왜.*필요|무엇.*의미)"
            ],
            QuestionIntent.PROBLEM_SOLVING: [
                r"(문제|에러|오류|안됨|실패|해결|고치)",
                r"(버그|이상|작동하지|안해|막힘)"
            ],
            QuestionIntent.IMPLEMENTATION: [
                r"(구현|만들|생성|개발|코딩|작성)",
                r"(추가|넣고|기능|모듈|컴포넌트)"
            ],
            QuestionIntent.OPTIMIZATION: [
                r"(최적화|성능|빠르게|효율|개선|향상)",
                r"(속도|메모리|리팩토링|튜닝)"
            ],
            QuestionIntent.COMPARISON: [
                r"(비교|차이|vs|대신|선택|어떤.*좋)",
                r"(장단점|pros.*cons|better|worse)"
            ],
            QuestionIntent.DEBUGGING: [
                r"(디버그|디버깅|찾기|원인|왜.*안)",
                r"(로그|추적|검사|확인)"
            ],
            QuestionIntent.ARCHITECTURE: [
                r"(아키텍처|설계|구조|패턴|시스템)",
                r"(모델링|디자인|프레임워크|구성)"
            ],
            QuestionIntent.BEST_PRACTICE: [
                r"(베스트.*프랙티스|가이드라인|규칙|표준)",
                r"(올바른.*방법|권장|추천.*방식)"
            ]
        }
        
        self.urgency_indicators = {
            UrgencyLevel.CRITICAL: [
                r"(긴급|즉시|빨리|급해|마감|deadline)",
                r"(서버.*다운|장애|critical|emergency)"
            ],
            UrgencyLevel.HIGH: [
                r"(중요|우선|먼저|시급|필수)",
                r"(프로덕션|라이브|production|live)"
            ],
            UrgencyLevel.MEDIUM: [
                r"(보통|일반|평소|때|when)",
                r"(개발|테스트|development|test)"
            ],
            UrgencyLevel.LOW: [
                r"(나중에|여유|시간.*날때|궁금)",
                r"(참고|reference|leisure|curious)"
            ]
        }
        
        self.complexity_indicators = {
            ComplexityLevel.SIMPLE: [
                r"(간단|쉬운|기본|basic|simple)",
                r"(시작|처음|초보|begin)"
            ],
            ComplexityLevel.MODERATE: [
                r"(보통|일반|medium|moderate)",
                r"(중급|intermediate|standard)"
            ],
            ComplexityLevel.COMPLEX: [
                r"(복잡|어려운|고급|complex|advanced)",
                r"(상세|detail|comprehensive)"
            ],
            ComplexityLevel.EXPERT: [
                r"(전문가|expert|professional|master)",
                r"(심화|deep.*dive|architecture.*level)"
            ]
        }
        
        # Stein님의 패턴 학습 데이터
        self.stein_patterns = {
            "preferred_tech": ["Python", "FastAPI", "React", "TypeScript", "AI/ML"],
            "communication_style": "detail_oriented",
            "learning_preference": "hands_on_with_theory",
            "question_evolution": "meta_cognitive",  # 메타인지적 성향
            "priority_tendency": "innovation_first"  # 혁신 우선
        }

    def analyze_context(self, question: str, session_history: List[str] = None) -> ContextualInfo:
        """맥락 정보 분석"""
        
        # 시간적 맥락 분석
        time_context = self._analyze_time_context(question)
        
        # 프로젝트 맥락 분석
        project_context = self._analyze_project_context(question)
        
        # 기술적 맥락 분석
        tech_context = self._analyze_tech_context(question)
        
        # 사용자 감정 상태 분석
        user_mood = self._analyze_user_mood(question)
        
        return ContextualInfo(
            time_context=time_context,
            project_context=project_context,
            tech_context=tech_context,
            user_mood=user_mood,
            session_history=session_history or []
        )

    def _analyze_time_context(self, question: str) -> str:
        """시간적 맥락 분석"""
        if re.search(r"(지금|현재|today|now)", question, re.IGNORECASE):
            return "immediate"
        elif re.search(r"(다음|next|향후|future)", question, re.IGNORECASE):
            return "future_planning"
        elif re.search(r"(이전|과거|before|past)", question, re.IGNORECASE):
            return "retrospective"
        else:
            return "general"

    def _analyze_project_context(self, question: str) -> str:
        """프로젝트 맥락 분석"""
        if re.search(r"(Stein|stein)", question, re.IGNORECASE):
            return "stein_ai_project"
        elif re.search(r"(프로젝트|project)", question, re.IGNORECASE):
            return "current_project"
        elif re.search(r"(시스템|system|플랫폼|platform)", question, re.IGNORECASE):
            return "system_development"
        else:
            return "general_development"

    def _analyze_tech_context(self, question: str) -> List[str]:
        """기술적 맥락 분석"""
        tech_stack = []
        
        for tech in self.stein_patterns["preferred_tech"]:
            if tech.lower() in question.lower():
                tech_stack.append(tech)
        
        # 추가 기술 스택 감지
        additional_tech = {
            "database": ["데이터베이스", "DB", "PostgreSQL", "MongoDB"],
            "frontend": ["프론트엔드", "UI", "UX", "웹"],
            "backend": ["백엔드", "서버", "API"],
            "mobile": ["모바일", "앱", "iOS", "Android"],
            "ai_ml": ["AI", "ML", "인공지능", "머신러닝", "딥러닝"]
        }
        
        for category, keywords in additional_tech.items():
            if any(keyword.lower() in question.lower() for keyword in keywords):
                tech_stack.append(category)
        
        return tech_stack

    def _analyze_user_mood(self, question: str) -> str:
        """사용자 감정 상태 분석"""
        if re.search(r"(고맙|감사|please|부탁)", question, re.IGNORECASE):
            return "polite"
        elif re.search(r"(긴급|급해|빨리|help)", question, re.IGNORECASE):
            return "urgent"
        elif re.search(r"(궁금|curious|wonder)", question, re.IGNORECASE):
            return "curious"
        elif re.search(r"(막힘|어렵|힘들|stuck)", question, re.IGNORECASE):
            return "frustrated"
        elif re.search(r"(좋은|훌륭|excellent|great)", question, re.IGNORECASE):
            return "positive"
        else:
            return "neutral"

    def detect_intent_and_priority(self, question: str, context: ContextualInfo) -> AutoDetectionResult:
        """질문 의도 및 우선순위 자동 감지"""
        
        # 1. 의도 분석
        intent = self._detect_intent(question)
        
        # 2. 긴급도 분석
        urgency = self._detect_urgency(question, context)
        
        # 3. 복잡도 분석
        complexity = self._detect_complexity(question, context)
        
        # 4. 종합 우선순위 점수 계산
        priority_score = self._calculate_priority_score(intent, urgency, complexity, context)
        
        # 5. 추론 근거 생성
        reasoning = self._generate_reasoning(intent, urgency, complexity, context)
        
        # 6. 제안 접근법 생성
        suggested_approach = self._suggest_approach(intent, urgency, complexity, context)
        
        # 7. 예상 소요 시간 계산
        estimated_time = self._estimate_time(complexity, intent)
        
        return AutoDetectionResult(
            intent=intent,
            urgency=urgency,
            complexity=complexity,
            priority_score=priority_score,
            context=context,
            reasoning=reasoning,
            suggested_approach=suggested_approach,
            estimated_time=estimated_time
        )

    def _detect_intent(self, question: str) -> QuestionIntent:
        """질문 의도 감지"""
        scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, question, re.IGNORECASE))
                score += matches
            scores[intent] = score
        
        # 가장 높은 점수의 의도 반환
        if max(scores.values()) == 0:
            return QuestionIntent.LEARNING  # 기본값
        
        return max(scores, key=scores.get)

    def _detect_urgency(self, question: str, context: ContextualInfo) -> UrgencyLevel:
        """긴급도 감지"""
        scores = {}
        
        for urgency, patterns in self.urgency_indicators.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, question, re.IGNORECASE))
                score += matches
            scores[urgency] = score
        
        # 맥락 기반 조정
        if context.user_mood == "urgent":
            scores[UrgencyLevel.HIGH] += 2
        elif context.user_mood == "frustrated":
            scores[UrgencyLevel.HIGH] += 1
        
        if context.project_context == "stein_ai_project":
            scores[UrgencyLevel.HIGH] += 1  # Stein 프로젝트는 우선순위
        
        if max(scores.values()) == 0:
            return UrgencyLevel.MEDIUM  # 기본값
        
        return max(scores, key=scores.get)

    def _detect_complexity(self, question: str, context: ContextualInfo) -> ComplexityLevel:
        """복잡도 감지"""
        scores = {}
        
        for complexity, patterns in self.complexity_indicators.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, question, re.IGNORECASE))
                score += matches
            scores[complexity] = score
        
        # 기술 스택 개수로 복잡도 조정
        tech_count = len(context.tech_context)
        if tech_count >= 3:
            scores[ComplexityLevel.COMPLEX] += 2
        elif tech_count >= 2:
            scores[ComplexityLevel.MODERATE] += 1
        
        # 질문 길이로 복잡도 조정
        if len(question) > 200:
            scores[ComplexityLevel.COMPLEX] += 1
        elif len(question) > 100:
            scores[ComplexityLevel.MODERATE] += 1
        
        if max(scores.values()) == 0:
            return ComplexityLevel.MODERATE  # 기본값
        
        return max(scores, key=scores.get)

    def _calculate_priority_score(self, intent: QuestionIntent, urgency: UrgencyLevel, 
                                 complexity: ComplexityLevel, context: ContextualInfo) -> float:
        """종합 우선순위 점수 계산 (0-100점)"""
        
        # 기본 점수
        base_score = 50.0
        
        # 긴급도 가중치
        urgency_weights = {
            UrgencyLevel.CRITICAL: 40,
            UrgencyLevel.HIGH: 25,
            UrgencyLevel.MEDIUM: 10,
            UrgencyLevel.LOW: -10
        }
        
        # 의도별 가중치 (Stein님 성향 반영)
        intent_weights = {
            QuestionIntent.LEARNING: 15,      # 학습 중시
            QuestionIntent.IMPLEMENTATION: 20, # 구현 중시
            QuestionIntent.OPTIMIZATION: 18,   # 최적화 중시
            QuestionIntent.ARCHITECTURE: 17,   # 아키텍처 중시
            QuestionIntent.PROBLEM_SOLVING: 25, # 문제해결 최우선
            QuestionIntent.COMPARISON: 12,
            QuestionIntent.DEBUGGING: 20,
            QuestionIntent.BEST_PRACTICE: 15
        }
        
        # 복잡도 가중치 (복잡할수록 더 흥미로워함)
        complexity_weights = {
            ComplexityLevel.EXPERT: 15,
            ComplexityLevel.COMPLEX: 10,
            ComplexityLevel.MODERATE: 5,
            ComplexityLevel.SIMPLE: 0
        }
        
        # 점수 계산
        score = base_score
        score += urgency_weights.get(urgency, 0)
        score += intent_weights.get(intent, 0)
        score += complexity_weights.get(complexity, 0)
        
        # 맥락 기반 추가 조정
        if context.project_context == "stein_ai_project":
            score += 10  # Stein 프로젝트 우선
        
        if "AI" in context.tech_context or "ML" in context.tech_context:
            score += 8   # AI/ML 관련 우선
        
        if context.user_mood == "curious":
            score += 5   # 호기심 장려
        
        return max(0.0, min(100.0, score))

    def _generate_reasoning(self, intent: QuestionIntent, urgency: UrgencyLevel, 
                          complexity: ComplexityLevel, context: ContextualInfo) -> str:
        """판별 근거 생성"""
        reasoning_parts = []
        
        # 의도 근거
        intent_reasons = {
            QuestionIntent.LEARNING: "학습 목적의 질문으로 판단됩니다",
            QuestionIntent.PROBLEM_SOLVING: "문제 해결이 필요한 상황으로 보입니다",
            QuestionIntent.IMPLEMENTATION: "구현 요청으로 분류됩니다",
            QuestionIntent.OPTIMIZATION: "성능 최적화 관련 질문입니다",
            QuestionIntent.COMPARISON: "비교 분석을 요청하는 질문입니다",
            QuestionIntent.DEBUGGING: "디버깅 지원이 필요한 상황입니다",
            QuestionIntent.ARCHITECTURE: "시스템 설계 관련 질문입니다",
            QuestionIntent.BEST_PRACTICE: "베스트 프랙티스 조언을 구하는 질문입니다"
        }
        reasoning_parts.append(intent_reasons.get(intent, "일반적인 질문입니다"))
        
        # 긴급도 근거
        if urgency == UrgencyLevel.CRITICAL:
            reasoning_parts.append("즉시 처리가 필요한 긴급한 상황으로 보입니다")
        elif urgency == UrgencyLevel.HIGH:
            reasoning_parts.append("높은 우선순위로 처리해야 할 중요한 질문입니다")
        
        # 복잡도 근거
        if complexity == ComplexityLevel.EXPERT:
            reasoning_parts.append("전문가 수준의 깊이 있는 답변이 필요합니다")
        elif complexity == ComplexityLevel.COMPLEX:
            reasoning_parts.append("복합적인 요소들을 고려한 상세한 분석이 필요합니다")
        
        # 맥락 근거
        if context.project_context == "stein_ai_project":
            reasoning_parts.append("Stein AI 프로젝트와 직접 관련된 질문입니다")
        
        if context.tech_context:
            tech_list = ", ".join(context.tech_context)
            reasoning_parts.append(f"다음 기술들이 관련됩니다: {tech_list}")
        
        return ". ".join(reasoning_parts) + "."

    def _suggest_approach(self, intent: QuestionIntent, urgency: UrgencyLevel, 
                         complexity: ComplexityLevel, context: ContextualInfo) -> str:
        """제안하는 접근 방법"""
        
        approach_suggestions = {
            QuestionIntent.LEARNING: "단계별 설명과 실습 예제를 포함한 학습 자료 제공",
            QuestionIntent.PROBLEM_SOLVING: "문제 분석 → 해결책 제시 → 검증 방법 안내",
            QuestionIntent.IMPLEMENTATION: "요구사항 분석 → 설계 → 단계별 구현 가이드",
            QuestionIntent.OPTIMIZATION: "현재 상태 분석 → 병목점 식별 → 최적화 방안 제시",
            QuestionIntent.COMPARISON: "다각도 비교 분석 → 장단점 정리 → 상황별 추천",
            QuestionIntent.DEBUGGING: "문제 재현 → 원인 분석 → 해결책 제시 → 예방법 안내",
            QuestionIntent.ARCHITECTURE: "요구사항 정의 → 아키텍처 설계 → 구현 전략",
            QuestionIntent.BEST_PRACTICE: "업계 표준 소개 → 실무 적용 방법 → 주의사항"
        }
        
        base_approach = approach_suggestions.get(intent, "질문 분석 후 맞춤형 답변 제공")
        
        # 긴급도에 따른 접근법 조정
        if urgency == UrgencyLevel.CRITICAL:
            return f"🚨 긴급 처리: {base_approach}"
        elif urgency == UrgencyLevel.HIGH:
            return f"⚡ 우선 처리: {base_approach}"
        
        # 복잡도에 따른 접근법 조정
        if complexity == ComplexityLevel.EXPERT:
            return f"🎓 전문가 수준: {base_approach} + 고급 개념 및 심화 분석"
        elif complexity == ComplexityLevel.SIMPLE:
            return f"📚 기초 수준: {base_approach} + 친절한 설명"
        
        return base_approach

    def _estimate_time(self, complexity: ComplexityLevel, intent: QuestionIntent) -> str:
        """예상 소요 시간 계산"""
        
        base_times = {
            ComplexityLevel.SIMPLE: 2,      # 2분
            ComplexityLevel.MODERATE: 5,    # 5분
            ComplexityLevel.COMPLEX: 15,    # 15분
            ComplexityLevel.EXPERT: 30      # 30분
        }
        
        intent_multipliers = {
            QuestionIntent.LEARNING: 1.2,
            QuestionIntent.IMPLEMENTATION: 1.5,
            QuestionIntent.ARCHITECTURE: 1.8,
            QuestionIntent.COMPARISON: 1.3,
            QuestionIntent.PROBLEM_SOLVING: 1.0,
            QuestionIntent.DEBUGGING: 1.1,
            QuestionIntent.OPTIMIZATION: 1.4,
            QuestionIntent.BEST_PRACTICE: 1.1
        }
        
        base_time = base_times.get(complexity, 5)
        multiplier = intent_multipliers.get(intent, 1.0)
        
        estimated_minutes = int(base_time * multiplier)
        
        if estimated_minutes < 5:
            return f"{estimated_minutes}분 내"
        elif estimated_minutes < 60:
            return f"약 {estimated_minutes}분"
        else:
            hours = estimated_minutes // 60
            minutes = estimated_minutes % 60
            return f"약 {hours}시간 {minutes}분"

# 🚀 Stein AI 자동 판별 엔진 인스턴스
stein_auto_detector = SteinContextualReasoningEngine()

async def analyze_question_automatically(question: str, session_history: List[str] = None) -> AutoDetectionResult:
    """질문 자동 분석 함수"""
    
    # 맥락 분석
    context = stein_auto_detector.analyze_context(question, session_history)
    
    # 의도 및 우선순위 감지
    result = stein_auto_detector.detect_intent_and_priority(question, context)
    
    return result

def get_stein_personalized_response(result: AutoDetectionResult) -> Dict[str, Any]:
    """Stein님 맞춤형 응답 생성"""
    
    return {
        "auto_analysis": {
            "intent": result.intent.value,
            "urgency": result.urgency.value,
            "complexity": result.complexity.value,
            "priority_score": result.priority_score,
            "estimated_time": result.estimated_time
        },
        "context_understanding": {
            "time_context": result.context.time_context,
            "project_context": result.context.project_context,
            "tech_context": result.context.tech_context,
            "user_mood": result.context.user_mood
        },
        "ai_reasoning": result.reasoning,
        "suggested_approach": result.suggested_approach,
        "stein_optimization": {
            "priority_explanation": f"우선순위 {result.priority_score:.1f}점 - {result.urgency.value} 긴급도, {result.complexity.value} 복잡도",
            "personalized_note": f"Stein님의 {result.intent.value} 성향을 고려한 맞춤형 접근법을 제안합니다",
            "learning_integration": "이 질문은 Stein AI 개인화 학습 데이터로 활용됩니다"
        }
    } 