"""
📈 Stein AI - 머신러닝 기반 예측 시스템
학습 패턴 분석 및 미래 성능 예측 엔진
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import json
import pickle

# 머신러닝 라이브러리
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# 설정
logger = logging.getLogger(__name__)

@dataclass
class PredictionResult:
    """예측 결과 구조"""
    metric_name: str
    current_value: float
    predicted_value: float
    confidence: float
    prediction_horizon: str  # "1일", "1주", "1개월"
    improvement_probability: float
    trend_direction: str  # "상승", "하락", "안정"
    key_factors: List[str]

@dataclass
class LearningPattern:
    """학습 패턴 구조"""
    user_id: str
    pattern_type: str  # "시간대", "주제", "난이도" 등
    pattern_data: Dict[str, Any]
    frequency: int
    effectiveness_score: float
    last_updated: datetime

class MLPredictionEngine:
    """머신러닝 기반 예측 엔진"""
    
    def __init__(self, model_dir: str = "data/ml_models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # 모델 저장소
        self.models = {
            'performance_predictor': None,
            'satisfaction_classifier': None,
            'pattern_clusterer': None,
            'trend_analyzer': None
        }
        
        # 데이터 전처리기
        self.scalers = {
            'features': StandardScaler(),
            'targets': StandardScaler()
        }
        
        self.label_encoders = {}
        
        # 학습 패턴 저장소
        self.learning_patterns = []
        
        logger.info("🤖 ML 예측 엔진 초기화 완료")

    def prepare_training_data(self, feedback_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """학습 데이터 준비 및 전처리"""
        try:
            if not feedback_data:
                logger.warning("피드백 데이터가 없습니다")
                return np.array([]), np.array([])
            
            # DataFrame 생성
            df = pd.DataFrame(feedback_data)
            
            # 시계열 특성 추출
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['day_of_month'] = df['timestamp'].dt.day
            
            # 텍스트 특성 추출
            df['question_length'] = df['question'].str.len()
            df['response_length'] = df['response'].str.len()
            df['has_code'] = df['question'].str.contains(r'```|def |class |import ', regex=True)
            df['question_marks'] = df['question'].str.count(r'\?')
            df['exclamation_marks'] = df['question'].str.count(r'!')
            
            # 사용자 행동 특성
            df['response_efficiency'] = df['response_length'] / (df['response_time'] + 1)
            df['quality_to_rating_ratio'] = df['quality_score'] / (df['rating'] + 0.1)
            
            # 특성 선택
            feature_columns = [
                'hour', 'day_of_week', 'day_of_month',
                'question_length', 'response_length', 'has_code',
                'question_marks', 'exclamation_marks',
                'response_time', 'quality_score',
                'response_efficiency', 'quality_to_rating_ratio'
            ]
            
            # 결측값 처리
            for col in feature_columns:
                if col in df.columns:
                    df[col] = df[col].fillna(df[col].mean() if df[col].dtype in ['int64', 'float64'] else 0)
            
            # 특성 매트릭스 구성
            X = df[feature_columns].values
            y = df['rating'].values
            
            # 데이터 정규화
            X_scaled = self.scalers['features'].fit_transform(X)
            
            return X_scaled, y
            
        except Exception as e:
            logger.error(f"학습 데이터 준비 실패: {e}")
            return np.array([]), np.array([])

    def train_performance_predictor(self, feedback_data: List[Dict]) -> Dict[str, float]:
        """성능 예측 모델 학습"""
        try:
            X, y = self.prepare_training_data(feedback_data)
            
            if len(X) < 5:  # 최소 데이터 요구량
                logger.warning("학습 데이터가 부족합니다")
                return {"accuracy": 0.0, "mse": 0.0}
            
            # 데이터 분할
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # 랜덤 포레스트 회귀 모델 학습
            self.models['performance_predictor'] = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            self.models['performance_predictor'].fit(X_train, y_train)
            
            # 모델 평가
            y_pred = self.models['performance_predictor'].predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            
            # 교차 검증
            cv_scores = cross_val_score(
                self.models['performance_predictor'], X, y, 
                cv=min(5, len(X)//2), scoring='neg_mean_squared_error'
            )
            
            accuracy = 1 - np.sqrt(-cv_scores.mean()) / 5.0  # 5점 척도 기준
            
            # 모델 저장
            self._save_model('performance_predictor')
            
            logger.info(f"성능 예측 모델 학습 완료 - 정확도: {accuracy:.3f}")
            
            return {
                "accuracy": float(accuracy),
                "mse": float(mse),
                "cv_mean": float(-cv_scores.mean()),
                "cv_std": float(cv_scores.std())
            }
            
        except Exception as e:
            logger.error(f"성능 예측 모델 학습 실패: {e}")
            return {"accuracy": 0.0, "mse": float('inf')}

    def train_satisfaction_classifier(self, feedback_data: List[Dict]) -> Dict[str, float]:
        """만족도 분류 모델 학습"""
        try:
            X, y = self.prepare_training_data(feedback_data)
            
            if len(X) < 5:
                return {"accuracy": 0.0}
            
            # 만족도를 3단계로 분류 (1-2: 낮음, 3: 보통, 4-5: 높음)
            y_categorical = np.where(y <= 2, 0, np.where(y <= 3, 1, 2))
            
            # 데이터 분할
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_categorical, test_size=0.2, random_state=42, stratify=y_categorical
            )
            
            # 그라디언트 부스팅 분류기 학습
            self.models['satisfaction_classifier'] = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            
            self.models['satisfaction_classifier'].fit(X_train, y_train)
            
            # 모델 평가
            y_pred = self.models['satisfaction_classifier'].predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # 모델 저장
            self._save_model('satisfaction_classifier')
            
            logger.info(f"만족도 분류 모델 학습 완료 - 정확도: {accuracy:.3f}")
            
            return {"accuracy": float(accuracy)}
            
        except Exception as e:
            logger.error(f"만족도 분류 모델 학습 실패: {e}")
            return {"accuracy": 0.0}

    def train_pattern_clusterer(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """학습 패턴 클러스터링 모델 학습"""
        try:
            X, _ = self.prepare_training_data(feedback_data)
            
            if len(X) < 3:
                return {"clusters": 0, "inertia": float('inf')}
            
            # 최적 클러스터 수 결정 (엘보우 방법 간소화)
            max_clusters = min(5, len(X) // 2)
            inertias = []
            
            for k in range(1, max_clusters + 1):
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(X)
                inertias.append(kmeans.inertia_)
            
            # 최적 클러스터 수 선택 (간단한 휴리스틱)
            optimal_k = min(3, max_clusters)
            
            # K-means 클러스터링
            self.models['pattern_clusterer'] = KMeans(
                n_clusters=optimal_k, 
                random_state=42, 
                n_init=10
            )
            
            cluster_labels = self.models['pattern_clusterer'].fit_predict(X)
            
            # 클러스터 분석
            cluster_info = {}
            for i in range(optimal_k):
                mask = cluster_labels == i
                if np.sum(mask) > 0:
                    cluster_info[f"cluster_{i}"] = {
                        "size": int(np.sum(mask)),
                        "centroid": self.models['pattern_clusterer'].cluster_centers_[i].tolist()
                    }
            
            # 모델 저장
            self._save_model('pattern_clusterer')
            
            logger.info(f"패턴 클러스터링 완료 - {optimal_k}개 클러스터")
            
            return {
                "clusters": optimal_k,
                "inertia": float(self.models['pattern_clusterer'].inertia_),
                "cluster_info": cluster_info
            }
            
        except Exception as e:
            logger.error(f"패턴 클러스터링 실패: {e}")
            return {"clusters": 0, "inertia": float('inf')}

    def predict_future_performance(self, current_features: Dict[str, Any], 
                                 horizon_days: int = 7) -> List[PredictionResult]:
        """미래 성능 예측"""
        try:
            predictions = []
            
            if self.models['performance_predictor'] is None:
                logger.warning("성능 예측 모델이 학습되지 않았습니다")
                return predictions
            
            # 현재 특성을 모델 입력 형태로 변환
            feature_vector = self._extract_features_from_dict(current_features)
            feature_vector_scaled = self.scalers['features'].transform([feature_vector])
            
            # 기본 예측
            base_prediction = self.models['performance_predictor'].predict(feature_vector_scaled)[0]
            
            # 시간대별 예측 (1일, 1주, 1개월)
            horizons = [
                (1, "1일"),
                (7, "1주"), 
                (30, "1개월")
            ]
            
            for days, label in horizons:
                # 시간 경과에 따른 특성 변화 시뮬레이션
                future_features = feature_vector.copy()
                
                # 학습 효과 반영 (시간이 지날수록 개선)
                learning_factor = 1 + (days * 0.01)  # 1% per day
                future_features[3] *= learning_factor  # 질문 품질 개선
                
                # 특성 정규화
                future_features_scaled = self.scalers['features'].transform([future_features])
                
                # 예측 실행
                predicted_rating = self.models['performance_predictor'].predict(future_features_scaled)[0]
                
                # 신뢰도 계산 (앙상블 예측의 분산 기반)
                if hasattr(self.models['performance_predictor'], 'estimators_'):
                    predictions_ensemble = [
                        estimator.predict(future_features_scaled)[0] 
                        for estimator in self.models['performance_predictor'].estimators_[:10]
                    ]
                    confidence = 1.0 - (np.std(predictions_ensemble) / 5.0)
                else:
                    confidence = 0.7  # 기본값
                
                # 개선 확률 계산
                improvement_prob = max(0.0, min(1.0, (predicted_rating - base_prediction + 2) / 4))
                
                # 트렌드 방향
                if predicted_rating > base_prediction + 0.1:
                    trend = "상승"
                elif predicted_rating < base_prediction - 0.1:
                    trend = "하락"
                else:
                    trend = "안정"
                
                # 주요 영향 요인 (특성 중요도 기반)
                if hasattr(self.models['performance_predictor'], 'feature_importances_'):
                    feature_names = [
                        'hour', 'day_of_week', 'day_of_month',
                        'question_length', 'response_length', 'has_code',
                        'question_marks', 'exclamation_marks',
                        'response_time', 'quality_score',
                        'response_efficiency', 'quality_to_rating_ratio'
                    ]
                    
                    importances = self.models['performance_predictor'].feature_importances_
                    top_factors = [
                        feature_names[i] for i in np.argsort(importances)[-3:][::-1]
                    ]
                else:
                    top_factors = ["질문_품질", "응답_시간", "학습_패턴"]
                
                prediction = PredictionResult(
                    metric_name=f"예상_만족도_{label}",
                    current_value=float(base_prediction),
                    predicted_value=float(predicted_rating),
                    confidence=float(max(0.0, min(1.0, confidence))),
                    prediction_horizon=label,
                    improvement_probability=float(improvement_prob),
                    trend_direction=trend,
                    key_factors=top_factors
                )
                
                predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            logger.error(f"미래 성능 예측 실패: {e}")
            return []

    def analyze_learning_patterns(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """학습 패턴 종합 분석"""
        try:
            if not feedback_data:
                return {"patterns": [], "insights": []}
            
            df = pd.DataFrame(feedback_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            patterns = {}
            
            # 1. 시간대별 패턴 분석
            df['hour'] = df['timestamp'].dt.hour
            hourly_performance = df.groupby('hour')['rating'].mean()
            best_hours = hourly_performance.nlargest(3).index.tolist()
            
            patterns['time_pattern'] = {
                "type": "시간대별_성능",
                "best_hours": [int(h) for h in best_hours],
                "performance_by_hour": hourly_performance.to_dict(),
                "insight": f"가장 좋은 성과를 내는 시간: {', '.join([f'{h}시' for h in best_hours])}"
            }
            
            # 2. 주제별 패턴 분석
            df['has_code'] = df['question'].str.contains(r'```|def |class |import ', regex=True)
            df['is_conceptual'] = df['question'].str.contains(r'개념|이론|원리|개념|설명', regex=True)
            df['is_troubleshooting'] = df['question'].str.contains(r'오류|에러|문제|오류|디버깅', regex=True)
            
            topic_performance = {
                "코딩": df[df['has_code']]['rating'].mean() if df['has_code'].any() else 0,
                "개념": df[df['is_conceptual']]['rating'].mean() if df['is_conceptual'].any() else 0,
                "문제해결": df[df['is_troubleshooting']]['rating'].mean() if df['is_troubleshooting'].any() else 0
            }
            
            best_topic = max(topic_performance.items(), key=lambda x: x[1])
            
            patterns['topic_pattern'] = {
                "type": "주제별_성능",
                "performance_by_topic": topic_performance,
                "strongest_area": best_topic[0],
                "insight": f"가장 강한 영역: {best_topic[0]} (평점 {best_topic[1]:.1f})"
            }
            
            # 3. 학습 진화 패턴
            df_sorted = df.sort_values('timestamp')
            df_sorted['rolling_avg'] = df_sorted['rating'].rolling(window=5, min_periods=1).mean()
            
            recent_avg = df_sorted['rolling_avg'].tail(5).mean()
            early_avg = df_sorted['rolling_avg'].head(5).mean()
            improvement_rate = (recent_avg - early_avg) / max(early_avg, 0.1)
            
            patterns['evolution_pattern'] = {
                "type": "학습_진화",
                "improvement_rate": float(improvement_rate),
                "recent_performance": float(recent_avg),
                "early_performance": float(early_avg),
                "insight": f"학습 진화율: {improvement_rate*100:.1f}% {'개선' if improvement_rate > 0 else '안정'}"
            }
            
            # 인사이트 생성
            insights = [
                f"📈 전체 학습 세션: {len(df)}회",
                f"⭐ 평균 만족도: {df['rating'].mean():.1f}/5.0",
                f"🎯 {patterns['topic_pattern']['strongest_area']} 영역에서 뛰어남",
                f"⏰ {patterns['time_pattern']['best_hours'][0]}시 경에 최고 성과",
                f"📊 지속적인 {'개선' if improvement_rate > 0.05 else '안정적 성과'} 추세"
            ]
            
            return {
                "patterns": patterns,
                "insights": insights,
                "total_sessions": len(df),
                "average_rating": float(df['rating'].mean()),
                "improvement_trend": "positive" if improvement_rate > 0.05 else "stable"
            }
            
        except Exception as e:
            logger.error(f"학습 패턴 분석 실패: {e}")
            return {"patterns": {}, "insights": []}

    def get_ai_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """AI 기반 개선 추천"""
        try:
            recommendations = []
            
            if 'patterns' in analysis_results:
                patterns = analysis_results['patterns']
                
                # 시간대 최적화 추천
                if 'time_pattern' in patterns:
                    best_hours = patterns['time_pattern']['best_hours']
                    recommendations.append(
                        f"🕒 최적 학습 시간: {', '.join([f'{h}시' for h in best_hours[:2]])}에 중요한 학습 세션을 배치하세요"
                    )
                
                # 주제별 강화 추천
                if 'topic_pattern' in patterns:
                    strongest = patterns['topic_pattern']['strongest_area']
                    recommendations.append(
                        f"💪 강점 활용: {strongest} 영역의 장점을 다른 영역에도 적용해보세요"
                    )
                
                # 학습 진화 기반 추천
                if 'evolution_pattern' in patterns:
                    improvement_rate = patterns['evolution_pattern']['improvement_rate']
                    if improvement_rate > 0.1:
                        recommendations.append("🚀 훌륭한 성장세! 현재 학습 방식을 유지하세요")
                    elif improvement_rate < -0.05:
                        recommendations.append("🔄 학습 방식 변화가 필요할 수 있습니다")
                    else:
                        recommendations.append("📈 안정적 성과! 새로운 도전을 시도해보세요")
            
            # 일반적인 AI 추천
            recommendations.extend([
                "🎯 질문을 더 구체적으로 작성하면 더 나은 답변을 받을 수 있습니다",
                "📚 정기적인 피드백 제공으로 AI 성능을 지속적으로 개선하세요",
                "🧠 다양한 주제로 질문하여 AI의 학습 범위를 확장하세요"
            ])
            
            return recommendations[:5]  # 최대 5개 추천
            
        except Exception as e:
            logger.error(f"AI 추천 생성 실패: {e}")
            return ["🤖 AI가 지속적으로 학습하여 더 나은 추천을 제공할 예정입니다"]

    def _extract_features_from_dict(self, feature_dict: Dict[str, Any]) -> List[float]:
        """딕셔너리에서 특성 벡터 추출"""
        try:
            # 기본값 설정
            now = datetime.now()
            
            features = [
                feature_dict.get('hour', now.hour),
                feature_dict.get('day_of_week', now.weekday()),
                feature_dict.get('day_of_month', now.day),
                feature_dict.get('question_length', 100),
                feature_dict.get('response_length', 500),
                1 if feature_dict.get('has_code', False) else 0,
                feature_dict.get('question_marks', 1),
                feature_dict.get('exclamation_marks', 0),
                feature_dict.get('response_time', 3.0),
                feature_dict.get('quality_score', 7.0),
                feature_dict.get('response_efficiency', 166.7),
                feature_dict.get('quality_to_rating_ratio', 1.75)
            ]
            
            return features
            
        except Exception as e:
            logger.error(f"특성 추출 실패: {e}")
            return [0.0] * 12  # 기본 특성 벡터

    def _save_model(self, model_name: str):
        """모델 저장"""
        try:
            if model_name in self.models and self.models[model_name] is not None:
                model_path = self.model_dir / f"{model_name}.pkl"
                with open(model_path, 'wb') as f:
                    pickle.dump(self.models[model_name], f)
                logger.info(f"모델 저장 완료: {model_name}")
        except Exception as e:
            logger.error(f"모델 저장 실패 {model_name}: {e}")

    def _load_model(self, model_name: str):
        """모델 로드"""
        try:
            model_path = self.model_dir / f"{model_name}.pkl"
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    self.models[model_name] = pickle.load(f)
                logger.info(f"모델 로드 완료: {model_name}")
                return True
        except Exception as e:
            logger.error(f"모델 로드 실패 {model_name}: {e}")
        return False

    def get_model_status(self) -> Dict[str, Any]:
        """모델 상태 확인"""
        status = {}
        for model_name in self.models:
            status[model_name] = {
                "trained": self.models[model_name] is not None,
                "file_exists": (self.model_dir / f"{model_name}.pkl").exists()
            }
        return status

# 전역 ML 예측 엔진 인스턴스
ml_prediction_engine = MLPredictionEngine()

# 편의 함수들
async def train_all_models(feedback_data: List[Dict]) -> Dict[str, Any]:
    """모든 ML 모델 학습"""
    try:
        if not feedback_data:
            return {"error": "학습 데이터가 없습니다"}
        
        results = {}
        
        # 성능 예측 모델 학습
        perf_result = ml_prediction_engine.train_performance_predictor(feedback_data)
        results['performance_predictor'] = perf_result
        
        # 만족도 분류 모델 학습
        sat_result = ml_prediction_engine.train_satisfaction_classifier(feedback_data)
        results['satisfaction_classifier'] = sat_result
        
        # 패턴 클러스터링 모델 학습
        cluster_result = ml_prediction_engine.train_pattern_clusterer(feedback_data)
        results['pattern_clusterer'] = cluster_result
        
        # 전체 성공 여부
        results['overall_success'] = all([
            perf_result.get('accuracy', 0) > 0.3,
            sat_result.get('accuracy', 0) > 0.3,
            cluster_result.get('clusters', 0) > 0
        ])
        
        return results
        
    except Exception as e:
        logger.error(f"모델 학습 실패: {e}")
        return {"error": str(e)}

async def get_performance_predictions(current_state: Dict[str, Any]) -> List[PredictionResult]:
    """성능 예측 수행"""
    return ml_prediction_engine.predict_future_performance(current_state)

async def analyze_learning_insights(feedback_data: List[Dict]) -> Dict[str, Any]:
    """학습 인사이트 분석"""
    analysis = ml_prediction_engine.analyze_learning_patterns(feedback_data)
    recommendations = ml_prediction_engine.get_ai_recommendations(analysis)
    
    return {
        **analysis,
        "ai_recommendations": recommendations
    }

def get_ml_system_status() -> Dict[str, Any]:
    """ML 시스템 상태"""
    return ml_prediction_engine.get_model_status() 