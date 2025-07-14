from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import uuid

class ProjectStatus(Enum):
    """프로젝트 상태"""
    INQUIRY = "inquiry"              # 문의
    ANALYSIS = "analysis"            # 요구사항 분석
    PROPOSAL = "proposal"            # 제안서 작성
    NEGOTIATION = "negotiation"      # 협상
    CONTRACT = "contract"            # 계약
    DEVELOPMENT = "development"      # 개발
    TESTING = "testing"              # 테스트
    DELIVERY = "delivery"            # 인도
    MAINTENANCE = "maintenance"      # 유지보수
    COMPLETED = "completed"          # 완료

class AIType(Enum):
    """AI 유형"""
    CHATBOT = "chatbot"              # 챗봇
    ANALYSIS = "analysis"            # 분석 AI
    AUTOMATION = "automation"        # 자동화 AI
    RECOMMENDATION = "recommendation" # 추천 AI
    PREDICTION = "prediction"        # 예측 AI
    CREATIVE = "creative"            # 창작 AI
    CUSTOM = "custom"                # 맞춤형

class ComplexityLevel(Enum):
    """복잡도 수준"""
    BASIC = "basic"                  # 기본
    INTERMEDIATE = "intermediate"    # 중급
    ADVANCED = "advanced"            # 고급
    ENTERPRISE = "enterprise"        # 엔터프라이즈

@dataclass
class CustomerRequirement:
    """고객 요구사항"""
    customer_id: str
    customer_name: str
    company: str
    contact_info: str
    ai_type: AIType
    complexity_level: ComplexityLevel
    description: str
    specific_features: List[str]
    target_users: str
    budget_range: str
    timeline: str
    success_criteria: List[str]
    additional_notes: str

@dataclass
class ProjectEstimate:
    """프로젝트 견적"""
    project_id: str
    development_cost: float
    maintenance_cost: float
    total_cost: float
    estimated_hours: int
    timeline_weeks: int
    team_size: int
    technologies: List[str]
    deliverables: List[str]
    risk_factors: List[str]
    assumptions: List[str]

@dataclass
class Project:
    """프로젝트"""
    project_id: str
    customer_requirement: CustomerRequirement
    estimate: ProjectEstimate
    status: ProjectStatus
    start_date: datetime
    end_date: Optional[datetime]
    milestones: List[Dict[str, Any]]
    team_members: List[str]
    progress: float  # 0-100%
    quality_score: float
    customer_satisfaction: float

