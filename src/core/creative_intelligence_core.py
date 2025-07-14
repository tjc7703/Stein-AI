"""
🎨 창의적 지능 코어
혁신적 사고, 창의적 문제해결, 브레이크스루 아이디어 생성

Stein님의 천재성과 AI의 처리능력을 융합한 창의성 엔진
"""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor
import itertools
import uuid

class CreativityMode(Enum):
    """창의성 모드"""
    EXPLORATION = "exploration"        # 탐색적 사고
    INNOVATION = "innovation"          # 혁신적 사고  
    SYNTHESIS = "synthesis"            # 통합적 사고
    BREAKTHROUGH = "breakthrough"      # 돌파적 사고
    COLLABORATION = "collaboration"    # 협력적 사고

class ThinkingPattern(Enum):
    """사고 패턴"""
    DIVERGENT = "divergent"           # 확산적 사고
    CONVERGENT = "convergent"         # 수렴적 사고
    LATERAL = "lateral"               # 수평적 사고
    ANALOGICAL = "analogical"         # 유추적 사고
    SYSTEMIC = "systemic"             # 시스템적 사고
    BREAKTHROUGH = "breakthrough"     # 돌파적 사고
    SYNTHESIS = "synthesis"           # 통합적 사고

@dataclass
class CreativeIdea:
    """창의적 아이디어"""
    id: str
    timestamp: str
    title: str
    description: str
    creativity_score: float
    feasibility_score: float
    innovation_level: float
    domain: str
    thinking_pattern: ThinkingPattern
    inspiration_sources: List[str]
    implementation_steps: List[str]
    potential_impact: Dict[str, float]
    synergy_opportunities: List[str]

@dataclass
class CreativityMetrics:
    """창의성 지표"""
    originality: float          # 독창성
    fluency: float             # 유창성
    flexibility: float         # 유연성
    elaboration: float         # 정교성
    synthesis_ability: float   # 통합능력
    breakthrough_potential: float  # 돌파가능성

