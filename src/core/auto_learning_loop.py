"""
🔄 Stein AI - 자동 학습 루프 시스템
사용자 피드백 기반 자동 개선 엔진
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# 설정
logger = logging.getLogger(__name__)

@dataclass
class FeedbackData:
    """피드백 데이터 구조"""
    user_id: str
    session_id: str
    question: str
    response: str
    rating: int  # 1-5 점수
    feedback_text: Optional[str]
    timestamp: datetime
    response_time: float
    question_quality_score: float
    improvement_suggestions: List[str]
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

@dataclass  
class LearningMetrics:
    """학습 메트릭 구조"""
    avg_rating: float
    response_time_trend: float
    question_quality_improvement: float
    user_satisfaction_trend: float
    learning_velocity: float
    confidence_score: float

class AutoLearningLoop:
    """자동 학습 루프 핵심 엔진"""
    
    def __init__(self, data_dir: str = "data/learning"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 학습 데이터 저장소
        self.feedback_storage = self.data_dir / "feedback.jsonl"
        self.learning_patterns = self.data_dir / "patterns.json"
        self.improvement_log = self.data_dir / "improvements.json"
        
        # 학습 상태
        self.learning_metrics = LearningMetrics(
            avg_rating=0.0,
            response_time_trend=0.0,
            question_quality_improvement=0.0,
            user_satisfaction_trend=0.0,
            learning_velocity=0.0,
            confidence_score=0.0
        )
        
        # 패턴 분석 결과
        self.learned_patterns = self._load_patterns()
        
        logger.info("🔄 자동 학습 루프 시스템 초기화 완료")

    def _load_patterns(self) -> Dict[str, Any]:
        """저장된 학습 패턴 로드"""
        try:
            if self.learning_patterns.exists():
                with open(self.learning_patterns, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"패턴 로드 실패: {e}")
        
        return {
            "question_patterns": {},
            "response_patterns": {},
            "user_preferences": {},
            "improvement_rules": []
        }

    def _save_patterns(self):
        """학습 패턴 저장"""
        try:
            with open(self.learning_patterns, 'w', encoding='utf-8') as f:
                json.dump(self.learned_patterns, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"패턴 저장 실패: {e}")

    async def collect_feedback(self, feedback: FeedbackData) -> bool:
        """피드백 수집 및 저장"""
        try:
            # 피드백 데이터 저장
            with open(self.feedback_storage, 'a', encoding='utf-8') as f:
                f.write(json.dumps(feedback.to_dict(), ensure_ascii=False) + '\n')
            
            # 실시간 학습 패턴 업데이트
            await self._update_learning_patterns(feedback)
            
            # 메트릭 업데이트
            await self._update_metrics()
            
            logger.info(f"✅ 피드백 수집 완료: {feedback.user_id}")
            return True
            
        except Exception as e:
            logger.error(f"피드백 수집 실패: {e}")
            return False

    async def _update_learning_patterns(self, feedback: FeedbackData):
        """학습 패턴 업데이트"""
        try:
            # 1. 질문 패턴 분석
            question_hash = hash(feedback.question)
            if str(question_hash) not in self.learned_patterns["question_patterns"]:
                self.learned_patterns["question_patterns"][str(question_hash)] = {
                    "question": feedback.question,
                    "ratings": [],
                    "response_times": [],
                    "quality_scores": []
                }
            
            pattern = self.learned_patterns["question_patterns"][str(question_hash)]
            pattern["ratings"].append(feedback.rating)
            pattern["response_times"].append(feedback.response_time)
            pattern["quality_scores"].append(feedback.question_quality_score)
            
            # 2. 응답 패턴 분석
            if feedback.rating >= 4:  # 좋은 응답 패턴 학습
                response_key = f"high_quality_{len(feedback.response)//100}"
                if response_key not in self.learned_patterns["response_patterns"]:
                    self.learned_patterns["response_patterns"][response_key] = []
                
                self.learned_patterns["response_patterns"][response_key].append({
                    "length": len(feedback.response),
                    "rating": feedback.rating,
                    "response_time": feedback.response_time,
                    "timestamp": feedback.timestamp.isoformat()
                })
            
            # 3. 사용자 선호도 학습
            if feedback.user_id not in self.learned_patterns["user_preferences"]:
                self.learned_patterns["user_preferences"][feedback.user_id] = {
                    "preferred_response_length": [],
                    "preferred_detail_level": [],
                    "satisfaction_history": []
                }
            
            user_pref = self.learned_patterns["user_preferences"][feedback.user_id]
            user_pref["preferred_response_length"].append(len(feedback.response))
            user_pref["satisfaction_history"].append(feedback.rating)
            
            # 패턴 저장
            self._save_patterns()
            
        except Exception as e:
            logger.error(f"패턴 업데이트 실패: {e}")

    async def _update_metrics(self):
        """학습 메트릭 업데이트"""
        try:
            # 최근 피드백 데이터 로드
            recent_feedback = self._load_recent_feedback(days=7)
            
            if not recent_feedback:
                return
            
            # 평균 평점
            ratings = [f.rating for f in recent_feedback]
            self.learning_metrics.avg_rating = sum(ratings) / len(ratings)
            
            # 응답 시간 트렌드
            response_times = [f.response_time for f in recent_feedback]
            self.learning_metrics.response_time_trend = self._calculate_trend(response_times)
            
            # 질문 품질 개선도
            quality_scores = [f.question_quality_score for f in recent_feedback]
            self.learning_metrics.question_quality_improvement = self._calculate_trend(quality_scores)
            
            # 사용자 만족도 트렌드
            self.learning_metrics.user_satisfaction_trend = self._calculate_trend(ratings)
            
            # 학습 속도
            self.learning_metrics.learning_velocity = self._calculate_learning_velocity()
            
            # 신뢰도 점수
            self.learning_metrics.confidence_score = self._calculate_confidence_score()
            
            logger.info(f"📊 메트릭 업데이트 완료: 평균 평점 {self.learning_metrics.avg_rating:.2f}")
            
        except Exception as e:
            logger.error(f"메트릭 업데이트 실패: {e}")

    def _load_recent_feedback(self, days: int = 7) -> List[FeedbackData]:
        """최근 피드백 데이터 로드"""
        try:
            if not self.feedback_storage.exists():
                return []
            
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_feedback = []
            
            with open(self.feedback_storage, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        timestamp = datetime.fromisoformat(data['timestamp'])
                        
                        if timestamp > cutoff_date:
                            feedback = FeedbackData(
                                user_id=data['user_id'],
                                session_id=data['session_id'],
                                question=data['question'],
                                response=data['response'],
                                rating=data['rating'],
                                feedback_text=data.get('feedback_text'),
                                timestamp=timestamp,
                                response_time=data['response_time'],
                                question_quality_score=data['question_quality_score'],
                                improvement_suggestions=data.get('improvement_suggestions', [])
                            )
                            recent_feedback.append(feedback)
                    except Exception as e:
                        logger.warning(f"피드백 파싱 실패: {e}")
            
            return recent_feedback
            
        except Exception as e:
            logger.error(f"피드백 로드 실패: {e}")
            return []

    def _calculate_trend(self, values: List[float]) -> float:
        """트렌드 계산 (간단한 선형 회귀)"""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * values[i] for i in range(n))
        sum_x_squared = sum(i * i for i in range(n))
        
        try:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x * sum_x)
            return slope
        except ZeroDivisionError:
            return 0.0

    def _calculate_learning_velocity(self) -> float:
        """학습 속도 계산"""
        try:
            pattern_count = len(self.learned_patterns["question_patterns"])
            improvement_count = len(self.learned_patterns["improvement_rules"])
            
            # 학습된 패턴 수와 개선 규칙 수를 기반으로 속도 계산
            velocity = (pattern_count * 0.7) + (improvement_count * 0.3)
            return min(velocity / 100, 1.0)  # 0-1 범위로 정규화
            
        except Exception:
            return 0.0

    def _calculate_confidence_score(self) -> float:
        """신뢰도 점수 계산"""
        try:
            # 평균 평점, 데이터 양, 트렌드를 종합한 신뢰도
            data_quality = min(self.learning_metrics.avg_rating / 5.0, 1.0)
            trend_stability = 1.0 - abs(self.learning_metrics.user_satisfaction_trend)
            
            confidence = (data_quality * 0.6) + (trend_stability * 0.4)
            return max(0.0, min(confidence, 1.0))
            
        except Exception:
            return 0.0

    async def get_improvement_suggestions(self, question: str, current_response: str) -> List[str]:
        """개선 제안 생성"""
        try:
            suggestions = []
            
            # 질문 패턴 기반 제안
            question_hash = str(hash(question))
            if question_hash in self.learned_patterns["question_patterns"]:
                pattern = self.learned_patterns["question_patterns"][question_hash]
                avg_rating = sum(pattern["ratings"]) / len(pattern["ratings"])
                
                if avg_rating < 3.5:
                    suggestions.append("🔄 이전 유사 질문의 평점이 낮습니다. 더 자세한 설명을 추가해보세요.")
                
                avg_response_time = sum(pattern["response_times"]) / len(pattern["response_times"])
                if avg_response_time > 5.0:
                    suggestions.append("⚡ 응답 시간을 단축하기 위해 핵심 내용을 먼저 제시하세요.")
            
            # 응답 길이 기반 제안
            response_length = len(current_response)
            if response_length < 100:
                suggestions.append("📝 더 자세한 설명과 예시를 추가하면 도움이 될 것 같습니다.")
            elif response_length > 2000:
                suggestions.append("✂️ 핵심 내용을 간결하게 정리하면 더 읽기 쉬울 것 같습니다.")
            
            # 개인화 제안
            suggestions.append("🎯 Stein님의 학습 스타일에 맞춰 코드 예시를 더 추가하는 것이 좋겠습니다.")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"개선 제안 생성 실패: {e}")
            return ["🔄 시스템을 개선하고 있습니다. 피드백을 주시면 더 나은 답변을 제공하겠습니다."]

    async def apply_learned_improvements(self, question: str) -> Dict[str, Any]:
        """학습된 개선사항 적용"""
        try:
            improvements = {
                "response_style": "detailed",
                "code_examples": True,
                "step_by_step": True,
                "korean_focus": True,
                "stein_personalization": True
            }
            
            # 사용자 선호도 반영
            if "stein" in self.learned_patterns["user_preferences"]:
                user_pref = self.learned_patterns["user_preferences"]["stein"]
                
                # 선호 응답 길이 계산
                if user_pref["preferred_response_length"]:
                    avg_length = sum(user_pref["preferred_response_length"]) / len(user_pref["preferred_response_length"])
                    if avg_length > 1000:
                        improvements["response_style"] = "very_detailed"
                    elif avg_length < 500:
                        improvements["response_style"] = "concise"
            
            # 질문 패턴 기반 개선
            question_hash = str(hash(question))
            if question_hash in self.learned_patterns["question_patterns"]:
                pattern = self.learned_patterns["question_patterns"][question_hash]
                avg_quality = sum(pattern["quality_scores"]) / len(pattern["quality_scores"])
                
                if avg_quality < 7.0:
                    improvements["quality_boost"] = True
                    improvements["additional_examples"] = True
            
            return improvements
            
        except Exception as e:
            logger.error(f"개선사항 적용 실패: {e}")
            return {"response_style": "detailed", "korean_focus": True}

    def get_learning_stats(self) -> Dict[str, Any]:
        """학습 통계 반환"""
        return {
            "learning_metrics": asdict(self.learning_metrics),
            "pattern_counts": {
                "question_patterns": len(self.learned_patterns["question_patterns"]),
                "response_patterns": len(self.learned_patterns["response_patterns"]),
                "user_preferences": len(self.learned_patterns["user_preferences"]),
                "improvement_rules": len(self.learned_patterns["improvement_rules"])
            },
            "system_health": {
                "status": "🚀 학습 중",
                "confidence": f"{self.learning_metrics.confidence_score:.1%}",
                "learning_rate": f"{self.learning_metrics.learning_velocity:.1%}",
                "user_satisfaction": f"{self.learning_metrics.avg_rating:.1f}/5.0"
            }
        }

# 전역 학습 루프 인스턴스
auto_learning_loop = AutoLearningLoop()

# 편의 함수들
async def collect_user_feedback(user_id: str, session_id: str, question: str, 
                               response: str, rating: int, feedback_text: str = None,
                               response_time: float = 0.0, quality_score: float = 0.0) -> bool:
    """사용자 피드백 수집"""
    feedback = FeedbackData(
        user_id=user_id,
        session_id=session_id,
        question=question,
        response=response,
        rating=rating,
        feedback_text=feedback_text,
        timestamp=datetime.now(),
        response_time=response_time,
        question_quality_score=quality_score,
        improvement_suggestions=[]
    )
    
    return await auto_learning_loop.collect_feedback(feedback)

async def get_smart_suggestions(question: str, response: str) -> List[str]:
    """스마트 개선 제안"""
    return await auto_learning_loop.get_improvement_suggestions(question, response)

async def apply_learning(question: str) -> Dict[str, Any]:
    """학습 내용 적용"""
    return await auto_learning_loop.apply_learned_improvements(question)

def get_learning_dashboard() -> Dict[str, Any]:
    """학습 대시보드 데이터"""
    return auto_learning_loop.get_learning_stats() 