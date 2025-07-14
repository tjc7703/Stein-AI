"""
🎮 Stein AI 마케팅 마스터 게임 시스템
30일 과정의 게임형 마케팅 학습 프로그램
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import random
from pathlib import Path

class MissionType(Enum):
    """미션 타입"""
    THEORY = "theory"           # 이론 학습
    PRACTICE = "practice"       # 실습 과제
    QUIZ = "quiz"              # 퀴즈
    PROJECT = "project"         # 프로젝트
    CHALLENGE = "challenge"    # 도전 과제

class DifficultyLevel(Enum):
    """난이도 레벨"""
    BEGINNER = "beginner"       # 초급
    INTERMEDIATE = "intermediate"  # 중급
    ADVANCED = "advanced"       # 고급
    EXPERT = "expert"          # 전문가

@dataclass
class Mission:
    """미션 데이터 클래스"""
    id: str
    day: int
    title: str
    description: str
    mission_type: MissionType
    difficulty: DifficultyLevel
    content: Dict[str, Any]
    rewards: Dict[str, Any]
    requirements: List[str]
    completed: bool = False
    score: int = 0
    completed_at: Optional[str] = None

@dataclass
class PlayerProgress:
    """플레이어 진행 상황"""
    current_day: int = 1
    total_score: int = 0
    completed_missions: int = 0
    current_streak: int = 0
    max_streak: int = 0
    badges: Optional[List[str]] = None
    skills: Optional[Dict[str, int]] = None
    
    def __post_init__(self):
        if self.badges is None:
            self.badges = []
        if self.skills is None:
            self.skills = {
                "마케팅_기초": 0,
                "브랜딩": 0,
                "디지털_마케팅": 0,
                "콘텐츠_마케팅": 0,
                "소셜_미디어": 0,
                "SEO": 0,
                "광고": 0,
                "데이터_분석": 0,
                "고객_관리": 0,
                "전략_수립": 0
            }

class MarketingLearningGame:
    """마케팅 학습 게임 메인 클래스"""
    
    def __init__(self):
        self.missions = self._create_missions()
        self.player_progress = PlayerProgress()
        self.game_data_path = Path("data/marketing_game")
        self.game_data_path.mkdir(parents=True, exist_ok=True)
        
    def _create_missions(self) -> List[Mission]:
        """30일 마케팅 학습 미션 생성"""
        missions = []
        
        # 1-5일: 마케팅 기초
        missions.extend([
            Mission(
                id="day_1_1",
                day=1,
                title="🎯 마케팅의 정의와 목적",
                description="마케팅의 기본 개념과 목적을 이해하고, 실제 사례를 분석해보세요.",
                mission_type=MissionType.THEORY,
                difficulty=DifficultyLevel.BEGINNER,
                content={
                    "theory": {
                        "title": "마케팅이란?",
                        "content": """
                        마케팅은 고객의 니즈를 파악하고, 제품/서비스를 통해 가치를 전달하는 과정입니다.
                        
                        📚 핵심 개념:
                        • 4P (Product, Price, Place, Promotion)
                        • 고객 가치 창출
                        • 시장 조사와 분석
                        • 브랜드 구축
                        
                        🎯 학습 목표:
                        • 마케팅의 정의와 역할 이해
                        • 4P 프레임워크 활용법
                        • 고객 중심 사고 방식
                        """,
                        "examples": [
                            "애플의 제품 마케팅 전략",
                            "스타벅스의 브랜드 경험",
                            "테슬라의 혁신적 마케팅"
                        ]
                    },
                    "quiz": {
                        "questions": [
                            {
                                "question": "마케팅 4P 중 'Product'에 해당하지 않는 것은?",
                                "options": ["제품 품질", "브랜드", "가격", "디자인"],
                                "correct": 2,
                                "explanation": "가격은 Price에 해당합니다."
                            },
                            {
                                "question": "고객 가치를 창출하는 가장 중요한 요소는?",
                                "options": ["낮은 가격", "고객 니즈 이해", "광고", "유통"],
                                "correct": 1,
                                "explanation": "고객의 니즈를 정확히 파악하는 것이 핵심입니다."
                            }
                        ]
                    }
                },
                rewards={"score": 100, "skill_points": {"마케팅_기초": 20}},
                requirements=[]
            ),
            Mission(
                id="day_1_2",
                day=1,
                title="📊 시장 조사 실습",
                description="가상의 제품에 대한 시장 조사를 수행하고 보고서를 작성하세요.",
                mission_type=MissionType.PRACTICE,
                difficulty=DifficultyLevel.BEGINNER,
                content={
                    "scenario": {
                        "title": "새로운 커피 브랜드 런칭",
                        "description": "당신은 새로운 프리미엄 커피 브랜드의 마케팅 매니저입니다.",
                        "tasks": [
                            "경쟁사 분석 (스타벅스, 투썸플레이스, 메가MGC)",
                            "타겟 고객 프로파일 작성",
                            "SWOT 분석 수행",
                            "시장 기회 분석"
                        ]
                    },
                    "template": {
                        "market_research": "시장 조사 템플릿 제공",
                        "competitor_analysis": "경쟁사 분석 프레임워크",
                        "customer_profile": "고객 프로파일 템플릿"
                    }
                },
                rewards={"score": 150, "skill_points": {"마케팅_기초": 30, "데이터_분석": 20}},
                requirements=["day_1_1"]
            )
        ])
        
        # 2일차: 브랜딩 기초
        missions.extend([
            Mission(
                id="day_2_1",
                day=2,
                title="🏷️ 브랜드 아이덴티티 구축",
                description="브랜드의 핵심 가치와 아이덴티티를 정의하고 시각적 요소를 설계하세요.",
                mission_type=MissionType.THEORY,
                difficulty=DifficultyLevel.BEGINNER,
                content={
                    "theory": {
                        "title": "브랜딩의 핵심",
                        "content": """
                        브랜딩은 고객의 마음속에 특별한 위치를 만드는 과정입니다.
                        
                        🎨 브랜드 요소:
                        • 브랜드 비전과 미션
                        • 브랜드 가치와 성격
                        • 로고와 시각적 아이덴티티
                        • 브랜드 메시지와 톤앤보이스
                        
                        💡 성공 사례:
                        • 나이키: "Just Do It"
                        • 애플: 혁신과 심플함
                        • 코카콜라: 행복과 연결
                        """,
                        "examples": [
                            "나이키의 브랜드 스토리",
                            "애플의 디자인 철학",
                            "코카콜라의 감정적 연결"
                        ]
                    }
                },
                rewards={"score": 120, "skill_points": {"브랜딩": 25}},
                requirements=["day_1_1", "day_1_2"]
            )
        ])
        
        # 3-7일: 디지털 마케팅 기초
        for day in range(3, 8):
            missions.extend([
                Mission(
                    id=f"day_{day}_1",
                    day=day,
                    title=f"🌐 디지털 마케팅 Day {day}",
                    description=f"디지털 마케팅의 핵심 요소들을 학습하고 실습합니다.",
                    mission_type=MissionType.THEORY,
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    content={
                        "topics": [
                            "소셜 미디어 마케팅",
                            "콘텐츠 마케팅",
                            "이메일 마케팅",
                            "SEO/SEM",
                            "인플루언서 마케팅"
                        ][day-3],
                        "practical_exercises": [
                            "소셜 미디어 캠페인 기획",
                            "블로그 콘텐츠 작성",
                            "이메일 시퀀스 설계",
                            "키워드 리서치",
                            "인플루언서 협업 계획"
                        ][day-3]
                    },
                    rewards={"score": 150, "skill_points": {"디지털_마케팅": 30}},
                    requirements=[f"day_{day-1}_1"] if day > 3 else ["day_2_1"]
                )
            ])
        
        # 8-12일: 고급 마케팅 전략
        for day in range(8, 13):
            missions.extend([
                Mission(
                    id=f"day_{day}_1",
                    day=day,
                    title=f"🎯 고급 마케팅 전략 Day {day}",
                    description=f"고급 마케팅 전략과 데이터 분석을 학습합니다.",
                    mission_type=MissionType.PROJECT,
                    difficulty=DifficultyLevel.ADVANCED,
                    content={
                        "strategies": [
                            "고객 여정 맵 작성",
                            "퍼널 분석과 최적화",
                            "A/B 테스트 설계",
                            "ROI 분석과 예측",
                            "크로스 채널 마케팅"
                        ][day-8],
                        "tools": [
                            "Google Analytics",
                            "Facebook Ads Manager",
                            "Mailchimp",
                            "HubSpot",
                            "Tableau"
                        ][day-8]
                    },
                    rewards={"score": 200, "skill_points": {"전략_수립": 40, "데이터_분석": 30}},
                    requirements=[f"day_{day-1}_1"] if day > 8 else ["day_7_1"]
                )
            ])
        
        # 13-20일: 전문가 수준 실습
        for day in range(13, 21):
            missions.extend([
                Mission(
                    id=f"day_{day}_1",
                    day=day,
                    title=f"🚀 전문가 마케팅 실습 Day {day}",
                    description=f"실제 비즈니스 환경에서 마케팅 전략을 수립하고 실행합니다.",
                    mission_type=MissionType.CHALLENGE,
                    difficulty=DifficultyLevel.EXPERT,
                    content={
                        "real_world_scenarios": [
                            "스타트업 마케팅 전략 수립",
                            "글로벌 마케팅 캠페인 기획",
                            "브랜드 리포지셔닝",
                            "위기 관리 마케팅",
                            "M&A 후 브랜드 통합",
                            "신제품 런칭 전략",
                            "시즌별 마케팅 캠페인",
                            "고객 충성도 프로그램"
                        ][day-13]
                    },
                    rewards={"score": 300, "skill_points": {"전략_수립": 50, "고객_관리": 40}},
                    requirements=[f"day_{day-1}_1"] if day > 13 else ["day_12_1"]
                )
            ])
        
        # 21-30일: 마스터 프로젝트
        for day in range(21, 31):
            missions.extend([
                Mission(
                    id=f"day_{day}_1",
                    day=day,
                    title=f"🏆 마스터 프로젝트 Day {day}",
                    description=f"종합적인 마케팅 마스터 프로젝트를 수행합니다.",
                    mission_type=MissionType.PROJECT,
                    difficulty=DifficultyLevel.EXPERT,
                    content={
                        "master_projects": [
                            "전체 마케팅 전략 수립",
                            "브랜드 전략 개발",
                            "디지털 마케팅 로드맵",
                            "고객 경험 설계",
                            "마케팅 자동화 구축",
                            "성과 측정 시스템",
                            "팀 관리와 리더십",
                            "혁신적 마케팅 아이디어",
                            "지속가능한 마케팅",
                            "미래 마케팅 트렌드"
                        ][day-21]
                    },
                    rewards={"score": 500, "skill_points": {"전략_수립": 100, "브랜딩": 80}},
                    requirements=[f"day_{day-1}_1"] if day > 21 else ["day_20_1"]
                )
            ])
        
        return missions
    
    async def start_game(self) -> Dict[str, Any]:
        """게임 시작"""
        return {
            "message": "🎮 마케팅 마스터 게임을 시작합니다!",
            "total_missions": len(self.missions),
            "current_day": self.player_progress.current_day,
            "total_score": self.player_progress.total_score,
            "next_mission": self.get_next_mission()
        }
    
    def get_next_mission(self) -> Optional[Mission]:
        """다음 미션 가져오기"""
        available_missions = [
            mission for mission in self.missions
            if mission.day == self.player_progress.current_day
            and not mission.completed
            and all(req in [m.id for m in self.missions if m.completed] 
                   for req in mission.requirements)
        ]
        return available_missions[0] if available_missions else None
    
    async def complete_mission(self, mission_id: str, answers: Dict[str, Any] = None) -> Dict[str, Any]:
        """미션 완료"""
        mission = next((m for m in self.missions if m.id == mission_id), None)
        if not mission:
            return {"error": "미션을 찾을 수 없습니다."}
        
        if mission.completed:
            return {"error": "이미 완료된 미션입니다."}
        
        # 미션 완료 처리
        mission.completed = True
        mission.completed_at = datetime.now().isoformat()
        
        # 점수 계산
        base_score = mission.rewards["score"]
        if answers:
            # 답변에 따른 추가 점수 계산
            correct_answers = self._evaluate_answers(mission, answers)
            mission.score = base_score + correct_answers * 10
        else:
            mission.score = base_score
        
        # 플레이어 진행 상황 업데이트
        self.player_progress.total_score += mission.score
        self.player_progress.completed_missions += 1
        self.player_progress.current_streak += 1
        
        # 스킬 포인트 추가
        for skill, points in mission.rewards.get("skill_points", {}).items():
            self.player_progress.skills[skill] += points
        
        # 배지 획득 체크
        new_badges = self._check_badges()
        
        # 다음 날로 진행
        if self._can_advance_day():
            self.player_progress.current_day += 1
            self.player_progress.max_streak = max(
                self.player_progress.max_streak,
                self.player_progress.current_streak
            )
        
        # 진행 상황 저장
        await self._save_progress()
        
        return {
            "success": True,
            "mission_completed": mission.title,
            "score_earned": mission.score,
            "total_score": self.player_progress.total_score,
            "new_badges": new_badges,
            "skills_updated": mission.rewards.get("skill_points", {}),
            "next_mission": self.get_next_mission()
        }
    
    def _evaluate_answers(self, mission: Mission, answers: Dict[str, Any]) -> int:
        """답변 평가"""
        if mission.mission_type == MissionType.QUIZ:
            correct_count = 0
            for question in mission.content.get("quiz", {}).get("questions", []):
                user_answer = answers.get(f"question_{question['correct']}")
                if user_answer == question['correct']:
                    correct_count += 1
            return correct_count
        return 0
    
    def _check_badges(self) -> List[str]:
        """배지 획득 체크"""
        new_badges = []
        
        # 첫 미션 완료
        if self.player_progress.completed_missions == 1:
            new_badges.append("🎯 첫 걸음")
        
        # 5일 연속 완료
        if self.player_progress.current_streak >= 5:
            new_badges.append("🔥 연속 완주")
        
        # 10개 미션 완료
        if self.player_progress.completed_missions >= 10:
            new_badges.append("📚 열심히 학습")
        
        # 스킬 마스터
        for skill, level in self.player_progress.skills.items():
            if level >= 100 and f"🏆 {skill} 마스터" not in self.player_progress.badges:
                new_badges.append(f"🏆 {skill} 마스터")
        
        self.player_progress.badges.extend(new_badges)
        return new_badges
    
    def _can_advance_day(self) -> bool:
        """다음 날로 진행 가능한지 체크"""
        current_day_missions = [
            m for m in self.missions 
            if m.day == self.player_progress.current_day
        ]
        completed_day_missions = [
            m for m in current_day_missions 
            if m.completed
        ]
        return len(completed_day_missions) >= len(current_day_missions)
    
    async def _save_progress(self):
        """진행 상황 저장"""
        progress_data = {
            "player_progress": asdict(self.player_progress),
            "missions": [asdict(m) for m in self.missions],
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.game_data_path / "progress.json", "w", encoding="utf-8") as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)
    
    async def load_progress(self):
        """진행 상황 로드"""
        progress_file = self.game_data_path / "progress.json"
        if progress_file.exists():
            with open(progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.player_progress = PlayerProgress(**data["player_progress"])
            
            for mission_data in data["missions"]:
                mission = Mission(**mission_data)
                mission.mission_type = MissionType(mission.mission_type)
                mission.difficulty = DifficultyLevel(mission.difficulty)
                
                # 기존 미션 업데이트
                for i, existing_mission in enumerate(self.missions):
                    if existing_mission.id == mission.id:
                        self.missions[i] = mission
                        break
    
    def get_game_status(self) -> Dict[str, Any]:
        """게임 상태 조회"""
        next_mission = self.get_next_mission()
        return {
            "current_day": self.player_progress.current_day,
            "total_score": self.player_progress.total_score,
            "completed_missions": self.player_progress.completed_missions,
            "current_streak": self.player_progress.current_streak,
            "max_streak": self.player_progress.max_streak,
            "badges": self.player_progress.badges,
            "skills": self.player_progress.skills,
            "next_mission": {
                "title": next_mission.title,
                "description": next_mission.description,
                "day": next_mission.day,
                "mission_type": next_mission.mission_type.value,
                "difficulty": next_mission.difficulty.value
            } if next_mission else {},
            "total_missions": len(self.missions),
            "completion_rate": (self.player_progress.completed_missions / len(self.missions)) * 100
        }

# 게임 인스턴스 생성
marketing_game = MarketingLearningGame() 