class CreativeIntelligenceCore:
    """
    🎨 창의적 지능 코어
    - 혁신적 아이디어 생성 및 평가
    - 다차원적 창의적 사고 프로세스
    - Stein님과의 창의적 협업 최적화
    - 브레이크스루 솔루션 발굴
    """
    
    def __init__(self):
        self.creativity_metrics = CreativityMetrics(
            originality=1.0,
            fluency=1.0,
            flexibility=1.0,
            elaboration=1.0,
            synthesis_ability=1.0,
            breakthrough_potential=1.0
        )
        
        # 창의적 아이디어 저장소
        self.idea_repository: List[CreativeIdea] = []
        self.inspiration_database: Dict[str, List[str]] = {}
        self.pattern_combinations: Dict[str, List[Tuple]] = {}
        
        # 창의성 시드 데이터
        self.creativity_seeds = {
            "technology": [
                "인공지능", "블록체인", "양자컴퓨팅", "IoT", "AR/VR", "로보틱스",
                "바이오테크", "나노기술", "우주기술", "재생에너지"
            ],
            "methodology": [
                "디자인싱킹", "애자일", "린스타트업", "시스템사고", "창의적문제해결",
                "브레인스토밍", "SCAMPER", "마인드맵", "시나리오플래닝"
            ],
            "domains": [
                "교육", "헬스케어", "금융", "엔터테인먼트", "교통", "환경",
                "농업", "제조", "유통", "통신", "보안", "게임"
            ],
            "patterns": [
                "융합", "분할", "역전", "확장", "축소", "변환", "연결", "분리",
                "순환", "계층화", "병렬화", "자동화", "개인화", "협업화"
            ]
        }
        
        # 창의적 사고 프로세스
        self.thinking_processes = {
            ThinkingPattern.DIVERGENT: self._divergent_thinking,
            ThinkingPattern.CONVERGENT: self._convergent_thinking,
            ThinkingPattern.LATERAL: self._lateral_thinking,
            ThinkingPattern.ANALOGICAL: self._analogical_thinking,
            ThinkingPattern.SYSTEMIC: self._systemic_thinking
        }
        
        # 혁신 히스토리
        self.innovation_history: List[Dict] = []
        self.breakthrough_moments: List[Dict] = []
        
        # 실시간 창의성 모니터링 - 임시 비활성화
        self.creativity_monitor_active = False  # 성능 최적화를 위해 비활성화
        # self.monitor_thread = threading.Thread(target=self._creativity_monitoring_loop, daemon=True)
        # self.monitor_thread.start()
        
        # 데이터 경로
        self.data_path = Path("data/creative_intelligence")
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 기존 아이디어 로드
        self._load_existing_ideas()
        
        print("🎨 창의적 지능 코어 초기화 완료!")
        print(f"💡 현재 아이디어 저장소: {len(self.idea_repository)}개")
    
    def generate_creative_ideas(self, 
                              problem: str,
                              domain: str = "technology",
                              creativity_mode: CreativityMode = CreativityMode.INNOVATION,
                              thinking_patterns: List[ThinkingPattern] = None,
                              count: int = 5) -> List[CreativeIdea]:
        """
        💡 창의적 아이디어 생성
        """
        if thinking_patterns is None:
            thinking_patterns = [ThinkingPattern.DIVERGENT, ThinkingPattern.LATERAL]
        
        ideas = []
        
        for pattern in thinking_patterns:
            pattern_ideas = self._generate_ideas_with_pattern(
                problem, domain, creativity_mode, pattern, count
            )
            ideas.extend(pattern_ideas)
        
        # 아이디어 평가 및 정제
        evaluated_ideas = []
        for idea in ideas:
            evaluated_idea = self._evaluate_and_enhance_idea(idea, problem)
            evaluated_ideas.append(evaluated_idea)
            
        # 최고 아이디어 선별
        top_ideas = sorted(evaluated_ideas, 
                          key=lambda x: x.creativity_score * x.feasibility_score, 
                          reverse=True)[:count]
        
        # 아이디어 저장소에 추가
        self.idea_repository.extend(top_ideas)
        
        # 창의성 지표 업데이트
        self._update_creativity_metrics(top_ideas)
        
        return top_ideas
    
    def _generate_ideas_with_pattern(self, 
                                   problem: str, 
                                   domain: str,
                                   mode: CreativityMode,
                                   pattern: ThinkingPattern,
                                   count: int) -> List[CreativeIdea]:
        """특정 사고 패턴으로 아이디어 생성"""
        thinking_func = self.thinking_processes[pattern]
        raw_ideas = thinking_func(problem, domain, mode, count)
        
        ideas = []
        for raw_idea in raw_ideas:
            idea = CreativeIdea(
                id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                title=raw_idea["title"],
                description=raw_idea["description"],
                creativity_score=0.0,  # 후에 평가
                feasibility_score=0.0,
                innovation_level=0.0,
                domain=domain,
                thinking_pattern=pattern,
                inspiration_sources=raw_idea.get("sources", []),
                implementation_steps=raw_idea.get("steps", []),
                potential_impact={},
                synergy_opportunities=[]
            )
            ideas.append(idea)
        
        return ideas
    
    def _divergent_thinking(self, problem: str, domain: str, mode: CreativityMode, count: int) -> List[Dict]:
        """확산적 사고"""
        ideas = []
        
        # 문제를 여러 관점에서 접근
        perspectives = ["기술적", "사용자", "비즈니스", "사회적", "환경적"]
        tech_seeds = self.creativity_seeds["technology"]
        method_seeds = self.creativity_seeds["methodology"]
        
        for i in range(count):
            perspective = random.choice(perspectives)
            tech = random.choice(tech_seeds)
            method = random.choice(method_seeds)
            
            idea = {
                "title": f"{perspective} 관점의 {tech} 기반 {problem} 해결방안",
                "description": f"{method}을 활용하여 {tech} 기술로 {problem}을 {perspective} 관점에서 해결하는 혁신적 접근법. "
                             f"기존 방식의 한계를 뛰어넘는 창의적 솔루션을 제공.",
                "sources": [perspective, tech, method],
                "steps": [
                    f"{perspective} 요구사항 분석",
                    f"{tech} 기술 적용 방안 설계",
                    f"{method} 방법론 통합",
                    "프로토타입 개발",
                    "사용자 피드백 수집 및 개선"
                ]
            }
            ideas.append(idea)
        
        return ideas
    
    def _convergent_thinking(self, problem: str, domain: str, mode: CreativityMode, count: int) -> List[Dict]:
        """수렴적 사고"""
        ideas = []
        
        # 기존 아이디어들에서 최적 요소 추출하여 통합
        if self.idea_repository:
            related_ideas = [idea for idea in self.idea_repository if domain in idea.domain]
            
            if len(related_ideas) >= 2:
                for i in range(count):
                    sample_ideas = random.sample(related_ideas, min(3, len(related_ideas)))
                    
                    # 최고 요소들 통합
                    best_elements = []
                    for idea in sample_ideas:
                        if idea.creativity_score > 7.0:
                            best_elements.extend(idea.implementation_steps[:2])
                    
                    idea = {
                        "title": f"통합형 {problem} 최적 솔루션",
                        "description": f"검증된 다양한 접근법의 최고 요소들을 통합하여 {problem}에 대한 "
                                     f"최적화된 솔루션 제공. 실용성과 혁신성의 균형.",
                        "sources": [f"아이디어_{sample_idea.id[:8]}" for sample_idea in sample_ideas],
                        "steps": best_elements[:5] if best_elements else [
                            "기존 솔루션 분석",
                            "최적 요소 추출",
                            "통합 아키텍처 설계",
                            "성능 최적화",
                            "품질 검증"
                        ]
                    }
                    ideas.append(idea)
        
        # 기본 수렴적 아이디어 생성
        if len(ideas) < count:
            for i in range(count - len(ideas)):
                idea = {
                    "title": f"{problem} 핵심 요소 집중 솔루션",
                    "description": f"{problem}의 핵심 요소에 집중하여 가장 효과적이고 실용적인 해결책 제시.",
                    "sources": ["핵심요소분석", "실용성중심"],
                    "steps": [
                        "핵심 문제 정의",
                        "필수 기능 선별",
                        "최소 실행 가능 제품 설계",
                        "점진적 기능 확장",
                        "지속적 개선"
                    ]
                }
                ideas.append(idea)
        
        return ideas
    
    def _lateral_thinking(self, problem: str, domain: str, mode: CreativityMode, count: int) -> List[Dict]:
        """수평적 사고 (에드워드 드 보노의 래터럴 씽킹)"""
        ideas = []
        
        # 무작위 연결을 통한 아이디어 생성
        random_domains = random.sample(self.creativity_seeds["domains"], 3)
        random_tech = random.sample(self.creativity_seeds["technology"], 3)
        random_patterns = random.sample(self.creativity_seeds["patterns"], 3)
        
        for i in range(count):
            unrelated_domain = random.choice(random_domains)
            unrelated_tech = random.choice(random_tech)
            unrelated_pattern = random.choice(random_patterns)
            
            idea = {
                "title": f"{unrelated_domain} 방식의 {problem} {unrelated_pattern} 접근",
                "description": f"{unrelated_domain} 분야의 {unrelated_tech} 기술을 {unrelated_pattern} 방식으로 "
                             f"적용하여 {problem}을 완전히 새로운 관점에서 해결. "
                             f"기존의 고정관념을 벗어난 혁신적 발상.",
                "sources": [unrelated_domain, unrelated_tech, unrelated_pattern],
                "steps": [
                    f"{unrelated_domain} 사례 연구",
                    f"{unrelated_tech} 기술 적용성 검토",
                    f"{unrelated_pattern} 방법론 설계",
                    "프로토타입 실험",
                    "효과성 검증 및 개선"
                ]
            }
            ideas.append(idea)
        
        return ideas
    
    def _analogical_thinking(self, problem: str, domain: str, mode: CreativityMode, count: int) -> List[Dict]:
        """유추적 사고"""
        ideas = []
        
        # 자연계, 생물학적 시스템에서 영감
        natural_systems = [
            "개미군집", "벌집구조", "신경망", "면역체계", "생태계", 
            "진화과정", "광합성", "DNA복제", "새떼비행", "물의순환"
        ]
        
        for i in range(count):
            natural_system = random.choice(natural_systems)
            
            # 자연 시스템의 특성을 기술 문제에 적용
            system_properties = self._get_natural_system_properties(natural_system)
            
            idea = {
                "title": f"{natural_system} 모델 기반 {problem} 해결 시스템",
                "description": f"{natural_system}의 {', '.join(system_properties)}을 모방하여 "
                             f"{problem}을 해결하는 바이오미메틱스 접근법. "
                             f"자연의 최적화된 시스템을 기술에 적용.",
                "sources": [natural_system, "biomimetics"] + system_properties,
                "steps": [
                    f"{natural_system} 작동 원리 분석",
                    "핵심 메커니즘 추출",
                    "기술적 구현 방안 설계",
                    "시뮬레이션 및 테스트",
                    "실제 시스템 적용"
                ]
            }
            ideas.append(idea)
        
        return ideas
    
    def _systemic_thinking(self, problem: str, domain: str, mode: CreativityMode, count: int) -> List[Dict]:
        """시스템적 사고"""
        ideas = []
        
        # 시스템 레벨에서 문제 접근
        system_levels = ["개인", "팀", "조직", "산업", "사회", "글로벌"]
        system_perspectives = ["구조", "프로세스", "관계", "문화", "환경"]
        
        for i in range(count):
            level = random.choice(system_levels)
            perspective = random.choice(system_perspectives)
            
            idea = {
                "title": f"{level} 레벨 {perspective} 관점 {problem} 시스템 솔루션",
                "description": f"{level} 레벨에서 {perspective} 관점으로 {problem}을 시스템적으로 분석하고 "
                             f"전체적 최적화를 통한 근본적 해결책 제시. "
                             f"부분이 아닌 전체 시스템의 변화를 추구.",
                "sources": [level, perspective, "systems_thinking"],
                "steps": [
                    f"{level} 레벨 현상 매핑",
                    f"{perspective} 관점 분석",
                    "시스템 동학 모델링",
                    "레버리지 포인트 식별",
                    "시스템 개입 설계",
                    "피드백 루프 구축"
                ]
            }
            ideas.append(idea)
        
        return ideas
    
    def _get_natural_system_properties(self, system: str) -> List[str]:
        """자연 시스템의 특성 반환"""
        properties_map = {
            "개미군집": ["집단지능", "자기조직화", "효율적분업"],
            "벌집구조": ["최적구조", "공간효율", "협력작업"],
            "신경망": ["분산처리", "학습능력", "적응성"],
            "면역체계": ["적응방어", "기억기능", "자가치유"],
            "생태계": ["상호의존", "균형유지", "순환구조"],
            "진화과정": ["적응진화", "다양성", "자연선택"],
            "광합성": ["에너지변환", "효율최적화", "지속가능"],
            "DNA복제": ["정확복사", "오류수정", "정보저장"],
            "새떼비행": ["군집행동", "동조화", "효율이동"],
            "물의순환": ["순환시스템", "자정작용", "에너지보존"]
        }
        
        return properties_map.get(system, ["자기조직화", "적응성", "효율성"])
    
    def _evaluate_and_enhance_idea(self, idea: CreativeIdea, original_problem: str) -> CreativeIdea:
        """아이디어 평가 및 개선"""
        
        # 창의성 점수 계산
        idea.creativity_score = self._calculate_creativity_score(idea)
        
        # 실현가능성 점수 계산
        idea.feasibility_score = self._calculate_feasibility_score(idea)
        
        # 혁신 수준 계산
        idea.innovation_level = self._calculate_innovation_level(idea)
        
        # 잠재적 영향도 분석
        idea.potential_impact = self._analyze_potential_impact(idea)
        
        # 시너지 기회 식별
        idea.synergy_opportunities = self._identify_synergy_opportunities(idea)
        
        # 구현 단계 개선
        idea.implementation_steps = self._enhance_implementation_steps(idea)
        
        return idea
    
    def _calculate_creativity_score(self, idea: CreativeIdea) -> float:
        """창의성 점수 계산"""
        # 독창성 평가
        uniqueness_score = self._assess_uniqueness(idea)
        
        # 복합성 평가 (여러 요소의 조합)
        complexity_score = len(idea.inspiration_sources) / 5.0
        
        # 사고 패턴 보너스
        pattern_bonus = {
            ThinkingPattern.LATERAL: 1.2,
            ThinkingPattern.ANALOGICAL: 1.1,
            ThinkingPattern.DIVERGENT: 1.0,
            ThinkingPattern.SYSTEMIC: 1.1,
            ThinkingPattern.CONVERGENT: 0.9
        }.get(idea.thinking_pattern, 1.0)
        
        base_score = (uniqueness_score * 0.6 + complexity_score * 0.4) * pattern_bonus
        
        return min(max(base_score * 10, 1.0), 10.0)
    
    def _assess_uniqueness(self, idea: CreativeIdea) -> float:
        """독창성 평가"""
        # 기존 아이디어와의 유사도 체크
        similar_count = 0
        for existing_idea in self.idea_repository:
            if self._calculate_idea_similarity(idea, existing_idea) > 0.7:
                similar_count += 1
        
        # 유사한 아이디어가 적을수록 높은 독창성
        uniqueness = max(0.1, 1.0 - (similar_count / max(len(self.idea_repository), 10)))
        
        return uniqueness
    
    def _calculate_idea_similarity(self, idea1: CreativeIdea, idea2: CreativeIdea) -> float:
        """아이디어 유사도 계산"""
        # 간단한 키워드 기반 유사도
        words1 = set(idea1.title.lower().split() + idea1.description.lower().split())
        words2 = set(idea2.title.lower().split() + idea2.description.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_feasibility_score(self, idea: CreativeIdea) -> float:
        """실현가능성 점수 계산"""
        # 구현 단계의 구체성
        step_specificity = len([step for step in idea.implementation_steps if len(step) > 10]) / max(len(idea.implementation_steps), 1)
        
        # 기술 성숙도 (알려진 기술인지)
        known_tech_count = 0
        for source in idea.inspiration_sources:
            if source in self.creativity_seeds["technology"]:
                known_tech_count += 1
        
        tech_maturity = known_tech_count / max(len(idea.inspiration_sources), 1)
        
        # 도메인 적합성
        domain_fit = 1.0 if idea.domain in self.creativity_seeds["domains"] else 0.7
        
        feasibility = (step_specificity * 0.4 + tech_maturity * 0.4 + domain_fit * 0.2)
        
        return min(max(feasibility * 10, 1.0), 10.0)
    
    def _calculate_innovation_level(self, idea: CreativeIdea) -> float:
        """혁신 수준 계산"""
        # 사고 패턴별 혁신도
        pattern_innovation = {
            ThinkingPattern.BREAKTHROUGH: 1.0,
            ThinkingPattern.LATERAL: 0.9,
            ThinkingPattern.ANALOGICAL: 0.8,
            ThinkingPattern.DIVERGENT: 0.7,
            ThinkingPattern.SYSTEMIC: 0.8,
            ThinkingPattern.CONVERGENT: 0.5
        }.get(idea.thinking_pattern, 0.7)
        
        # 영감 소스의 다양성
        source_diversity = len(set(idea.inspiration_sources)) / max(len(idea.inspiration_sources), 1)
        
        # 설명의 혁신 키워드
        innovation_keywords = ["혁신", "혁명", "돌파", "새로운", "최초", "독창적", "획기적"]
        innovation_word_count = sum(1 for kw in innovation_keywords if kw in idea.description)
        keyword_score = min(innovation_word_count / 3, 1.0)
        
        innovation = (pattern_innovation * 0.5 + source_diversity * 0.3 + keyword_score * 0.2)
        
        return min(max(innovation * 10, 1.0), 10.0)
    
    def _analyze_potential_impact(self, idea: CreativeIdea) -> Dict[str, float]:
        """잠재적 영향도 분석"""
        impact = {
            "technical": 0.0,
            "social": 0.0,
            "economic": 0.0,
            "environmental": 0.0,
            "user_experience": 0.0
        }
        
        description_lower = idea.description.lower()
        
        # 기술적 영향
        tech_indicators = ["기술", "알고리즘", "시스템", "플랫폼", "인프라"]
        impact["technical"] = min(sum(1 for ind in tech_indicators if ind in description_lower) * 2, 10)
        
        # 사회적 영향
        social_indicators = ["사회", "커뮤니티", "협업", "교육", "소통"]
        impact["social"] = min(sum(1 for ind in social_indicators if ind in description_lower) * 2, 10)
        
        # 경제적 영향
        economic_indicators = ["비즈니스", "수익", "효율", "비용", "생산성"]
        impact["economic"] = min(sum(1 for ind in economic_indicators if ind in description_lower) * 2, 10)
        
        # 환경적 영향
        env_indicators = ["환경", "지속가능", "친환경", "에너지", "재활용"]
        impact["environmental"] = min(sum(1 for ind in env_indicators if ind in description_lower) * 2, 10)
        
        # 사용자 경험 영향
        ux_indicators = ["사용자", "경험", "편의", "접근성", "직관적"]
        impact["user_experience"] = min(sum(1 for ind in ux_indicators if ind in description_lower) * 2, 10)
        
        return impact
    
    def _identify_synergy_opportunities(self, idea: CreativeIdea) -> List[str]:
        """시너지 기회 식별"""
        opportunities = []
        
        # 다른 아이디어와의 조합 가능성
        for other_idea in self.idea_repository[-20:]:  # 최근 20개 아이디어만 체크
            if other_idea.id != idea.id and other_idea.domain == idea.domain:
                if self._calculate_idea_similarity(idea, other_idea) > 0.3:
                    opportunities.append(f"{other_idea.title[:30]}...과의 융합 가능성")
        
        # 기술 조합 기회
        for tech in self.creativity_seeds["technology"]:
            if tech not in idea.inspiration_sources and tech.lower() in idea.description.lower():
                opportunities.append(f"{tech} 기술과의 통합 확장")
        
        # 도메인 확장 기회
        related_domains = {
            "교육": ["헬스케어", "엔터테인먼트"],
            "헬스케어": ["교육", "웰빙"],
            "금융": ["보안", "AI"],
            "게임": ["교육", "헬스케어"]
        }
        
        if idea.domain in related_domains:
            for related_domain in related_domains[idea.domain]:
                opportunities.append(f"{related_domain} 분야로의 확장 적용")
        
        return opportunities[:5]  # 상위 5개만 반환
    
    def _enhance_implementation_steps(self, idea: CreativeIdea) -> List[str]:
        """구현 단계 개선"""
        enhanced_steps = []
        
        for step in idea.implementation_steps:
            # 단계를 더 구체화
            if len(step) < 15:  # 너무 간단한 단계
                enhanced_step = f"{step} - 상세 요구사항 분석 및 구체적 실행 계획 수립"
            else:
                enhanced_step = step
            
            enhanced_steps.append(enhanced_step)
        
        # 필수 단계 추가 (없는 경우)
        essential_steps = ["프로토타입 개발", "사용자 테스트", "피드백 수집", "성능 최적화"]
        
        for essential in essential_steps:
            if not any(essential in step for step in enhanced_steps):
                enhanced_steps.append(f"{essential} 및 검증")
        
        return enhanced_steps[:8]  # 최대 8단계로 제한
    
    def _update_creativity_metrics(self, ideas: List[CreativeIdea]):
        """창의성 지표 업데이트"""
        if not ideas:
            return
        
        # 아이디어들의 평균 점수로 지표 업데이트
        avg_creativity = sum(idea.creativity_score for idea in ideas) / len(ideas)
        avg_innovation = sum(idea.innovation_level for idea in ideas) / len(ideas)
        
        # 점진적 업데이트 (이동 평균)
        self.creativity_metrics.originality = (self.creativity_metrics.originality * 0.8 + 
                                             avg_creativity / 10 * 0.2)
        
        # 유창성 (아이디어 생성 속도)
        self.creativity_metrics.fluency = min(self.creativity_metrics.fluency * 1.01, 2.0)
        
        # 유연성 (다양한 사고 패턴 사용)
        pattern_diversity = len(set(idea.thinking_pattern for idea in ideas)) / 5
        self.creativity_metrics.flexibility = (self.creativity_metrics.flexibility * 0.9 + 
                                             pattern_diversity * 0.1)
        
        # 정교성 (아이디어의 구체성)
        avg_elaboration = sum(len(idea.implementation_steps) for idea in ideas) / len(ideas) / 8
        self.creativity_metrics.elaboration = (self.creativity_metrics.elaboration * 0.9 +
                                             avg_elaboration * 0.1)
        
        # 돌파 가능성
        breakthrough_score = avg_innovation / 10
        self.creativity_metrics.breakthrough_potential = (self.creativity_metrics.breakthrough_potential * 0.9 +
                                                        breakthrough_score * 0.1)
    
    def _creativity_monitoring_loop(self):
        """창의성 모니터링 루프 (백그라운드)"""
        while self.creativity_monitor_active:
            try:
                time.sleep(1800)  # 30분마다 실행
                
                if self.idea_repository:
                    self._analyze_creativity_trends()
                    self._identify_innovation_patterns()
                    self._suggest_creativity_improvements()
                
            except Exception as e:
                print(f"⚠️ 창의성 모니터링 오류: {e}")
                time.sleep(300)
    
    def _analyze_creativity_trends(self):
        """창의성 트렌드 분석"""
        if len(self.idea_repository) < 10:
            return
        
        recent_ideas = self.idea_repository[-20:]
        
        # 최근 아이디어들의 품질 트렌드
        avg_creativity = sum(idea.creativity_score for idea in recent_ideas) / len(recent_ideas)
        avg_feasibility = sum(idea.feasibility_score for idea in recent_ideas) / len(recent_ideas)
        avg_innovation = sum(idea.innovation_level for idea in recent_ideas) / len(recent_ideas)
        
        # 사고 패턴 분포
        pattern_distribution = {}
        for idea in recent_ideas:
            pattern = idea.thinking_pattern.value
            pattern_distribution[pattern] = pattern_distribution.get(pattern, 0) + 1
        
        # 도메인 선호도
        domain_preference = {}
        for idea in recent_ideas:
            domain = idea.domain
            domain_preference[domain] = domain_preference.get(domain, 0) + 1
        
        trend_summary = {
            "timestamp": datetime.now().isoformat(),
            "avg_creativity": avg_creativity,
            "avg_feasibility": avg_feasibility,
            "avg_innovation": avg_innovation,
            "pattern_distribution": pattern_distribution,
            "domain_preference": domain_preference
        }
        
        print(f"🎨 창의성 트렌드: 창의성 {avg_creativity:.1f}, 실현성 {avg_feasibility:.1f}, 혁신성 {avg_innovation:.1f}")
    
    def _identify_innovation_patterns(self):
        """혁신 패턴 식별"""
        high_innovation_ideas = [idea for idea in self.idea_repository if idea.innovation_level > 8.0]
        
        if len(high_innovation_ideas) >= 3:
            # 고혁신 아이디어들의 공통 패턴 분석
            common_sources = {}
            common_patterns = {}
            
            for idea in high_innovation_ideas:
                for source in idea.inspiration_sources:
                    common_sources[source] = common_sources.get(source, 0) + 1
                
                pattern = idea.thinking_pattern.value
                common_patterns[pattern] = common_patterns.get(pattern, 0) + 1
            
            # 가장 효과적인 혁신 요소들 식별
            top_sources = sorted(common_sources.items(), key=lambda x: x[1], reverse=True)[:3]
            top_patterns = sorted(common_patterns.items(), key=lambda x: x[1], reverse=True)[:2]
            
            innovation_pattern = {
                "timestamp": datetime.now().isoformat(),
                "top_innovation_sources": top_sources,
                "effective_thinking_patterns": top_patterns,
                "innovation_rate": len(high_innovation_ideas) / len(self.idea_repository)
            }
            
            self.innovation_history.append(innovation_pattern)
    
    def _suggest_creativity_improvements(self):
        """창의성 개선 제안"""
        suggestions = []
        
        # 사고 패턴 다양성 체크
        recent_patterns = [idea.thinking_pattern for idea in self.idea_repository[-10:]]
        pattern_diversity = len(set(recent_patterns)) / 5
        
        if pattern_diversity < 0.6:
            suggestions.append("더 다양한 사고 패턴 활용 권장 (래터럴, 유추적 사고 등)")
        
        # 도메인 확장 제안
        recent_domains = [idea.domain for idea in self.idea_repository[-10:]]
        domain_diversity = len(set(recent_domains)) / len(self.creativity_seeds["domains"])
        
        if domain_diversity < 0.3:
            suggestions.append("다양한 도메인으로 아이디어 확장 시도")
        
        # 혁신성 향상 제안
        avg_innovation = sum(idea.innovation_level for idea in self.idea_repository[-10:]) / 10
        if avg_innovation < 7.0:
            suggestions.append("더 급진적이고 혁신적인 아이디어 도전")
        
        if suggestions:
            print(f"💡 창의성 개선 제안: {', '.join(suggestions)}")
    
    def combine_ideas(self, idea_ids: List[str]) -> Optional[CreativeIdea]:
        """아이디어 융합"""
        if len(idea_ids) < 2:
            return None
        
        ideas_to_combine = []
        for idea_id in idea_ids:
            idea = next((idea for idea in self.idea_repository if idea.id == idea_id), None)
            if idea:
                ideas_to_combine.append(idea)
        
        if len(ideas_to_combine) < 2:
            return None
        
        # 융합된 아이디어 생성
        combined_title = " + ".join([idea.title[:20] + "..." for idea in ideas_to_combine])
        
        combined_description = f"다음 아이디어들의 혁신적 융합: {', '.join([idea.title for idea in ideas_to_combine])}. "
        combined_description += "각 아이디어의 핵심 강점을 통합하여 시너지 효과를 극대화한 혁신 솔루션."
        
        # 모든 영감 소스 통합
        all_sources = []
        for idea in ideas_to_combine:
            all_sources.extend(idea.inspiration_sources)
        
        # 모든 구현 단계 통합 및 정리
        all_steps = []
        for idea in ideas_to_combine:
            all_steps.extend(idea.implementation_steps)
        
        # 중복 제거 및 논리적 순서 정리
        unique_steps = []
        for step in all_steps:
            if step not in unique_steps:
                unique_steps.append(step)
        
        combined_idea = CreativeIdea(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            title=f"융합형 솔루션: {combined_title}",
            description=combined_description,
            creativity_score=0.0,
            feasibility_score=0.0,
            innovation_level=0.0,
            domain=ideas_to_combine[0].domain,
            thinking_pattern=ThinkingPattern.SYNTHESIS,
            inspiration_sources=list(set(all_sources)),
            implementation_steps=unique_steps[:10],
            potential_impact={},
            synergy_opportunities=[]
        )
        
        # 평가 및 개선
        enhanced_idea = self._evaluate_and_enhance_idea(combined_idea, "아이디어 융합")
        
        # 융합 보너스 적용
        enhanced_idea.creativity_score = min(enhanced_idea.creativity_score * 1.2, 10.0)
        enhanced_idea.innovation_level = min(enhanced_idea.innovation_level * 1.1, 10.0)
        
        self.idea_repository.append(enhanced_idea)
        
        return enhanced_idea
    
    def get_creativity_insights(self) -> Dict[str, Any]:
        """창의성 인사이트 반환"""
        if not self.idea_repository:
            return {"message": "아직 생성된 아이디어가 없습니다."}
        
        # 통계 계산
        total_ideas = len(self.idea_repository)
        avg_creativity = sum(idea.creativity_score for idea in self.idea_repository) / total_ideas
        avg_feasibility = sum(idea.feasibility_score for idea in self.idea_repository) / total_ideas
        avg_innovation = sum(idea.innovation_level for idea in self.idea_repository) / total_ideas
        
        # 최고 아이디어들
        top_creative_ideas = sorted(self.idea_repository, key=lambda x: x.creativity_score, reverse=True)[:3]
        top_innovative_ideas = sorted(self.idea_repository, key=lambda x: x.innovation_level, reverse=True)[:3]
        
        # 사고 패턴 분포
        pattern_distribution = {}
        for idea in self.idea_repository:
            pattern = idea.thinking_pattern.value
            pattern_distribution[pattern] = pattern_distribution.get(pattern, 0) + 1
        
        return {
            "총_아이디어_수": total_ideas,
            "평균_창의성_점수": round(avg_creativity, 1),
            "평균_실현가능성_점수": round(avg_feasibility, 1),
            "평균_혁신_수준": round(avg_innovation, 1),
            "창의성_지표": {
                "독창성": round(self.creativity_metrics.originality, 2),
                "유창성": round(self.creativity_metrics.fluency, 2),
                "유연성": round(self.creativity_metrics.flexibility, 2),
                "정교성": round(self.creativity_metrics.elaboration, 2),
                "통합능력": round(self.creativity_metrics.synthesis_ability, 2),
                "돌파가능성": round(self.creativity_metrics.breakthrough_potential, 2)
            },
            "사고패턴_분포": pattern_distribution,
            "최고_창의성_아이디어": [{"제목": idea.title, "점수": idea.creativity_score} for idea in top_creative_ideas],
            "최고_혁신성_아이디어": [{"제목": idea.title, "점수": idea.innovation_level} for idea in top_innovative_ideas],
            "혁신_히스토리_수": len(self.innovation_history),
            "다음_추천_사고패턴": self._recommend_next_thinking_pattern()
        }
    
    def _recommend_next_thinking_pattern(self) -> str:
        """다음 권장 사고 패턴"""
        if not self.idea_repository:
            return ThinkingPattern.DIVERGENT.value
        
        recent_patterns = [idea.thinking_pattern for idea in self.idea_repository[-5:]]
        pattern_counts = {}
        for pattern in recent_patterns:
            pattern_counts[pattern.value] = pattern_counts.get(pattern.value, 0) + 1
        
        # 가장 적게 사용된 패턴 추천
        all_patterns = [p.value for p in ThinkingPattern]
        unused_patterns = [p for p in all_patterns if p not in pattern_counts]
        
        if unused_patterns:
            return random.choice(unused_patterns)
        else:
            least_used = min(pattern_counts.items(), key=lambda x: x[1])
            return least_used[0]
    
    def _load_existing_ideas(self):
        """기존 아이디어 로드"""
        ideas_file = self.data_path / "creative_ideas.json"
        if ideas_file.exists():
            try:
                with open(ideas_file, 'r', encoding='utf-8') as f:
                    ideas_data = json.load(f)
                    
                for idea_data in ideas_data:
                    idea = CreativeIdea(
                        id=idea_data["id"],
                        timestamp=idea_data["timestamp"],
                        title=idea_data["title"],
                        description=idea_data["description"],
                        creativity_score=idea_data["creativity_score"],
                        feasibility_score=idea_data["feasibility_score"],
                        innovation_level=idea_data["innovation_level"],
                        domain=idea_data["domain"],
                        thinking_pattern=ThinkingPattern(idea_data["thinking_pattern"]),
                        inspiration_sources=idea_data["inspiration_sources"],
                        implementation_steps=idea_data["implementation_steps"],
                        potential_impact=idea_data["potential_impact"],
                        synergy_opportunities=idea_data["synergy_opportunities"]
                    )
                    self.idea_repository.append(idea)
                    
                print(f"💡 {len(self.idea_repository)}개의 기존 아이디어 로드 완료")
                
            except Exception as e:
                print(f"⚠️ 기존 아이디어 로드 실패: {e}")

# 전역 창의적 지능 코어 인스턴스
creative_intelligence = CreativeIntelligenceCore() 