class CustomAIBusinessEngine:
    """🏢 맞춤형 AI 비즈니스 관리 엔진"""
    
    def __init__(self):
        self.customers = {}
        self.projects = {}
        self.templates = self._load_templates()
        self.pricing_model = self._load_pricing_model()
        self.quality_standards = self._load_quality_standards()
        
    def analyze_customer_inquiry(self, inquiry_data: Dict[str, Any]) -> Dict[str, Any]:
        """📋 고객 문의 분석"""
        
        # 요구사항 추출 및 분석
        requirement = self._extract_requirements(inquiry_data)
        
        # AI 유형 분류
        ai_type = self._classify_ai_type(requirement)
        
        # 복잡도 평가
        complexity = self._assess_complexity(requirement)
        
        # 실현 가능성 평가
        feasibility = self._assess_feasibility(requirement)
        
        # 유사 프로젝트 검색
        similar_projects = self._find_similar_projects(requirement)
        
        analysis_result = {
            'customer_id': str(uuid.uuid4()),
            'ai_type': ai_type,
            'complexity_level': complexity,
            'feasibility_score': feasibility,
            'estimated_effort': self._estimate_initial_effort(complexity, ai_type),
            'recommended_approach': self._recommend_approach(ai_type, complexity),
            'similar_projects': similar_projects,
            'next_steps': self._suggest_next_steps(feasibility),
            'questions_for_customer': self._generate_clarifying_questions(requirement)
        }
        
        return analysis_result
    
    def generate_proposal(self, customer_requirement: CustomerRequirement) -> Dict[str, Any]:
        """📄 제안서 생성"""
        
        # 기술적 솔루션 설계
        technical_solution = self._design_technical_solution(customer_requirement)
        
        # 프로젝트 견적 산정
        estimate = self._calculate_project_estimate(customer_requirement, technical_solution)
        
        # 프로젝트 계획 수립
        project_plan = self._create_project_plan(customer_requirement, estimate)
        
        # 팀 구성 제안
        team_composition = self._propose_team_composition(estimate)
        
        # 리스크 분석
        risk_analysis = self._analyze_project_risks(customer_requirement, technical_solution)
        
        proposal = {
            'proposal_id': str(uuid.uuid4()),
            'customer_id': customer_requirement.customer_id,
            'executive_summary': self._generate_executive_summary(customer_requirement),
            'technical_solution': technical_solution,
            'project_estimate': estimate,
            'project_plan': project_plan,
            'team_composition': team_composition,
            'risk_analysis': risk_analysis,
            'terms_and_conditions': self._generate_terms_and_conditions(),
            'next_steps': self._define_proposal_next_steps(),
            'validity_period': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        return proposal
    
    def _extract_requirements(self, inquiry_data: Dict[str, Any]) -> Dict[str, Any]:
        """요구사항 추출"""
        
        # 자연어 처리를 통한 요구사항 추출
        extracted = {
            'functional_requirements': [],
            'non_functional_requirements': [],
            'business_goals': [],
            'technical_constraints': [],
            'user_personas': []
        }
        
        # 키워드 기반 추출
        description = inquiry_data.get('description', '').lower()
        
        # 기능적 요구사항 추출
        if 'chatbot' in description or '챗봇' in description:
            extracted['functional_requirements'].append('conversational_interface')
        if 'analyze' in description or '분석' in description:
            extracted['functional_requirements'].append('data_analysis')
        if 'recommend' in description or '추천' in description:
            extracted['functional_requirements'].append('recommendation_system')
        
        # 비기능적 요구사항 추출
        if 'fast' in description or '빠른' in description:
            extracted['non_functional_requirements'].append('high_performance')
        if 'secure' in description or '보안' in description:
            extracted['non_functional_requirements'].append('security')
        if 'scale' in description or '확장' in description:
            extracted['non_functional_requirements'].append('scalability')
        
        return extracted
    
    def _classify_ai_type(self, requirement: Dict[str, Any]) -> AIType:
        """AI 유형 분류"""
        
        functional_reqs = requirement.get('functional_requirements', [])
        
        if 'conversational_interface' in functional_reqs:
            return AIType.CHATBOT
        elif 'data_analysis' in functional_reqs:
            return AIType.ANALYSIS
        elif 'recommendation_system' in functional_reqs:
            return AIType.RECOMMENDATION
        else:
            return AIType.CUSTOM
    
    def _assess_complexity(self, requirement: Dict[str, Any]) -> ComplexityLevel:
        """복잡도 평가"""
        
        complexity_score = 0
        
        # 기능적 요구사항 수
        complexity_score += len(requirement.get('functional_requirements', [])) * 2
        
        # 비기능적 요구사항 수
        complexity_score += len(requirement.get('non_functional_requirements', [])) * 1.5
        
        # 기술적 제약사항 수
        complexity_score += len(requirement.get('technical_constraints', [])) * 1
        
        if complexity_score < 5:
            return ComplexityLevel.BASIC
        elif complexity_score < 10:
            return ComplexityLevel.INTERMEDIATE
        elif complexity_score < 15:
            return ComplexityLevel.ADVANCED
        else:
            return ComplexityLevel.ENTERPRISE
    
    def _assess_feasibility(self, requirement: Dict[str, Any]) -> float:
        """실현 가능성 평가"""
        
        feasibility_score = 1.0
        
        # 기술적 실현 가능성
        functional_reqs = requirement.get('functional_requirements', [])
        
        # 일반적인 기능들은 높은 실현 가능성
        common_features = ['conversational_interface', 'data_analysis', 'recommendation_system']
        for feature in functional_reqs:
            if feature in common_features:
                feasibility_score *= 0.95  # 약간의 리스크
            else:
                feasibility_score *= 0.85  # 더 큰 리스크
        
        # 복잡도에 따른 실현 가능성
        complexity = self._assess_complexity(requirement)
        complexity_multipliers = {
            ComplexityLevel.BASIC: 1.0,
            ComplexityLevel.INTERMEDIATE: 0.9,
            ComplexityLevel.ADVANCED: 0.8,
            ComplexityLevel.ENTERPRISE: 0.7
        }
        
        feasibility_score *= complexity_multipliers[complexity]
        
        return min(feasibility_score, 1.0)
    
    def _estimate_initial_effort(self, complexity: ComplexityLevel, ai_type: AIType) -> Dict[str, int]:
        """초기 노력 추정"""
        
        base_hours = {
            ComplexityLevel.BASIC: 40,
            ComplexityLevel.INTERMEDIATE: 80,
            ComplexityLevel.ADVANCED: 160,
            ComplexityLevel.ENTERPRISE: 320
        }
        
        type_multipliers = {
            AIType.CHATBOT: 1.0,
            AIType.ANALYSIS: 1.2,
            AIType.AUTOMATION: 1.1,
            AIType.RECOMMENDATION: 1.3,
            AIType.PREDICTION: 1.4,
            AIType.CREATIVE: 1.5,
            AIType.CUSTOM: 1.6
        }
        
        total_hours = base_hours[complexity] * type_multipliers[ai_type]
        
        return {
            'development_hours': int(total_hours * 0.6),
            'testing_hours': int(total_hours * 0.2),
            'deployment_hours': int(total_hours * 0.1),
            'documentation_hours': int(total_hours * 0.1),
            'total_hours': int(total_hours)
        }
    
    def _recommend_approach(self, ai_type: AIType, complexity: ComplexityLevel) -> Dict[str, Any]:
        """접근 방법 추천"""
        
        approaches = {
            AIType.CHATBOT: {
                'framework': 'FastAPI + React',
                'ai_model': 'GPT-4 기반 커스텀 모델',
                'deployment': 'Cloud 기반',
                'development_phases': ['MVP', '기능 확장', '최적화']
            },
            AIType.ANALYSIS: {
                'framework': 'Python + ML Libraries',
                'ai_model': 'Scikit-learn + Custom Algorithms',
                'deployment': 'Cloud 기반',
                'development_phases': ['데이터 분석', '모델 개발', '시각화']
            },
            AIType.RECOMMENDATION: {
                'framework': 'Python + Recommendation Engine',
                'ai_model': 'Collaborative Filtering + Content-based',
                'deployment': 'Cloud 기반',
                'development_phases': ['데이터 수집', '모델 훈련', '추천 엔진']
            }
        }
        
        base_approach = approaches.get(ai_type, approaches[AIType.CHATBOT])
        
        # 복잡도에 따른 조정
        if complexity in [ComplexityLevel.ADVANCED, ComplexityLevel.ENTERPRISE]:
            base_approach['additional_considerations'] = [
                'Microservices 아키텍처',
                '고가용성 설계',
                '확장성 고려',
                '보안 강화'
            ]
        
        return base_approach
    
    def _find_similar_projects(self, requirement: Dict[str, Any]) -> List[Dict[str, Any]]:
        """유사 프로젝트 검색"""
        
        # 실제로는 데이터베이스에서 검색
        similar_projects = [
            {
                'project_name': 'E-commerce 챗봇',
                'similarity_score': 0.85,
                'duration_weeks': 8,
                'success_rate': 0.95,
                'lessons_learned': ['사용자 의도 파악이 핵심', '지속적인 학습 필요']
            },
            {
                'project_name': '데이터 분석 대시보드',
                'similarity_score': 0.72,
                'duration_weeks': 12,
                'success_rate': 0.88,
                'lessons_learned': ['데이터 품질이 중요', '시각화 최적화 필요']
            }
        ]
        
        return similar_projects
    
    def _suggest_next_steps(self, feasibility: float) -> List[str]:
        """다음 단계 제안"""
        
        if feasibility > 0.8:
            return [
                "요구사항 상세 분석 미팅 일정 조율",
                "기술적 프로토타입 개발 제안",
                "프로젝트 일정 및 예산 논의"
            ]
        elif feasibility > 0.6:
            return [
                "기술적 실현 가능성 상세 검토",
                "요구사항 재정의 및 우선순위 설정",
                "리스크 완화 방안 수립"
            ]
        else:
            return [
                "요구사항 단순화 검토",
                "단계별 접근 방안 제안",
                "대안 솔루션 탐색"
            ]
    
    def _generate_clarifying_questions(self, requirement: Dict[str, Any]) -> List[str]:
        """명확화 질문 생성"""
        
        questions = [
            "예상 사용자 수는 얼마나 되나요?",
            "기존 시스템과의 연동이 필요한가요?",
            "데이터 보안 요구사항이 있나요?",
            "성능 목표가 있다면 구체적으로 알려주세요.",
            "유지보수 및 업데이트 계획은 어떻게 되나요?"
        ]
        
        # 요구사항에 따른 추가 질문
        if 'data_analysis' in requirement.get('functional_requirements', []):
            questions.extend([
                "분석할 데이터의 형태와 크기는?",
                "실시간 분석이 필요한가요?",
                "분석 결과를 어떻게 활용할 예정인가요?"
            ])
        
        return questions
    
    def _design_technical_solution(self, customer_requirement: CustomerRequirement) -> Dict[str, Any]:
        """기술적 솔루션 설계"""
        
        solution = {
            'architecture': self._design_architecture(customer_requirement),
            'technology_stack': self._select_technology_stack(customer_requirement),
            'data_flow': self._design_data_flow(customer_requirement),
            'security_measures': self._design_security_measures(customer_requirement),
            'scalability_plan': self._design_scalability_plan(customer_requirement),
            'integration_points': self._identify_integration_points(customer_requirement)
        }
        
        return solution
    
    def _design_architecture(self, requirement: CustomerRequirement) -> Dict[str, Any]:
        """아키텍처 설계"""
        
        if requirement.complexity_level in [ComplexityLevel.ADVANCED, ComplexityLevel.ENTERPRISE]:
            return {
                'pattern': 'Microservices',
                'components': [
                    'API Gateway',
                    'Auth Service',
                    'AI Processing Service',
                    'Data Service',
                    'Frontend Application'
                ],
                'deployment': 'Containerized (Docker + Kubernetes)'
            }
        else:
            return {
                'pattern': 'Monolithic',
                'components': [
                    'Web Application',
                    'AI Module',
                    'Database'
                ],
                'deployment': 'Single Server or Cloud Instance'
            }
    
    def _select_technology_stack(self, requirement: CustomerRequirement) -> Dict[str, Any]:
        """기술 스택 선택"""
        
        stack = {
            'backend': 'Python (FastAPI)',
            'frontend': 'React + TypeScript',
            'database': 'PostgreSQL',
            'ai_framework': 'scikit-learn + Custom Models',
            'deployment': 'Docker + Cloud Platform'
        }
        
        # AI 유형에 따른 조정
        if requirement.ai_type == AIType.CHATBOT:
            stack['ai_framework'] = 'OpenAI API + Custom Training'
        elif requirement.ai_type == AIType.ANALYSIS:
            stack['ai_framework'] = 'Pandas + NumPy + scikit-learn'
        
        return stack
    
    def _design_data_flow(self, requirement: CustomerRequirement) -> List[Dict[str, Any]]:
        """데이터 흐름 설계"""
        
        return [
            {
                'step': 1,
                'description': '사용자 입력 수집',
                'components': ['Frontend', 'API Gateway']
            },
            {
                'step': 2,
                'description': 'AI 처리',
                'components': ['AI Service', 'ML Models']
            },
            {
                'step': 3,
                'description': '결과 반환',
                'components': ['API Gateway', 'Frontend']
            }
        ]
    
    def _design_security_measures(self, requirement: CustomerRequirement) -> List[str]:
        """보안 조치 설계"""
        
        measures = [
            'HTTPS 암호화',
            'JWT 토큰 인증',
            'API Rate Limiting',
            'Input Validation',
            'SQL Injection 방지'
        ]
        
        if requirement.complexity_level == ComplexityLevel.ENTERPRISE:
            measures.extend([
                'OAuth 2.0 인증',
                '데이터 암호화',
                '접근 권한 관리',
                '보안 로깅 및 모니터링'
            ])
        
        return measures
    
    def _design_scalability_plan(self, requirement: CustomerRequirement) -> Dict[str, Any]:
        """확장성 계획 설계"""
        
        return {
            'horizontal_scaling': '로드 밸런서 + 다중 인스턴스',
            'database_scaling': '읽기 복제본 + 샤딩',
            'caching_strategy': 'Redis 캐싱',
            'cdn_usage': '정적 파일 CDN 배포',
            'monitoring': 'CloudWatch + Custom Metrics'
        }
    
    def _identify_integration_points(self, requirement: CustomerRequirement) -> List[Dict[str, Any]]:
        """통합 지점 식별"""
        
        return [
            {
                'system': '기존 데이터베이스',
                'method': 'REST API',
                'complexity': 'Medium'
            },
            {
                'system': '외부 API',
                'method': 'HTTP Requests',
                'complexity': 'Low'
            }
        ]
    
    def _calculate_project_estimate(self, requirement: CustomerRequirement, solution: Dict[str, Any]) -> ProjectEstimate:
        """프로젝트 견적 산정"""
        
        # 기본 개발 비용 계산
        base_cost = self._calculate_base_development_cost(requirement, solution)
        
        # 복잡도에 따른 조정
        complexity_multiplier = {
            ComplexityLevel.BASIC: 1.0,
            ComplexityLevel.INTERMEDIATE: 1.5,
            ComplexityLevel.ADVANCED: 2.0,
            ComplexityLevel.ENTERPRISE: 3.0
        }
        
        development_cost = base_cost * complexity_multiplier[requirement.complexity_level]
        
        # 유지보수 비용 (연간)
        maintenance_cost = development_cost * 0.2
        
        # 총 비용 (1년 유지보수 포함)
        total_cost = development_cost + maintenance_cost
        
        # 예상 시간 계산
        estimated_hours = int(development_cost / 100)  # 시간당 10만원 가정
        timeline_weeks = max(4, estimated_hours // 40)  # 주당 40시간
        team_size = max(2, estimated_hours // (timeline_weeks * 40))
        
        return ProjectEstimate(
            project_id=str(uuid.uuid4()),
            development_cost=development_cost,
            maintenance_cost=maintenance_cost,
            total_cost=total_cost,
            estimated_hours=estimated_hours,
            timeline_weeks=timeline_weeks,
            team_size=team_size,
            technologies=list(solution.get('technology_stack', {}).values()),
            deliverables=self._define_deliverables(requirement),
            risk_factors=self._identify_risk_factors(requirement, solution),
            assumptions=self._list_assumptions(requirement, solution)
        )
    
    def _calculate_base_development_cost(self, requirement: CustomerRequirement, solution: Dict[str, Any]) -> float:
        """기본 개발 비용 계산"""
        
        base_costs = {
            AIType.CHATBOT: 5000000,        # 500만원
            AIType.ANALYSIS: 8000000,       # 800만원
            AIType.AUTOMATION: 6000000,     # 600만원
            AIType.RECOMMENDATION: 10000000, # 1000만원
            AIType.PREDICTION: 12000000,    # 1200만원
            AIType.CREATIVE: 15000000,      # 1500만원
            AIType.CUSTOM: 10000000         # 1000만원
        }
        
        return base_costs.get(requirement.ai_type, 10000000)
    
    def _define_deliverables(self, requirement: CustomerRequirement) -> List[str]:
        """인도물 정의"""
        
        deliverables = [
            'AI 시스템 소스코드',
            'API 문서',
            '사용자 매뉴얼',
            '배포 가이드',
            '시스템 아키텍처 문서'
        ]
        
        if requirement.complexity_level in [ComplexityLevel.ADVANCED, ComplexityLevel.ENTERPRISE]:
            deliverables.extend([
                '성능 테스트 보고서',
                '보안 검토 보고서',
                '운영 매뉴얼',
                '모니터링 대시보드'
            ])
        
        return deliverables
    
    def _identify_risk_factors(self, requirement: CustomerRequirement, solution: Dict[str, Any]) -> List[str]:
        """리스크 요소 식별"""
        
        risks = [
            '요구사항 변경',
            '기술적 복잡도',
            '데이터 품질 이슈'
        ]
        
        if requirement.complexity_level == ComplexityLevel.ENTERPRISE:
            risks.extend([
                '대규모 시스템 통합',
                '성능 요구사항 충족',
                '보안 요구사항 준수'
            ])
        
        return risks
    
    def _list_assumptions(self, requirement: CustomerRequirement, solution: Dict[str, Any]) -> List[str]:
        """가정사항 나열"""
        
        return [
            '고객이 필요한 데이터를 제공할 수 있음',
            '기존 시스템과의 호환성 확보 가능',
            '프로젝트 기간 중 요구사항 변경 최소화',
            '적절한 테스트 환경 제공',
            '고객 측 담당자의 적극적 협조'
        ]
    
    def _create_project_plan(self, requirement: CustomerRequirement, estimate: ProjectEstimate) -> Dict[str, Any]:
        """프로젝트 계획 수립"""
        
        phases = [
            {
                'name': '요구사항 분석 및 설계',
                'duration_weeks': max(1, estimate.timeline_weeks * 0.2),
                'deliverables': ['요구사항 명세서', '시스템 설계서']
            },
            {
                'name': '개발',
                'duration_weeks': max(2, estimate.timeline_weeks * 0.5),
                'deliverables': ['MVP', '기능 구현', '통합 테스트']
            },
            {
                'name': '테스트 및 배포',
                'duration_weeks': max(1, estimate.timeline_weeks * 0.2),
                'deliverables': ['테스트 완료', '배포', '사용자 교육']
            },
            {
                'name': '안정화 및 인수',
                'duration_weeks': max(1, estimate.timeline_weeks * 0.1),
                'deliverables': ['버그 수정', '성능 최적화', '프로젝트 인수']
            }
        ]
        
        return {
            'total_duration_weeks': estimate.timeline_weeks,
            'phases': phases,
            'milestones': self._define_milestones(phases),
            'resource_allocation': self._plan_resource_allocation(estimate)
        }
    
    def _define_milestones(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """마일스톤 정의"""
        
        milestones = []
        current_week = 0
        
        for phase in phases:
            current_week += phase['duration_weeks']
            milestones.append({
                'name': f"{phase['name']} 완료",
                'week': current_week,
                'criteria': phase['deliverables']
            })
        
        return milestones
    
    def _plan_resource_allocation(self, estimate: ProjectEstimate) -> Dict[str, Any]:
        """자원 배분 계획"""
        
        return {
            'team_composition': {
                'project_manager': 1,
                'ai_engineer': max(1, estimate.team_size // 2),
                'backend_developer': 1,
                'frontend_developer': 1,
                'qa_engineer': 1
            },
            'key_roles': [
                'AI 엔지니어: 모델 개발 및 최적화',
                '백엔드 개발자: API 및 시스템 구조',
                '프론트엔드 개발자: 사용자 인터페이스',
                'QA 엔지니어: 품질 보증 및 테스트'
            ]
        }
    
    def _propose_team_composition(self, estimate: ProjectEstimate) -> Dict[str, Any]:
        """팀 구성 제안"""
        
        return {
            'total_team_size': estimate.team_size,
            'roles': [
                {
                    'role': 'AI Engineer',
                    'count': max(1, estimate.team_size // 3),
                    'responsibilities': ['AI 모델 개발', '데이터 처리', '성능 최적화']
                },
                {
                    'role': 'Full-stack Developer',
                    'count': max(1, estimate.team_size // 3),
                    'responsibilities': ['웹 애플리케이션 개발', 'API 개발', 'UI/UX']
                },
                {
                    'role': 'DevOps Engineer',
                    'count': 1,
                    'responsibilities': ['배포', '인프라', '모니터링']
                }
            ],
            'external_consultants': [
                'UI/UX 디자이너 (필요시)',
                '보안 컨설턴트 (엔터프라이즈급)',
                '도메인 전문가 (업종별)'
            ]
        }
    
    def _analyze_project_risks(self, requirement: CustomerRequirement, solution: Dict[str, Any]) -> Dict[str, Any]:
        """프로젝트 리스크 분석"""
        
        technical_risks = [
            {
                'risk': 'AI 모델 성능 부족',
                'probability': 'Medium',
                'impact': 'High',
                'mitigation': '다양한 알고리즘 테스트, 데이터 품질 개선'
            },
            {
                'risk': '기존 시스템 통합 이슈',
                'probability': 'Medium',
                'impact': 'Medium',
                'mitigation': '사전 호환성 테스트, API 문서 확인'
            }
        ]
        
        business_risks = [
            {
                'risk': '요구사항 변경',
                'probability': 'High',
                'impact': 'Medium',
                'mitigation': '명확한 요구사항 문서화, 변경 관리 프로세스'
            },
            {
                'risk': '예산 초과',
                'probability': 'Medium',
                'impact': 'High',
                'mitigation': '단계별 예산 관리, 정기적 리뷰'
            }
        ]
        
        return {
            'technical_risks': technical_risks,
            'business_risks': business_risks,
            'overall_risk_level': self._calculate_overall_risk(technical_risks + business_risks)
        }
    
    def _calculate_overall_risk(self, risks: List[Dict[str, Any]]) -> str:
        """전체 리스크 수준 계산"""
        
        risk_scores = []
        for risk in risks:
            prob_score = {'Low': 1, 'Medium': 2, 'High': 3}[risk['probability']]
            impact_score = {'Low': 1, 'Medium': 2, 'High': 3}[risk['impact']]
            risk_scores.append(prob_score * impact_score)
        
        avg_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        
        if avg_score < 3:
            return 'Low'
        elif avg_score < 6:
            return 'Medium'
        else:
            return 'High'
    
    def _generate_executive_summary(self, requirement: CustomerRequirement) -> str:
        """경영진 요약 생성"""
        
        return f"""
{requirement.company}님을 위한 {requirement.ai_type.value} AI 솔루션 제안

고객의 요구사항을 분석한 결과, {requirement.complexity_level.value} 수준의 맞춤형 AI 시스템 개발을 제안드립니다.

주요 특징:
- {requirement.ai_type.value} 기반 지능형 시스템
- {requirement.target_users} 대상 최적화
- 확장 가능한 아키텍처 설계

기대 효과:
- 업무 효율성 향상
- 고객 만족도 증대
- 운영 비용 절감
        """
    
    def _generate_terms_and_conditions(self) -> List[str]:
        """약관 생성"""
        
        return [
            "프로젝트 시작 전 50% 선금 지불",
            "각 마일스톤 완료 시 단계별 지불",
            "요구사항 변경 시 추가 비용 발생 가능",
            "프로젝트 완료 후 3개월 무상 A/S 제공",
            "소스코드 및 지적재산권은 프로젝트 완료 후 고객에게 이전",
            "기밀유지 약정 체결 필수"
        ]
    
    def _define_proposal_next_steps(self) -> List[str]:
        """제안서 다음 단계 정의"""
        
        return [
            "제안서 검토 (1주일)",
            "협상 및 계약 조건 논의 (1주일)",
            "계약 체결",
            "프로젝트 킥오프 미팅",
            "개발 시작"
        ]
    
    def manage_project_lifecycle(self, project_id: str) -> Dict[str, Any]:
        """프로젝트 라이프사이클 관리"""
        
        if project_id not in self.projects:
            return {'error': '프로젝트를 찾을 수 없습니다.'}
        
        project = self.projects[project_id]
        
        # 진행률 업데이트
        progress = self._calculate_project_progress(project)
        project.progress = progress
        
        # 품질 점검
        quality_score = self._assess_project_quality(project)
        project.quality_score = quality_score
        
        # 다음 단계 제안
        next_actions = self._suggest_next_actions(project)
        
        return {
            'project_id': project_id,
            'current_status': project.status.value,
            'progress': progress,
            'quality_score': quality_score,
            'next_actions': next_actions,
            'alerts': self._check_project_alerts(project)
        }
    
    def _calculate_project_progress(self, project: Project) -> float:
        """프로젝트 진행률 계산"""
        
        completed_milestones = len([m for m in project.milestones if m.get('completed', False)])
        total_milestones = len(project.milestones)
        
        return (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    
    def _assess_project_quality(self, project: Project) -> float:
        """프로젝트 품질 평가"""
        
        # 간단한 품질 점수 계산
        quality_factors = {
            'code_quality': 85,      # 코드 품질
            'test_coverage': 90,     # 테스트 커버리지
            'documentation': 80,     # 문서화 수준
            'performance': 88,       # 성능
            'security': 92          # 보안
        }
        
        return sum(quality_factors.values()) / len(quality_factors)
    
    def _suggest_next_actions(self, project: Project) -> List[str]:
        """다음 액션 제안"""
        
        status_actions = {
            ProjectStatus.DEVELOPMENT: [
                "일일 스탠드업 미팅 진행",
                "코드 리뷰 수행",
                "진행률 업데이트"
            ],
            ProjectStatus.TESTING: [
                "테스트 케이스 실행",
                "버그 수정",
                "성능 최적화"
            ],
            ProjectStatus.DELIVERY: [
                "배포 준비",
                "사용자 교육",
                "문서 최종 검토"
            ]
        }
        
        return status_actions.get(project.status, ["프로젝트 상태 검토"])
    
    def _check_project_alerts(self, project: Project) -> List[str]:
        """프로젝트 알림 확인"""
        
        alerts = []
        
        # 일정 지연 체크
        if project.end_date and project.end_date < datetime.now():
            alerts.append("프로젝트 일정이 지연되었습니다.")
        
        # 품질 점수 체크
        if project.quality_score < 80:
            alerts.append("품질 점수가 기준 이하입니다.")
        
        # 고객 만족도 체크
        if project.customer_satisfaction < 80:
            alerts.append("고객 만족도가 낮습니다.")
        
        return alerts
    
    def _load_templates(self) -> Dict[str, Any]:
        """템플릿 로드"""
        
        return {
            'proposal_template': '제안서 템플릿',
            'contract_template': '계약서 템플릿',
            'project_plan_template': '프로젝트 계획 템플릿'
        }
    
    def _load_pricing_model(self) -> Dict[str, Any]:
        """가격 모델 로드"""
        
        return {
            'hourly_rate': 100000,  # 시간당 10만원
            'complexity_multipliers': {
                'basic': 1.0,
                'intermediate': 1.5,
                'advanced': 2.0,
                'enterprise': 3.0
            },
            'technology_premiums': {
                'ai_development': 1.2,
                'custom_algorithms': 1.5,
                'real_time_processing': 1.3
            }
        }
    
    def _load_quality_standards(self) -> Dict[str, Any]:
        """품질 기준 로드"""
        
        return {
            'minimum_test_coverage': 80,
            'code_quality_threshold': 85,
            'performance_requirements': {
                'response_time': '< 2초',
                'availability': '99.9%',
                'error_rate': '< 0.1%'
            },
            'security_requirements': [
                'HTTPS 암호화',
                '인증/인가',
                '데이터 검증',
                '보안 로깅'
            ]
        }
    
    def generate_business_report(self) -> str:
        """비즈니스 보고서 생성"""
        
        total_projects = len(self.projects)
        completed_projects = len([p for p in self.projects.values() if p.status == ProjectStatus.COMPLETED])
        
        report = f"""
🏢 맞춤형 AI 비즈니스 현황 보고서
=====================================

📊 프로젝트 현황:
- 총 프로젝트: {total_projects}개
- 완료 프로젝트: {completed_projects}개
- 성공률: {(completed_projects/total_projects*100) if total_projects > 0 else 0:.1f}%

💰 매출 현황:
- 총 계약금액: {sum(p.estimate.total_cost for p in self.projects.values()):,}원
- 평균 프로젝트 규모: {sum(p.estimate.total_cost for p in self.projects.values())/max(total_projects, 1):,.0f}원

🎯 주요 AI 유형:
"""
        
        # AI 유형별 통계
        ai_type_counts = {}
        for project in self.projects.values():
            ai_type = project.customer_requirement.ai_type.value
            ai_type_counts[ai_type] = ai_type_counts.get(ai_type, 0) + 1
        
        for ai_type, count in ai_type_counts.items():
            report += f"- {ai_type}: {count}개\n"
        
        report += f"""
📈 품질 지표:
- 평균 품질 점수: {sum(p.quality_score for p in self.projects.values())/max(total_projects, 1):.1f}점
- 평균 고객 만족도: {sum(p.customer_satisfaction for p in self.projects.values())/max(total_projects, 1):.1f}점

🚀 성장 기회:
- 반복 고객 비율 증대
- 새로운 AI 기술 도입
- 자동화 도구 개발
- 파트너십 확대
        """
        
        return report 