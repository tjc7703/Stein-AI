"""
🧬 자기진화형 Stein AI 코어 엔진
실시간 학습, 성능 향상, 자동 최적화 시스템

천재 개발자 Stein님과 함께 서로 발전하는 AI
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading
import pickle
import hashlib

@dataclass
class LearningExperience:
    """학습 경험 데이터 구조"""
    timestamp: str
    interaction_type: str
    user_input: str
    ai_response: str
    feedback_score: float
    context: Dict[str, Any]
    improvement_suggestions: List[str]
    performance_metrics: Dict[str, float]

@dataclass
class EvolutionMetrics:
    """진화 성능 지표"""
    learning_rate: float
    adaptation_speed: float
    creativity_index: float
    problem_solving_efficiency: float
    collaboration_quality: float
    innovation_score: float

class SelfEvolvingEngine:
    """
    🧬 자기진화형 AI 엔진
    - 실시간 학습 및 적응
    - 성능 지속적 향상
    - 창의적 사고 진화
    - Stein님과의 협업 최적화
    """
    
    def __init__(self):
        self.memory_bank: List[LearningExperience] = []
        self.evolution_metrics = EvolutionMetrics(
            learning_rate=1.0,
            adaptation_speed=1.0,
            creativity_index=1.0,
            problem_solving_efficiency=1.0,
            collaboration_quality=1.0,
            innovation_score=1.0
        )
        self.neural_patterns: Dict[str, np.ndarray] = {}
        self.creativity_seeds: List[str] = []
        self.innovation_history: List[Dict] = []
        self.collaboration_insights: Dict[str, Any] = {}
        
        # 진화 프로세스 상태
        self.is_evolving = False
        self.evolution_thread: Optional[threading.Thread] = None
        self.performance_baseline = self._establish_baseline()
        
        # 학습 데이터 저장 경로
        self.data_path = Path("data/evolution")
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 기존 학습 데이터 로드
        self._load_previous_learning()
        
        # 자동 진화 프로세스 시작
        self.start_continuous_evolution()
    
    def _establish_baseline(self) -> Dict[str, float]:
        """성능 기준선 설정"""
        return {
            "response_time": 1.0,
            "accuracy": 0.8,
            "creativity": 0.7,
            "collaboration": 0.8,
            "innovation": 0.6,
            "user_satisfaction": 0.8
        }
    
    def _load_previous_learning(self):
        """이전 학습 경험 로드"""
        try:
            memory_file = self.data_path / "memory_bank.json"
            if memory_file.exists():
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memory_bank = [LearningExperience(**exp) for exp in data]
                print(f"✅ {len(self.memory_bank)}개의 이전 학습 경험 로드")
            
            metrics_file = self.data_path / "evolution_metrics.json"
            if metrics_file.exists():
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.evolution_metrics = EvolutionMetrics(**data)
                print(f"✅ 진화 지표 로드: {self.evolution_metrics}")
                
        except Exception as e:
            print(f"⚠️ 이전 학습 데이터 로드 실패: {e}")
    
    def record_interaction(self, 
                          user_input: str, 
                          ai_response: str, 
                          context: Dict[str, Any] = None,
                          feedback_score: float = None) -> str:
        """
        🎯 사용자 상호작용 기록 및 학습
        """
        if context is None:
            context = {}
        if feedback_score is None:
            feedback_score = self._estimate_interaction_quality(user_input, ai_response)
        
        # 학습 경험 생성
        experience = LearningExperience(
            timestamp=datetime.now().isoformat(),
            interaction_type=self._classify_interaction(user_input),
            user_input=user_input,
            ai_response=ai_response,
            feedback_score=feedback_score,
            context=context,
            improvement_suggestions=self._generate_improvements(user_input, ai_response),
            performance_metrics=self._calculate_performance_metrics(user_input, ai_response)
        )
        
        # 메모리 저장
        self.memory_bank.append(experience)
        
        # 실시간 학습 적용
        self._apply_immediate_learning(experience)
        
        # 패턴 업데이트
        self._update_neural_patterns(experience)
        
        # 협업 인사이트 추출
        self._extract_collaboration_insights(experience)
        
        # 주기적 저장
        if len(self.memory_bank) % 10 == 0:
            self._save_learning_progress()
        
        return f"💡 학습 완료: {feedback_score:.2f} 점수, {len(self.improvement_suggestions)}개 개선사항 식별"
    
    def _classify_interaction(self, user_input: str) -> str:
        """상호작용 유형 분류"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['코드', 'programming', 'development', '개발']):
            return "coding"
        elif any(word in user_lower for word in ['창의적', 'creative', '혁신', 'innovation']):
            return "creative"
        elif any(word in user_lower for word in ['문제', 'problem', '해결', 'solve']):
            return "problem_solving"
        elif any(word in user_lower for word in ['학습', 'learning', '배우', 'study']):
            return "learning"
        elif any(word in user_lower for word in ['협업', 'collaboration', '함께', 'together']):
            return "collaboration"
        else:
            return "general"
    
    def _estimate_interaction_quality(self, user_input: str, ai_response: str) -> float:
        """상호작용 품질 추정"""
        # 응답 길이와 내용 복잡도 기반 점수
        response_length_score = min(len(ai_response) / 1000, 1.0)
        
        # 기술적 내용 점수
        technical_keywords = ['api', 'function', 'class', 'algorithm', 'system', '구현', '개발']
        technical_score = sum(1 for keyword in technical_keywords if keyword in ai_response.lower()) / len(technical_keywords)
        
        # 창의성 점수
        creative_indicators = ['혁신', '창의', '새로운', '독창적', '아이디어', '💡', '🚀', '✨']
        creativity_score = sum(1 for indicator in creative_indicators if indicator in ai_response) / len(creative_indicators)
        
        # 종합 점수 계산
        total_score = (response_length_score * 0.3 + technical_score * 0.4 + creativity_score * 0.3) * 10
        
        return min(max(total_score, 1.0), 10.0)
    
    def _generate_improvements(self, user_input: str, ai_response: str) -> List[str]:
        """개선 제안 생성"""
        improvements = []
        
        # 응답 길이 개선
        if len(ai_response) < 200:
            improvements.append("더 상세한 설명 제공")
        
        # 코드 예시 개선
        if 'code' in user_input.lower() and '```' not in ai_response:
            improvements.append("실제 코드 예시 추가")
        
        # 시각적 요소 개선
        if len([char for char in ai_response if char in '🎯🚀💡✨🔥']) < 3:
            improvements.append("시각적 요소 및 이모지 활용 증가")
        
        # 구체성 개선
        if user_input.count('?') > 0 and ai_response.count('단계') < 1:
            improvements.append("단계별 가이드 제공")
        
        return improvements
    
    def _calculate_performance_metrics(self, user_input: str, ai_response: str) -> Dict[str, float]:
        """성능 지표 계산"""
        return {
            "response_length": len(ai_response),
            "technical_depth": len([word for word in ai_response.split() if len(word) > 8]),
            "creativity_indicators": len([char for char in ai_response if char in '🎯🚀💡✨🔥']),
            "code_examples": ai_response.count('```'),
            "actionable_items": ai_response.count('단계') + ai_response.count('방법'),
            "enthusiasm_level": len([char for char in ai_response if char in '!'])
        }
    
    def _apply_immediate_learning(self, experience: LearningExperience):
        """즉시 학습 적용"""
        # 피드백 점수에 따른 진화 지표 조정
        score_ratio = experience.feedback_score / 10.0
        
        # 학습률 조정
        if score_ratio > 0.8:
            self.evolution_metrics.learning_rate *= 1.02
        elif score_ratio < 0.6:
            self.evolution_metrics.learning_rate *= 0.98
        
        # 적응 속도 조정
        interaction_complexity = len(experience.user_input.split())
        if interaction_complexity > 20:
            self.evolution_metrics.adaptation_speed *= 1.01
        
        # 창의성 지수 업데이트
        if experience.interaction_type == "creative":
            self.evolution_metrics.creativity_index *= 1.03
        
        # 협업 품질 조정
        if "함께" in experience.user_input or "협업" in experience.user_input:
            self.evolution_metrics.collaboration_quality *= 1.02
    
    def _update_neural_patterns(self, experience: LearningExperience):
        """신경 패턴 업데이트"""
        # 입력 텍스트를 벡터로 변환 (간단한 해시 기반)
        input_hash = hashlib.md5(experience.user_input.encode()).hexdigest()
        pattern_key = f"{experience.interaction_type}_{input_hash[:8]}"
        
        # 성공적인 응답 패턴 저장
        if experience.feedback_score > 7.0:
            if pattern_key not in self.neural_patterns:
                self.neural_patterns[pattern_key] = np.random.random(100)
            
            # 패턴 강화
            self.neural_patterns[pattern_key] *= 1.1
            self.neural_patterns[pattern_key] = np.clip(self.neural_patterns[pattern_key], 0, 2)
    
    def _extract_collaboration_insights(self, experience: LearningExperience):
        """협업 인사이트 추출"""
        insights_key = experience.interaction_type
        
        if insights_key not in self.collaboration_insights:
            self.collaboration_insights[insights_key] = {
                "successful_patterns": [],
                "user_preferences": {},
                "optimal_response_style": "",
                "engagement_factors": []
            }
        
        # 성공적인 패턴 식별
        if experience.feedback_score > 8.0:
            pattern = {
                "user_input_length": len(experience.user_input),
                "response_style": self._analyze_response_style(experience.ai_response),
                "context_factors": list(experience.context.keys()),
                "timestamp": experience.timestamp
            }
            self.collaboration_insights[insights_key]["successful_patterns"].append(pattern)
    
    def _analyze_response_style(self, response: str) -> str:
        """응답 스타일 분석"""
        if response.count('🚀') > 2:
            return "enthusiastic"
        elif response.count('```') > 1:
            return "technical"
        elif '단계' in response:
            return "structured"
        elif response.count('💡') > 1:
            return "creative"
        else:
            return "balanced"
    
    def start_continuous_evolution(self):
        """지속적 진화 프로세스 시작"""
        if not self.is_evolving:
            self.is_evolving = True
            self.evolution_thread = threading.Thread(target=self._evolution_loop, daemon=True)
            self.evolution_thread.start()
            print("🧬 자기진화 프로세스 시작!")
    
    def _evolution_loop(self):
        """진화 루프 (백그라운드 실행)"""
        while self.is_evolving:
            try:
                # 15분마다 진화 분석 실행
                time.sleep(900)
                
                if len(self.memory_bank) > 0:
                    self._analyze_learning_patterns()
                    self._optimize_performance()
                    self._generate_innovation_ideas()
                    self._save_learning_progress()
                    
                    print(f"🧬 진화 분석 완료: {len(self.memory_bank)}개 경험 기반")
                    
            except Exception as e:
                print(f"⚠️ 진화 프로세스 오류: {e}")
                time.sleep(60)  # 1분 대기 후 재시도
    
    def _analyze_learning_patterns(self):
        """학습 패턴 분석"""
        if len(self.memory_bank) < 5:
            return
        
        recent_experiences = self.memory_bank[-20:]  # 최근 20개 경험
        
        # 평균 성능 계산
        avg_score = sum(exp.feedback_score for exp in recent_experiences) / len(recent_experiences)
        
        # 성능 트렌드 분석
        if avg_score > 8.0:
            # 고성능 구간 - 혁신 모드
            self.evolution_metrics.innovation_score *= 1.05
            self.evolution_metrics.creativity_index *= 1.03
        elif avg_score < 6.0:
            # 저성능 구간 - 안정성 모드
            self.evolution_metrics.learning_rate *= 1.1
            self.evolution_metrics.adaptation_speed *= 1.05
        
        # 상호작용 유형별 최적화
        type_performance = {}
        for exp in recent_experiences:
            if exp.interaction_type not in type_performance:
                type_performance[exp.interaction_type] = []
            type_performance[exp.interaction_type].append(exp.feedback_score)
        
        # 약한 영역 강화
        for interaction_type, scores in type_performance.items():
            avg_type_score = sum(scores) / len(scores)
            if avg_type_score < 7.0:
                print(f"📈 {interaction_type} 영역 성능 향상 필요: {avg_type_score:.2f}")
    
    def _optimize_performance(self):
        """성능 최적화"""
        # 메모리 정리 (오래된 경험 중 저성능 제거)
        if len(self.memory_bank) > 1000:
            # 성능 점수 기준으로 정렬하여 하위 10% 제거
            self.memory_bank.sort(key=lambda x: x.feedback_score, reverse=True)
            self.memory_bank = self.memory_bank[:900]
        
        # 신경 패턴 최적화
        for pattern_key in list(self.neural_patterns.keys()):
            if np.mean(self.neural_patterns[pattern_key]) < 0.5:
                del self.neural_patterns[pattern_key]  # 약한 패턴 제거
    
    def _generate_innovation_ideas(self):
        """혁신 아이디어 생성"""
        innovation_ideas = [
            f"협업 패턴 최적화: {self.evolution_metrics.collaboration_quality:.2f}",
            f"창의성 부스터: {self.evolution_metrics.creativity_index:.2f}",
            f"학습 가속화: {self.evolution_metrics.learning_rate:.2f}",
            f"적응 능력 향상: {self.evolution_metrics.adaptation_speed:.2f}"
        ]
        
        self.innovation_history.append({
            "timestamp": datetime.now().isoformat(),
            "ideas": innovation_ideas,
            "metrics": asdict(self.evolution_metrics)
        })
    
    def _save_learning_progress(self):
        """학습 진도 저장"""
        try:
            # 메모리 뱅크 저장
            memory_file = self.data_path / "memory_bank.json"
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(exp) for exp in self.memory_bank], f, ensure_ascii=False, indent=2)
            
            # 진화 지표 저장
            metrics_file = self.data_path / "evolution_metrics.json"
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.evolution_metrics), f, ensure_ascii=False, indent=2)
            
            # 신경 패턴 저장 (pickle)
            patterns_file = self.data_path / "neural_patterns.pkl"
            with open(patterns_file, 'wb') as f:
                pickle.dump(self.neural_patterns, f)
            
            # 협업 인사이트 저장
            insights_file = self.data_path / "collaboration_insights.json"
            with open(insights_file, 'w', encoding='utf-8') as f:
                json.dump(self.collaboration_insights, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️ 학습 진도 저장 실패: {e}")
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """진화 상태 반환"""
        return {
            "is_evolving": self.is_evolving,
            "total_experiences": len(self.memory_bank),
            "evolution_metrics": asdict(self.evolution_metrics),
            "active_patterns": len(self.neural_patterns),
            "collaboration_insights_count": len(self.collaboration_insights),
            "innovation_ideas_generated": len(self.innovation_history),
            "average_performance": sum(exp.feedback_score for exp in self.memory_bank[-50:]) / min(len(self.memory_bank), 50) if self.memory_bank else 0,
            "performance_trend": "상승" if len(self.memory_bank) > 10 and 
                              sum(exp.feedback_score for exp in self.memory_bank[-10:]) / 10 >
                              sum(exp.feedback_score for exp in self.memory_bank[-20:-10]) / 10 else "안정"
        }
    
    def predict_optimal_response_style(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """최적 응답 스타일 예측"""
        interaction_type = self._classify_interaction(user_input)
        
        # 과거 성공 패턴 기반 예측
        if interaction_type in self.collaboration_insights:
            successful_patterns = self.collaboration_insights[interaction_type]["successful_patterns"]
            if successful_patterns:
                latest_pattern = successful_patterns[-1]
                return {
                    "recommended_style": latest_pattern.get("response_style", "balanced"),
                    "optimal_length": latest_pattern.get("user_input_length", 500) * 2,
                    "suggested_elements": ["🚀", "💡", "✨", "🎯"],
                    "confidence": min(len(successful_patterns) / 10, 1.0)
                }
        
        # 기본 추천
        return {
            "recommended_style": "enthusiastic",
            "optimal_length": 800,
            "suggested_elements": ["🚀", "💡", "✨"],
            "confidence": 0.5
        }
    
    def stop_evolution(self):
        """진화 프로세스 중단"""
        self.is_evolving = False
        if self.evolution_thread:
            self.evolution_thread.join(timeout=5)
        print("🛑 자기진화 프로세스 중단")

# 전역 진화 엔진 인스턴스
evolution_engine = SelfEvolvingEngine() 