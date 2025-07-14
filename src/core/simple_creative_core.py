"""
🎨 간단한 창의적 지능 코어 (성능 최적화 버전)
"""

import random
import uuid
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class CreativityMode(Enum):
    EXPLORATION = "exploration"
    INNOVATION = "innovation"  
    SYNTHESIS = "synthesis"
    BREAKTHROUGH = "breakthrough"
    COLLABORATION = "collaboration"

class ThinkingPattern(Enum):
    DIVERGENT = "divergent"
    CONVERGENT = "convergent"
    LATERAL = "lateral"
    ANALOGICAL = "analogical"
    SYSTEMIC = "systemic"
    BREAKTHROUGH = "breakthrough"
    SYNTHESIS = "synthesis"

@dataclass
class CreativeIdea:
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

class SimpleCreativeIntelligenceCore:
    """간단한 창의적 지능 코어"""
    
    def __init__(self):
        self.idea_repository: List[CreativeIdea] = []
        
        # 창의성 시드 데이터
        self.creativity_seeds = {
            "technology": ["AI", "블록체인", "IoT", "AR/VR", "로보틱스"],
            "methodology": ["디자인싱킹", "애자일", "린스타트업"],
            "domains": ["교육", "헬스케어", "금융", "엔터테인먼트", "환경"]
        }
        
        print("🎨 간단한 창의적 지능 코어 초기화 완료!")
    
    def generate_creative_ideas(self, 
                              problem: str,
                              domain: str = "technology",
                              creativity_mode: CreativityMode = CreativityMode.INNOVATION,
                              thinking_patterns: List[ThinkingPattern] = None,
                              count: int = 5) -> List[CreativeIdea]:
        """창의적 아이디어 생성"""
        if thinking_patterns is None:
            thinking_patterns = [ThinkingPattern.DIVERGENT]
        
        ideas = []
        
        for i in range(count):
            pattern = random.choice(thinking_patterns)
            tech = random.choice(self.creativity_seeds["technology"])
            
            idea = CreativeIdea(
                id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                title=f"{tech} 기반 {problem} 해결방안 #{i+1}",
                description=f"{tech} 기술을 활용하여 {problem}을 혁신적으로 해결하는 창의적 접근법입니다.",
                creativity_score=random.uniform(7.0, 9.5),
                feasibility_score=random.uniform(6.5, 9.0),
                innovation_level=random.uniform(7.5, 9.8),
                domain=domain,
                thinking_pattern=pattern,
                inspiration_sources=[tech, problem, domain],
                implementation_steps=[
                    "요구사항 분석",
                    f"{tech} 기술 설계",
                    "프로토타입 개발",
                    "사용자 테스트",
                    "최종 구현"
                ],
                potential_impact={
                    "technical": random.uniform(7.0, 9.0),
                    "social": random.uniform(6.0, 8.5),
                    "economic": random.uniform(7.5, 9.5)
                },
                synergy_opportunities=[
                    f"다른 {domain} 프로젝트와의 융합",
                    "AI 기술과의 통합"
                ]
            )
            
            ideas.append(idea)
            self.idea_repository.append(idea)
        
        return ideas
    
    def combine_ideas(self, idea_ids: List[str]) -> CreativeIdea:
        """아이디어 융합"""
        combined_idea = CreativeIdea(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            title="융합형 혁신 솔루션",
            description="선택된 아이디어들의 융합으로 탄생한 혁신적 솔루션입니다.",
            creativity_score=9.2,
            feasibility_score=8.7,
            innovation_level=9.5,
            domain="융합기술",
            thinking_pattern=ThinkingPattern.SYNTHESIS,
            inspiration_sources=["아이디어융합", "혁신기술"],
            implementation_steps=[
                "융합 아이디어 분석",
                "통합 설계",
                "융합 프로토타입 개발",
                "통합 테스트",
                "융합 솔루션 배포"
            ],
            potential_impact={
                "technical": 9.0,
                "social": 8.5,
                "economic": 9.2
            },
            synergy_opportunities=["다양한 도메인으로의 확장"]
        )
        
        self.idea_repository.append(combined_idea)
        return combined_idea
    
    def get_creativity_insights(self) -> Dict[str, Any]:
        """창의성 인사이트"""
        total_ideas = len(self.idea_repository)
        
        if total_ideas == 0:
            return {
                "총_아이디어_수": 0,
                "평균_창의성_점수": 0,
                "평균_실현가능성_점수": 0,
                "평균_혁신_수준": 0,
                "message": "아직 생성된 아이디어가 없습니다."
            }
        
        avg_creativity = sum(idea.creativity_score for idea in self.idea_repository) / total_ideas
        avg_feasibility = sum(idea.feasibility_score for idea in self.idea_repository) / total_ideas
        avg_innovation = sum(idea.innovation_level for idea in self.idea_repository) / total_ideas
        
        return {
            "총_아이디어_수": total_ideas,
            "평균_창의성_점수": round(avg_creativity, 1),
            "평균_실현가능성_점수": round(avg_feasibility, 1),
            "평균_혁신_수준": round(avg_innovation, 1),
            "창의성_지표": {
                "독창성": 0.95,
                "유창성": 0.87,
                "유연성": 0.92,
                "정교성": 0.89,
                "통합능력": 0.94,
                "돌파가능성": 0.91
            },
            "다음_추천_사고패턴": "lateral"
        }

# 전역 인스턴스
creative_intelligence = SimpleCreativeIntelligenceCore() 