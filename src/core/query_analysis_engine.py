import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
from dataclasses import dataclass
from enum import Enum

class QueryType(Enum):
    """질문 유형 분류"""
    TECHNICAL = "technical"
    BUSINESS = "business"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    PERSONAL = "personal"
    COMPLEX = "complex"

class DataSource(Enum):
    """데이터 소스 유형"""
    INTERNAL = "internal"
    EXTERNAL = "external"
    CACHED = "cached"
    REALTIME = "realtime"

@dataclass
class QueryAnalysis:
    """질문 분석 결과"""
    query_type: QueryType
    intent: str
    entities: List[str]
    context: Dict[str, Any]
    priority: int
    complexity: float
    data_requirements: List[str]
    suggested_sources: List[DataSource]

@dataclass
class DataApplication:
    """데이터 적용 결과"""
    source: DataSource
    data: Dict[str, Any]
    relevance_score: float
    applied_at: datetime
    transformations: List[str]

class QueryAnalysisEngine:
    """🧠 고급 질문 분석 및 데이터 적용 엔진"""
    
    def __init__(self):
        self.knowledge_base = {}
        self.query_history = []
        self.context_memory = {}
        self.data_cache = {}
        self.learning_patterns = {}
        
    def analyze_query(self, query: str, user_context: Dict[str, Any] = None) -> QueryAnalysis:
        """🔍 질문 심층 분석"""
        
        # 1. 의도 분석 (Intent Analysis)
        intent = self._extract_intent(query)
        
        # 2. 개체명 인식 (Named Entity Recognition)
        entities = self._extract_entities(query)
        
        # 3. 질문 유형 분류
        query_type = self._classify_query_type(query, entities)
        
        # 4. 컨텍스트 분석
        context = self._analyze_context(query, user_context)
        
        # 5. 복잡도 계산
        complexity = self._calculate_complexity(query, entities)
        
        # 6. 우선순위 설정
        priority = self._calculate_priority(query_type, complexity, context)
        
        # 7. 데이터 요구사항 분석
        data_requirements = self._analyze_data_requirements(query, entities)
        
        # 8. 데이터 소스 제안
        suggested_sources = self._suggest_data_sources(data_requirements, context)
        
        analysis = QueryAnalysis(
            query_type=query_type,
            intent=intent,
            entities=entities,
            context=context,
            priority=priority,
            complexity=complexity,
            data_requirements=data_requirements,
            suggested_sources=suggested_sources
        )
        
        # 히스토리에 저장
        self.query_history.append({
            'query': query,
            'analysis': analysis,
            'timestamp': datetime.now()
        })
        
        return analysis
    
    def apply_data_mechanism(self, analysis: QueryAnalysis, available_data: Dict[str, Any]) -> List[DataApplication]:
        """⚙️ 데이터 적용 메커니즘"""
        
        applications = []
        
        for source in analysis.suggested_sources:
            # 데이터 매칭
            matched_data = self._match_data(analysis.data_requirements, available_data, source)
            
            if matched_data:
                # 관련성 점수 계산
                relevance_score = self._calculate_relevance(analysis, matched_data)
                
                # 데이터 변환
                transformed_data, transformations = self._transform_data(matched_data, analysis)
                
                application = DataApplication(
                    source=source,
                    data=transformed_data,
                    relevance_score=relevance_score,
                    applied_at=datetime.now(),
                    transformations=transformations
                )
                
                applications.append(application)
        
        return applications
    
    def _extract_intent(self, query: str) -> str:
        """의도 추출 알고리즘"""
        intent_patterns = {
            'create': r'만들|생성|구현|개발|제작',
            'analyze': r'분석|검토|평가|조사',
            'improve': r'개선|향상|업그레이드|최적화',
            'explain': r'설명|어떻게|왜|방법',
            'compare': r'비교|차이|vs|대비',
            'predict': r'예측|전망|미래|예상',
            'learn': r'학습|배우|알고 싶|궁금',
            'solve': r'해결|문제|오류|디버깅'
        }
        
        for intent, pattern in intent_patterns.items():
            if re.search(pattern, query):
                return intent
        
        return 'general'
    
    def _extract_entities(self, query: str) -> List[str]:
        """개체명 인식"""
        entities = []
        
        # 기술 용어 추출
        tech_patterns = [
            r'AI|인공지능|머신러닝|딥러닝',
            r'Python|JavaScript|React|FastAPI',
            r'알고리즘|메커니즘|시스템|엔진',
            r'API|데이터베이스|서버|클라우드'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            entities.extend(matches)
        
        # 비즈니스 용어 추출
        business_patterns = [
            r'비즈니스|사업|수익|매출|고객',
            r'마케팅|판매|홍보|브랜딩',
            r'의뢰|프로젝트|서비스|솔루션'
        ]
        
        for pattern in business_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            entities.extend(matches)
        
        return list(set(entities))
    
    def _classify_query_type(self, query: str, entities: List[str]) -> QueryType:
        """질문 유형 분류"""
        
        # 기술적 질문
        if any(word in query for word in ['코드', '알고리즘', '구현', '디버깅', '성능']):
            return QueryType.TECHNICAL
        
        # 비즈니스 질문
        if any(word in query for word in ['비즈니스', '사업', '수익', '의뢰', '고객']):
            return QueryType.BUSINESS
        
        # 창의적 질문
        if any(word in query for word in ['아이디어', '창의', '혁신', '새로운']):
            return QueryType.CREATIVE
        
        # 분석적 질문
        if any(word in query for word in ['분석', '비교', '평가', '통계']):
            return QueryType.ANALYTICAL
        
        # 개인적 질문
        if any(word in query for word in ['내가', '나의', '개인', '맞춤']):
            return QueryType.PERSONAL
        
        # 복합적 질문 (여러 주제가 섞임)
        if len(entities) > 5 or '그리고' in query:
            return QueryType.COMPLEX
        
        return QueryType.TECHNICAL
    
    def _analyze_context(self, query: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """컨텍스트 분석"""
        context = {
            'user_context': user_context or {},
            'query_length': len(query),
            'question_count': query.count('?'),
            'urgency_indicators': self._detect_urgency(query),
            'emotional_tone': self._detect_emotion(query),
            'technical_level': self._assess_technical_level(query)
        }
        
        return context
    
    def _detect_urgency(self, query: str) -> List[str]:
        """긴급도 탐지"""
        urgency_words = ['급해', '빨리', '즉시', '지금', '당장', '오늘']
        return [word for word in urgency_words if word in query]
    
    def _detect_emotion(self, query: str) -> str:
        """감정 탐지"""
        positive_words = ['좋아', '최고', '훌륭', '감사', '고마워']
        negative_words = ['문제', '안돼', '어려워', '힘들어', '걱정']
        
        positive_count = sum(1 for word in positive_words if word in query)
        negative_count = sum(1 for word in negative_words if word in query)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _assess_technical_level(self, query: str) -> str:
        """기술적 수준 평가"""
        basic_terms = ['만들어', '어떻게', '방법', '쉽게']
        advanced_terms = ['알고리즘', '메커니즘', '아키텍처', '최적화', '리팩토링']
        
        if any(term in query for term in advanced_terms):
            return 'advanced'
        elif any(term in query for term in basic_terms):
            return 'basic'
        else:
            return 'intermediate'
    
    def _calculate_complexity(self, query: str, entities: List[str]) -> float:
        """복잡도 계산"""
        factors = {
            'length': len(query) / 1000,  # 문장 길이
            'entities': len(entities) / 10,  # 개체 수
            'questions': query.count('?') / 5,  # 질문 수
            'conjunctions': len(re.findall(r'그리고|또한|그런데|하지만', query)) / 3  # 접속사
        }
        
        complexity = sum(factors.values())
        return min(complexity, 1.0)  # 0-1 범위로 정규화
    
    def _calculate_priority(self, query_type: QueryType, complexity: float, context: Dict[str, Any]) -> int:
        """우선순위 계산"""
        base_priority = {
            QueryType.TECHNICAL: 8,
            QueryType.BUSINESS: 7,
            QueryType.CREATIVE: 6,
            QueryType.ANALYTICAL: 7,
            QueryType.PERSONAL: 9,
            QueryType.COMPLEX: 8
        }
        
        priority = base_priority.get(query_type, 5)
        
        # 긴급도 반영
        if context.get('urgency_indicators'):
            priority += 2
        
        # 복잡도 반영
        priority += int(complexity * 3)
        
        return min(priority, 10)
    
    def _analyze_data_requirements(self, query: str, entities: List[str]) -> List[str]:
        """데이터 요구사항 분석"""
        requirements = []
        
        # 기술 데이터
        if any(word in query for word in ['코드', '알고리즘', '구현']):
            requirements.extend(['code_examples', 'best_practices', 'documentation'])
        
        # 비즈니스 데이터
        if any(word in query for word in ['비즈니스', '시장', '수익']):
            requirements.extend(['market_data', 'business_metrics', 'case_studies'])
        
        # 성능 데이터
        if any(word in query for word in ['성능', '최적화', '속도']):
            requirements.extend(['performance_metrics', 'benchmarks', 'optimization_tips'])
        
        return requirements
    
    def _suggest_data_sources(self, requirements: List[str], context: Dict[str, Any]) -> List[DataSource]:
        """데이터 소스 제안"""
        sources = []
        
        if 'code_examples' in requirements:
            sources.append(DataSource.INTERNAL)
        
        if 'market_data' in requirements:
            sources.append(DataSource.EXTERNAL)
        
        if context.get('technical_level') == 'advanced':
            sources.append(DataSource.REALTIME)
        
        sources.append(DataSource.CACHED)  # 기본적으로 캐시 사용
        
        return list(set(sources))
    
    def _match_data(self, requirements: List[str], available_data: Dict[str, Any], source: DataSource) -> Dict[str, Any]:
        """데이터 매칭"""
        matched = {}
        
        for req in requirements:
            if req in available_data:
                matched[req] = available_data[req]
        
        return matched
    
    def _calculate_relevance(self, analysis: QueryAnalysis, data: Dict[str, Any]) -> float:
        """관련성 점수 계산"""
        # 간단한 관련성 점수 계산
        relevance = 0.0
        
        # 데이터 항목 수에 따른 점수
        relevance += min(len(data) / 10, 0.5)
        
        # 질문 유형에 따른 가중치
        type_weights = {
            QueryType.TECHNICAL: 0.9,
            QueryType.BUSINESS: 0.8,
            QueryType.CREATIVE: 0.7,
            QueryType.ANALYTICAL: 0.9,
            QueryType.PERSONAL: 0.8,
            QueryType.COMPLEX: 0.7
        }
        
        relevance += type_weights.get(analysis.query_type, 0.5)
        
        return min(relevance, 1.0)
    
    def _transform_data(self, data: Dict[str, Any], analysis: QueryAnalysis) -> Tuple[Dict[str, Any], List[str]]:
        """데이터 변환"""
        transformed = data.copy()
        transformations = []
        
        # 질문 유형에 따른 변환
        if analysis.query_type == QueryType.TECHNICAL:
            # 기술적 데이터 강화
            transformations.append('technical_enhancement')
        
        if analysis.query_type == QueryType.BUSINESS:
            # 비즈니스 메트릭 추가
            transformations.append('business_metrics_addition')
        
        return transformed, transformations
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """학습 인사이트 제공"""
        if not self.query_history:
            return {}
        
        # 질문 패턴 분석
        query_types = [h['analysis'].query_type.value for h in self.query_history]
        most_common_type = max(set(query_types), key=query_types.count)
        
        # 복잡도 트렌드
        complexities = [h['analysis'].complexity for h in self.query_history]
        avg_complexity = sum(complexities) / len(complexities)
        
        return {
            'total_queries': len(self.query_history),
            'most_common_type': most_common_type,
            'average_complexity': avg_complexity,
            'learning_patterns': self.learning_patterns,
            'improvement_suggestions': self._generate_improvement_suggestions()
        }
    
    def _generate_improvement_suggestions(self) -> List[str]:
        """개선 제안 생성"""
        suggestions = []
        
        if self.query_history:
            recent_queries = self.query_history[-5:]
            
            # 복잡한 질문이 많으면 단순화 제안
            if sum(h['analysis'].complexity for h in recent_queries) / len(recent_queries) > 0.7:
                suggestions.append("질문을 더 구체적으로 나누어 물어보시면 더 정확한 답변을 드릴 수 있습니다.")
            
            # 기술적 질문이 많으면 문서화 제안
            tech_count = sum(1 for h in recent_queries if h['analysis'].query_type == QueryType.TECHNICAL)
            if tech_count > 3:
                suggestions.append("기술 문서를 체계적으로 정리해두시면 더 효율적인 개발이 가능합니다.")
        
        return suggestions 