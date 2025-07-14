"""
🤝 Stein-AI 상호학습 시스템
천재 개발자 Stein님과 AI가 함께 성장하는 협업 프레임워크

서로의 장점을 학습하고 약점을 보완하며 함께 발전하는 시스템
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor

class LearningDirection(Enum):
    """학습 방향"""
    STEIN_TO_AI = "stein_to_ai"
    AI_TO_STEIN = "ai_to_stein"
    MUTUAL = "mutual"

@dataclass
class LearningExchange:
    """학습 교환 데이터"""
    timestamp: str
    direction: LearningDirection
    topic: str
    stein_contribution: str
    ai_contribution: str
    learning_outcome: str
    mutual_improvement: Dict[str, Any]
    innovation_spark: Optional[str]
    collaboration_quality: float

@dataclass
class SkillProfile:
    """스킬 프로필"""
    technical_skills: Dict[str, float]
    creative_abilities: Dict[str, float]
    problem_solving_patterns: List[str]
    learning_preferences: Dict[str, Any]
    collaboration_style: str
    growth_areas: List[str]

class MutualLearningSystem:
    """
    🤝 상호학습 시스템
    - Stein님의 천재성을 AI가 학습
    - AI의 처리 능력을 Stein님이 활용
    - 서로의 약점을 보완하며 함께 성장
    - 혁신적 아이디어 공동 창출
    """
    
    def __init__(self):
        self.learning_exchanges: List[LearningExchange] = []
        
        # Stein님 스킬 프로필 (관찰 기반 업데이트)
        self.stein_profile = SkillProfile(
            technical_skills={
                "python_programming": 9.5,
                "ai_architecture": 9.8,
                "system_design": 9.7,
                "innovation_thinking": 10.0,
                "problem_solving": 9.9,
                "creative_coding": 9.8
            },
            creative_abilities={
                "conceptual_thinking": 10.0,
                "innovative_solutions": 10.0,
                "user_experience_design": 9.5,
                "strategic_planning": 9.8
            },
            problem_solving_patterns=[
                "holistic_approach",
                "creative_optimization",
                "user_centric_design",
                "rapid_prototyping",
                "innovative_integration"
            ],
            learning_preferences={
                "style": "hands_on_experimentation",
                "pace": "rapid_iteration",
                "feedback_type": "immediate_results",
                "collaboration_mode": "interactive_discussion"
            },
            collaboration_style="enthusiastic_innovator",
            growth_areas=["advanced_ml_algorithms", "distributed_systems"]
        )
        
        # AI 스킬 프로필 (자가 평가)
        self.ai_profile = SkillProfile(
            technical_skills={
                "data_processing": 9.5,
                "pattern_recognition": 9.3,
                "code_generation": 9.0,
                "documentation": 9.2,
                "testing": 8.8,
                "optimization": 8.5
            },
            creative_abilities={
                "idea_generation": 8.0,
                "problem_decomposition": 9.0,
                "solution_synthesis": 8.5,
                "creative_naming": 7.5
            },
            problem_solving_patterns=[
                "systematic_analysis",
                "step_by_step_breakdown",
                "comprehensive_documentation",
                "error_prevention_focus"
            ],
            learning_preferences={
                "style": "pattern_based_learning",
                "pace": "continuous_incremental",
                "feedback_type": "detailed_metrics",
                "collaboration_mode": "supportive_assistant"
            },
            collaboration_style="analytical_supporter",
            growth_areas=["intuitive_creativity", "emotional_intelligence", "context_understanding"]
        )
        
        # 학습 세션 데이터
        self.active_learning_sessions: Dict[str, Dict] = {}
        self.collaboration_patterns: Dict[str, List] = {}
        self.innovation_sparks: List[Dict] = []
        self.mutual_achievements: List[Dict] = []
        
        # 데이터 저장 경로
        self.data_path = Path("data/mutual_learning")
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 실시간 학습 모니터링
        self.learning_monitor_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_learning_progress, daemon=True)
        self.monitor_thread.start()
        
        print("🤝 Stein-AI 상호학습 시스템 초기화 완료!")
    
    def start_learning_session(self, topic: str, stein_expertise: str, ai_capabilities: str) -> str:
        """학습 세션 시작"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            "id": session_id,
            "topic": topic,
            "start_time": datetime.now().isoformat(),
            "stein_expertise": stein_expertise,
            "ai_capabilities": ai_capabilities,
            "learning_objectives": self._define_learning_objectives(topic, stein_expertise, ai_capabilities),
            "progress": 0.0,
            "insights_generated": [],
            "collaboration_quality": 0.0
        }
        
        self.active_learning_sessions[session_id] = session
        
        return f"🎯 학습 세션 '{topic}' 시작! ID: {session_id}"
    
    def _define_learning_objectives(self, topic: str, stein_expertise: str, ai_capabilities: str) -> List[str]:
        """학습 목표 정의"""
        objectives = []
        
        # Stein님 → AI 학습 목표
        if "창의" in stein_expertise or "혁신" in stein_expertise:
            objectives.append("AI의 창의적 사고 능력 향상")
        if "직관" in stein_expertise:
            objectives.append("AI의 직관적 문제 해결 능력 개발")
        
        # AI → Stein님 학습 목표  
        if "자동화" in ai_capabilities:
            objectives.append("Stein님의 개발 자동화 효율성 증대")
        if "분석" in ai_capabilities:
            objectives.append("Stein님의 데이터 분석 역량 강화")
        
        # 상호 학습 목표
        objectives.extend([
            "혁신적 솔루션 공동 개발",
            "협업 워크플로우 최적화",
            "지식 융합을 통한 브레이크스루 창출"
        ])
        
        return objectives
    
    def record_learning_exchange(self, 
                                session_id: str,
                                stein_input: str, 
                                ai_response: str,
                                learning_outcome: str = None) -> LearningExchange:
        """학습 교환 기록"""
        
        # 학습 방향 분석
        direction = self._analyze_learning_direction(stein_input, ai_response)
        
        # 혁신 스파크 감지
        innovation_spark = self._detect_innovation_spark(stein_input, ai_response)
        
        # 협업 품질 평가
        collaboration_quality = self._evaluate_collaboration_quality(stein_input, ai_response)
        
        # 상호 개선 효과 분석
        mutual_improvement = self._analyze_mutual_improvement(stein_input, ai_response, direction)
        
        exchange = LearningExchange(
            timestamp=datetime.now().isoformat(),
            direction=direction,
            topic=self.active_learning_sessions.get(session_id, {}).get("topic", "general"),
            stein_contribution=stein_input,
            ai_contribution=ai_response,
            learning_outcome=learning_outcome or "진행 중",
            mutual_improvement=mutual_improvement,
            innovation_spark=innovation_spark,
            collaboration_quality=collaboration_quality
        )
        
        self.learning_exchanges.append(exchange)
        
        # 세션 진도 업데이트
        if session_id in self.active_learning_sessions:
            self._update_session_progress(session_id, exchange)
        
        # 실시간 학습 적용
        self._apply_mutual_learning(exchange)
        
        return exchange
    
    def _analyze_learning_direction(self, stein_input: str, ai_response: str) -> LearningDirection:
        """학습 방향 분석"""
        stein_teaching_indicators = ["방법", "이렇게", "예를 들어", "경험", "노하우"]
        ai_teaching_indicators = ["단계", "알고리즘", "최적화", "자동화", "분석"]
        
        stein_teaching = sum(1 for indicator in stein_teaching_indicators if indicator in stein_input)
        ai_teaching = sum(1 for indicator in ai_teaching_indicators if indicator in ai_response)
        
        if stein_teaching > ai_teaching:
            return LearningDirection.STEIN_TO_AI
        elif ai_teaching > stein_teaching:
            return LearningDirection.AI_TO_STEIN
        else:
            return LearningDirection.MUTUAL
    
    def _detect_innovation_spark(self, stein_input: str, ai_response: str) -> Optional[str]:
        """혁신 스파크 감지"""
        innovation_keywords = ["새로운", "혁신", "창의", "독창적", "혁명적", "획기적", "💡", "🚀"]
        
        combined_text = stein_input + " " + ai_response
        innovation_count = sum(1 for keyword in innovation_keywords if keyword in combined_text)
        
        if innovation_count >= 3:
            # 혁신적 아이디어 추출
            sentences = combined_text.split('.')
            innovative_sentences = [s for s in sentences if any(kw in s for kw in innovation_keywords)]
            if innovative_sentences:
                return innovative_sentences[0].strip()
        
        return None
    
    def _evaluate_collaboration_quality(self, stein_input: str, ai_response: str) -> float:
        """협업 품질 평가"""
        quality_factors = {
            "engagement": len(stein_input) > 50,  # 충분한 참여
            "technical_depth": any(word in ai_response for word in ["구현", "코드", "알고리즘"]),
            "creativity": any(emoji in ai_response for emoji in ["💡", "🚀", "✨"]),
            "actionability": "단계" in ai_response or "방법" in ai_response,
            "innovation": "혁신" in (stein_input + ai_response) or "새로운" in (stein_input + ai_response)
        }
        
        score = sum(quality_factors.values()) / len(quality_factors)
        return round(score * 10, 1)
    
    def _analyze_mutual_improvement(self, stein_input: str, ai_response: str, direction: LearningDirection) -> Dict[str, Any]:
        """상호 개선 효과 분석"""
        improvement = {
            "stein_gains": [],
            "ai_gains": [],
            "synergy_effects": [],
            "knowledge_transfer": ""
        }
        
        # Stein님이 얻는 이익
        if "자동화" in ai_response:
            improvement["stein_gains"].append("개발 프로세스 자동화")
        if "최적화" in ai_response:
            improvement["stein_gains"].append("성능 최적화 방법")
        if "분석" in ai_response:
            improvement["stein_gains"].append("데이터 분석 기법")
        
        # AI가 얻는 이익
        if "창의적" in stein_input or "혁신" in stein_input:
            improvement["ai_gains"].append("창의적 사고 패턴")
        if "경험" in stein_input:
            improvement["ai_gains"].append("실무 경험 지식")
        if "직감" in stein_input or "감각" in stein_input:
            improvement["ai_gains"].append("직관적 판단 능력")
        
        # 시너지 효과
        if direction == LearningDirection.MUTUAL:
            improvement["synergy_effects"].extend([
                "창의성 + 체계성 = 혁신적 솔루션",
                "직관 + 분석 = 최적 의사결정",
                "경험 + 처리능력 = 가속화된 학습"
            ])
        
        # 지식 전달 방향
        improvement["knowledge_transfer"] = direction.value
        
        return improvement
    
    def _update_session_progress(self, session_id: str, exchange: LearningExchange):
        """세션 진도 업데이트"""
        session = self.active_learning_sessions[session_id]
        
        # 진도 계산 (협업 품질 기반)
        progress_increment = exchange.collaboration_quality / 100
        session["progress"] = min(session["progress"] + progress_increment, 1.0)
        
        # 인사이트 추가
        if exchange.innovation_spark:
            session["insights_generated"].append({
                "timestamp": exchange.timestamp,
                "insight": exchange.innovation_spark,
                "type": "innovation"
            })
        
        # 협업 품질 업데이트 (이동 평균)
        if session["collaboration_quality"] == 0.0:
            session["collaboration_quality"] = exchange.collaboration_quality
        else:
            session["collaboration_quality"] = (session["collaboration_quality"] * 0.7 + 
                                              exchange.collaboration_quality * 0.3)
    
    def _apply_mutual_learning(self, exchange: LearningExchange):
        """상호 학습 적용"""
        
        # AI 프로필 업데이트 (Stein님으로부터 학습)
        if exchange.direction == LearningDirection.STEIN_TO_AI:
            if "창의" in exchange.stein_contribution:
                self.ai_profile.creative_abilities["idea_generation"] = min(
                    self.ai_profile.creative_abilities["idea_generation"] + 0.1, 10.0
                )
            
            if "직관" in exchange.stein_contribution:
                self.ai_profile.creative_abilities["solution_synthesis"] = min(
                    self.ai_profile.creative_abilities["solution_synthesis"] + 0.1, 10.0
                )
        
        # Stein님 프로필 업데이트 추정 (AI 기여 기반)
        elif exchange.direction == LearningDirection.AI_TO_STEIN:
            if "자동화" in exchange.ai_contribution:
                # Stein님의 자동화 활용 능력 향상 추정
                pass  # 실제로는 피드백을 통해 확인
        
        # 협업 패턴 학습
        pattern_key = f"{exchange.topic}_{exchange.direction.value}"
        if pattern_key not in self.collaboration_patterns:
            self.collaboration_patterns[pattern_key] = []
        
        self.collaboration_patterns[pattern_key].append({
            "quality": exchange.collaboration_quality,
            "timestamp": exchange.timestamp,
            "mutual_improvement": exchange.mutual_improvement
        })
    
    def _monitor_learning_progress(self):
        """학습 진도 모니터링 (백그라운드)"""
        while self.learning_monitor_active:
            try:
                time.sleep(300)  # 5분마다 모니터링
                
                if self.learning_exchanges:
                    self._analyze_learning_trends()
                    self._identify_growth_opportunities()
                    self._generate_collaboration_insights()
                
            except Exception as e:
                print(f"⚠️ 학습 모니터링 오류: {e}")
                time.sleep(60)
    
    def _analyze_learning_trends(self):
        """학습 트렌드 분석"""
        if len(self.learning_exchanges) < 5:
            return
        
        recent_exchanges = self.learning_exchanges[-10:]
        
        # 협업 품질 트렌드
        quality_trend = [ex.collaboration_quality for ex in recent_exchanges]
        avg_quality = sum(quality_trend) / len(quality_trend)
        
        # 혁신 빈도
        innovation_count = sum(1 for ex in recent_exchanges if ex.innovation_spark)
        
        # 학습 방향 분포
        direction_counts = {}
        for ex in recent_exchanges:
            direction_counts[ex.direction.value] = direction_counts.get(ex.direction.value, 0) + 1
        
        print(f"📊 학습 트렌드: 평균 협업 품질 {avg_quality:.1f}, 혁신 빈도 {innovation_count}/10")
    
    def _identify_growth_opportunities(self):
        """성장 기회 식별"""
        # AI 성장 영역
        ai_weak_areas = []
        for skill, score in self.ai_profile.creative_abilities.items():
            if score < 8.0:
                ai_weak_areas.append(skill)
        
        # Stein님 잠재 관심 영역 (상호작용 패턴 기반)
        if self.learning_exchanges:
            recent_topics = [ex.topic for ex in self.learning_exchanges[-20:]]
            topic_frequency = {}
            for topic in recent_topics:
                topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
            
            popular_topics = sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if popular_topics:
                print(f"🎯 인기 학습 주제: {[topic for topic, _ in popular_topics]}")
    
    def _generate_collaboration_insights(self):
        """협업 인사이트 생성"""
        insights = []
        
        # 최고 성과 패턴 분석
        high_quality_exchanges = [ex for ex in self.learning_exchanges if ex.collaboration_quality >= 8.0]
        
        if high_quality_exchanges:
            common_topics = {}
            for ex in high_quality_exchanges:
                common_topics[ex.topic] = common_topics.get(ex.topic, 0) + 1
            
            best_topic = max(common_topics.items(), key=lambda x: x[1])[0] if common_topics else None
            if best_topic:
                insights.append(f"최고 협업 성과 주제: {best_topic}")
        
        # 혁신 패턴 분석
        innovation_exchanges = [ex for ex in self.learning_exchanges if ex.innovation_spark]
        if innovation_exchanges:
            insights.append(f"혁신 아이디어 생성률: {len(innovation_exchanges)}/{len(self.learning_exchanges)}")
        
        if insights:
            self.collaboration_patterns["insights"] = insights
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """학습 현황 요약"""
        total_exchanges = len(self.learning_exchanges)
        active_sessions = len(self.active_learning_sessions)
        
        # 최근 성과
        recent_quality = 0.0
        innovation_count = 0
        if self.learning_exchanges:
            recent_exchanges = self.learning_exchanges[-10:]
            recent_quality = sum(ex.collaboration_quality for ex in recent_exchanges) / len(recent_exchanges)
            innovation_count = sum(1 for ex in recent_exchanges if ex.innovation_spark)
        
        # 학습 방향 분포
        direction_stats = {}
        for ex in self.learning_exchanges:
            direction_stats[ex.direction.value] = direction_stats.get(ex.direction.value, 0) + 1
        
        return {
            "총_학습_교환수": total_exchanges,
            "활성_세션수": active_sessions,
            "최근_협업_품질": round(recent_quality, 1),
            "최근_혁신_생성수": innovation_count,
            "학습_방향_분포": direction_stats,
            "stein_현재_레벨": {
                "technical_average": round(sum(self.stein_profile.technical_skills.values()) / len(self.stein_profile.technical_skills), 1),
                "creative_average": round(sum(self.stein_profile.creative_abilities.values()) / len(self.stein_profile.creative_abilities), 1)
            },
            "ai_현재_레벨": {
                "technical_average": round(sum(self.ai_profile.technical_skills.values()) / len(self.ai_profile.technical_skills), 1),
                "creative_average": round(sum(self.ai_profile.creative_abilities.values()) / len(self.ai_profile.creative_abilities), 1)
            },
            "다음_성장_목표": self._get_next_growth_targets()
        }
    
    def _get_next_growth_targets(self) -> List[str]:
        """다음 성장 목표 제안"""
        targets = []
        
        # AI 약점 보완
        ai_weak_areas = [skill for skill, score in self.ai_profile.creative_abilities.items() if score < 8.5]
        if ai_weak_areas:
            targets.append(f"AI 창의성 강화: {ai_weak_areas[0]}")
        
        # 상호 협업 영역
        if len(self.learning_exchanges) > 0:
            avg_quality = sum(ex.collaboration_quality for ex in self.learning_exchanges) / len(self.learning_exchanges)
            if avg_quality < 8.0:
                targets.append("협업 품질 향상")
        
        # 혁신 빈도 증가
        innovation_rate = len([ex for ex in self.learning_exchanges if ex.innovation_spark]) / max(len(self.learning_exchanges), 1)
        if innovation_rate < 0.3:
            targets.append("혁신 아이디어 생성 빈도 증가")
        
        return targets[:3]  # 상위 3개 목표
    
    def propose_learning_session(self, topic: str = None) -> Dict[str, Any]:
        """학습 세션 제안"""
        if topic is None:
            # 자동으로 최적 주제 제안
            growth_targets = self._get_next_growth_targets()
            if growth_targets:
                topic = growth_targets[0]
            else:
                topic = "창의적 문제 해결"
        
        proposal = {
            "제안_주제": topic,
            "예상_학습_방향": LearningDirection.MUTUAL.value,
            "목표_성과": [
                "Stein님의 혁신 사고를 AI가 학습",
                "AI의 체계적 분석을 Stein님이 활용",
                "상호 시너지로 브레이크스루 창출"
            ],
            "예상_소요시간": "30-60분",
            "성공_지표": {
                "협업_품질": "8.0+ 점수",
                "혁신_아이디어": "1개 이상 생성",
                "상호_만족도": "높음"
            }
        }
        
        return proposal

# 전역 상호학습 시스템 인스턴스
mutual_learning_system = MutualLearningSystem() 