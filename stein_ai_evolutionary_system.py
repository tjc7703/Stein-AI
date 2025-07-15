#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stein AI 진화형 시스템
패턴과 효과성을 지속적으로 높이는 자가학습 AI 시스템
"""

import re
import json
import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import random

@dataclass
class EvolutionaryPattern:
    """진화형 패턴"""
    pattern_id: str
    original_request: str
    enhanced_response: str
    effectiveness_score: float
    success_rate: float
    usage_count: int
    mutation_count: int
    generation: int
    fitness_score: float
    context_patterns: List[str]
    created_at: str
    last_used: str
    adaptation_history: List[Dict[str, Any]]

@dataclass
class EvolutionMetrics:
    """진화 메트릭"""
    total_patterns: int
    average_fitness: float
    best_pattern_id: str
    evolution_generation: int
    mutation_rate: float
    adaptation_success_rate: float
    learning_progress: float

class SteinAIEvolutionarySystem:
    """Stein AI 진화형 시스템"""
    
    def __init__(self):
        self.evolutionary_patterns = {}
        self.generation_counter = 0
        self.mutation_rate = 0.1
        self.crossover_rate = 0.3
        self.fitness_threshold = 0.8
        self.max_population = 50
        self.stein_preferences = self._load_evolutionary_preferences()
        self.learning_history = []
        self.adaptation_engine = self._initialize_adaptation_engine()
        self.evolution_metrics = self._initialize_evolution_metrics()
        
    def _load_evolutionary_preferences(self) -> Dict[str, Any]:
        """진화형 선호도 로드"""
        return {
            "learning_rate": 0.15,
            "mutation_intensity": 0.2,
            "crossover_probability": 0.3,
            "fitness_threshold": 0.8,
            "generation_size": 20,
            "survival_rate": 0.7,
            "adaptation_speed": 0.1,
            "innovation_bonus": 0.2
        }
    
    def _initialize_adaptation_engine(self) -> Dict[str, Any]:
        """적응 엔진 초기화"""
        return {
            "pattern_recognition": {
                "keyword_evolution": defaultdict(float),
                "context_evolution": defaultdict(float),
                "style_evolution": defaultdict(float)
            },
            "mutation_strategies": {
                "keyword_mutation": 0.3,
                "context_mutation": 0.3,
                "style_mutation": 0.4
            },
            "fitness_calculation": {
                "effectiveness_weight": 0.4,
                "success_rate_weight": 0.3,
                "adaptability_weight": 0.3
            }
        }
    
    def _initialize_evolution_metrics(self) -> EvolutionMetrics:
        """진화 메트릭 초기화"""
        return EvolutionMetrics(
            total_patterns=0,
            average_fitness=0.0,
            best_pattern_id="",
            evolution_generation=0,
            mutation_rate=0.1,
            adaptation_success_rate=0.0,
            learning_progress=0.0
        )
    
    def create_initial_population(self):
        """초기 패턴 집단 생성"""
        base_patterns = [
            {
                "request": "코드 수정해줘",
                "response": "코드 리뷰하면서 개선점을 찾아보자. 성능, 가독성, 보안, 테스트 커버리지를 모두 고려해서 최적화해줘.",
                "effectiveness": 0.9,
                "context": ["code_review", "optimization"]
            },
            {
                "request": "버그 수정",
                "response": "이 에러를 함께 분석해보자. 원인을 찾고 방어 코드도 추가해서 비슷한 문제가 재발하지 않도록 해줘.",
                "effectiveness": 0.95,
                "context": ["bug_fixing", "debugging"]
            },
            {
                "request": "기능 추가",
                "response": "이 기능을 TDD 방식으로 구현해줘. 먼저 테스트를 작성하고, 그 다음 구현하고, 마지막에 통합 테스트도 추가해줘.",
                "effectiveness": 0.85,
                "context": ["feature_development", "tdd"]
            },
            {
                "request": "최적화",
                "response": "성능 프로파일링을 해보고 병목 지점을 찾아서 최적화해줘. 메모리 사용량과 실행 시간을 모두 고려해줘.",
                "effectiveness": 0.88,
                "context": ["performance", "optimization"]
            },
            {
                "request": "테스트",
                "response": "단위 테스트, 통합 테스트, E2E 테스트를 모두 작성해줘. 테스트 커버리지 90% 이상을 목표로 해줘.",
                "effectiveness": 0.92,
                "context": ["testing", "coverage"]
            }
        ]
        
        for i, pattern_data in enumerate(base_patterns):
            pattern_id = f"pattern_{i+1}_gen_0"
            pattern = EvolutionaryPattern(
                pattern_id=pattern_id,
                original_request=pattern_data["request"],
                enhanced_response=pattern_data["response"],
                effectiveness_score=pattern_data["effectiveness"],
                success_rate=pattern_data["effectiveness"],
                usage_count=0,
                mutation_count=0,
                generation=0,
                fitness_score=pattern_data["effectiveness"],
                context_patterns=pattern_data["context"],
                created_at=datetime.now().isoformat(),
                last_used="",
                adaptation_history=[]
            )
            
            self.evolutionary_patterns[pattern_id] = pattern
        
        self.evolution_metrics.total_patterns = len(self.evolutionary_patterns)
        self.evolution_metrics.evolution_generation = 0
    
    def evolve_patterns(self):
        """패턴 진화"""
        if len(self.evolutionary_patterns) < 5:
            return
        
        # 현재 세대의 패턴들
        current_patterns = list(self.evolutionary_patterns.values())
        
        # 적합도 기반 선택
        selected_patterns = self._select_fittest_patterns(current_patterns)
        
        # 새로운 세대 생성
        new_generation = self._create_new_generation(selected_patterns)
        
        # 돌연변이 적용
        mutated_patterns = self._apply_mutations(new_generation)
        
        # 교차 적용
        crossover_patterns = self._apply_crossover(mutated_patterns)
        
        # 새로운 패턴들을 시스템에 추가
        for pattern in crossover_patterns:
            self.evolutionary_patterns[pattern.pattern_id] = pattern
        
        # 진화 메트릭 업데이트
        self._update_evolution_metrics()
        
        self.generation_counter += 1
    
    def _select_fittest_patterns(self, patterns: List[EvolutionaryPattern]) -> List[EvolutionaryPattern]:
        """가장 적합한 패턴 선택"""
        # 적합도 순으로 정렬
        sorted_patterns = sorted(patterns, key=lambda p: p.fitness_score, reverse=True)
        
        # 상위 70% 선택
        selection_count = int(len(sorted_patterns) * self.stein_preferences["survival_rate"])
        return sorted_patterns[:selection_count]
    
    def _create_new_generation(self, selected_patterns: List[EvolutionaryPattern]) -> List[EvolutionaryPattern]:
        """새로운 세대 생성"""
        new_generation = []
        
        for i in range(self.stein_preferences["generation_size"]):
            # 부모 패턴 선택
            parent1 = random.choice(selected_patterns)
            parent2 = random.choice(selected_patterns)
            
            # 자식 패턴 생성
            child = self._create_child_pattern(parent1, parent2, i)
            new_generation.append(child)
        
        return new_generation
    
    def _create_child_pattern(self, parent1: EvolutionaryPattern, parent2: EvolutionaryPattern, index: int) -> EvolutionaryPattern:
        """자식 패턴 생성"""
        # 교차점 결정
        crossover_point = random.randint(0, 1)
        
        if crossover_point == 0:
            # 부모1의 요청 + 부모2의 응답
            original_request = parent1.original_request
            enhanced_response = parent2.enhanced_response
        else:
            # 부모2의 요청 + 부모1의 응답
            original_request = parent2.original_request
            enhanced_response = parent1.enhanced_response
        
        # 컨텍스트 패턴 결합
        context_patterns = list(set(parent1.context_patterns + parent2.context_patterns))
        
        # 적합도 계산
        fitness_score = (parent1.fitness_score + parent2.fitness_score) / 2
        
        child = EvolutionaryPattern(
            pattern_id=f"pattern_{len(self.evolutionary_patterns)+1}_gen_{self.generation_counter+1}",
            original_request=original_request,
            enhanced_response=enhanced_response,
            effectiveness_score=fitness_score,
            success_rate=fitness_score,
            usage_count=0,
            mutation_count=0,
            generation=self.generation_counter + 1,
            fitness_score=fitness_score,
            context_patterns=context_patterns,
            created_at=datetime.now().isoformat(),
            last_used="",
            adaptation_history=[]
        )
        
        return child
    
    def _apply_mutations(self, patterns: List[EvolutionaryPattern]) -> List[EvolutionaryPattern]:
        """돌연변이 적용"""
        mutated_patterns = []
        
        for pattern in patterns:
            if random.random() < self.mutation_rate:
                # 돌연변이 적용
                mutated_pattern = self._mutate_pattern(pattern)
                mutated_patterns.append(mutated_pattern)
            else:
                mutated_patterns.append(pattern)
        
        return mutated_patterns
    
    def _mutate_pattern(self, pattern: EvolutionaryPattern) -> EvolutionaryPattern:
        """패턴 돌연변이"""
        mutation_type = random.choice(["keyword", "context", "style"])
        
        if mutation_type == "keyword":
            # 키워드 돌연변이
            enhanced_response = self._mutate_keywords(pattern.enhanced_response)
        elif mutation_type == "context":
            # 컨텍스트 돌연변이
            context_patterns = self._mutate_context_patterns(pattern.context_patterns)
            enhanced_response = pattern.enhanced_response
        else:
            # 스타일 돌연변이
            enhanced_response = self._mutate_style(pattern.enhanced_response)
            context_patterns = pattern.context_patterns
        
        # 적합도 조정
        fitness_adjustment = random.uniform(-0.1, 0.1)
        new_fitness = max(0.0, min(1.0, pattern.fitness_score + fitness_adjustment))
        
        mutated_pattern = EvolutionaryPattern(
            pattern_id=pattern.pattern_id + "_mut",
            original_request=pattern.original_request,
            enhanced_response=enhanced_response,
            effectiveness_score=new_fitness,
            success_rate=new_fitness,
            usage_count=pattern.usage_count,
            mutation_count=pattern.mutation_count + 1,
            generation=pattern.generation,
            fitness_score=new_fitness,
            context_patterns=context_patterns,
            created_at=datetime.now().isoformat(),
            last_used=pattern.last_used,
            adaptation_history=pattern.adaptation_history.copy()
        )
        
        return mutated_pattern
    
    def _mutate_keywords(self, response: str) -> str:
        """키워드 돌연변이"""
        stein_keywords = [
            "함께", "협업", "분석", "최적화", "테스트", "보안", "성능",
            "문서화", "리뷰", "개선", "구현", "설계", "검증", "모니터링"
        ]
        
        # 랜덤하게 키워드 추가/교체
        if random.random() < 0.5:
            # 키워드 추가
            new_keyword = random.choice(stein_keywords)
            if new_keyword not in response:
                response += f" {new_keyword}도 고려해서 구현해줘."
        else:
            # 기존 키워드 교체
            for keyword in stein_keywords:
                if keyword in response:
                    replacement = random.choice([k for k in stein_keywords if k != keyword])
                    response = response.replace(keyword, replacement)
                    break
        
        return response
    
    def _mutate_context_patterns(self, context_patterns: List[str]) -> List[str]:
        """컨텍스트 패턴 돌연변이"""
        new_contexts = [
            "python_stack", "javascript_stack", "react_stack", "fastapi_stack",
            "high_complexity", "low_complexity", "high_urgency", "security_focus"
        ]
        
        # 랜덤하게 컨텍스트 추가/교체
        if random.random() < 0.3:
            new_context = random.choice(new_contexts)
            if new_context not in context_patterns:
                context_patterns.append(new_context)
        
        return context_patterns
    
    def _mutate_style(self, response: str) -> str:
        """스타일 돌연변이"""
        style_variations = [
            "Stein님 스타일에 맞춰서",
            "최고 효율적으로",
            "혁신적인 방식으로",
            "Stein님만의 방식으로",
            "창의적으로"
        ]
        
        # 스타일 변형 적용
        if random.random() < 0.4:
            style_prefix = random.choice(style_variations)
            response = f"{style_prefix} {response}"
        
        return response
    
    def _apply_crossover(self, patterns: List[EvolutionaryPattern]) -> List[EvolutionaryPattern]:
        """교차 적용"""
        crossover_patterns = []
        
        for i in range(0, len(patterns), 2):
            if i + 1 < len(patterns):
                # 두 패턴 교차
                child1, child2 = self._crossover_patterns(patterns[i], patterns[i+1])
                crossover_patterns.extend([child1, child2])
            else:
                crossover_patterns.append(patterns[i])
        
        return crossover_patterns
    
    def _crossover_patterns(self, pattern1: EvolutionaryPattern, pattern2: EvolutionaryPattern) -> Tuple[EvolutionaryPattern, EvolutionaryPattern]:
        """패턴 교차"""
        # 요청과 응답을 교차
        child1 = EvolutionaryPattern(
            pattern_id=f"{pattern1.pattern_id}_cross1",
            original_request=pattern1.original_request,
            enhanced_response=pattern2.enhanced_response,
            effectiveness_score=(pattern1.effectiveness_score + pattern2.effectiveness_score) / 2,
            success_rate=(pattern1.success_rate + pattern2.success_rate) / 2,
            usage_count=0,
            mutation_count=0,
            generation=self.generation_counter + 1,
            fitness_score=(pattern1.fitness_score + pattern2.fitness_score) / 2,
            context_patterns=pattern1.context_patterns + pattern2.context_patterns,
            created_at=datetime.now().isoformat(),
            last_used="",
            adaptation_history=[]
        )
        
        child2 = EvolutionaryPattern(
            pattern_id=f"{pattern2.pattern_id}_cross2",
            original_request=pattern2.original_request,
            enhanced_response=pattern1.enhanced_response,
            effectiveness_score=(pattern1.effectiveness_score + pattern2.effectiveness_score) / 2,
            success_rate=(pattern1.success_rate + pattern2.success_rate) / 2,
            usage_count=0,
            mutation_count=0,
            generation=self.generation_counter + 1,
            fitness_score=(pattern1.fitness_score + pattern2.fitness_score) / 2,
            context_patterns=pattern2.context_patterns + pattern1.context_patterns,
            created_at=datetime.now().isoformat(),
            last_used="",
            adaptation_history=[]
        )
        
        return child1, child2
    
    def find_best_pattern(self, request: str) -> Optional[EvolutionaryPattern]:
        """최적 패턴 찾기"""
        if not self.evolutionary_patterns:
            return None
        
        request_lower = request.lower()
        best_pattern = None
        best_score = 0.0
        
        for pattern in self.evolutionary_patterns.values():
            # 요청 유사도 계산
            similarity = self._calculate_request_similarity(request_lower, pattern.original_request.lower())
            
            # 적합도와 유사도의 가중 평균
            score = (similarity * 0.6 + pattern.fitness_score * 0.4)
            
            if score > best_score:
                best_score = score
                best_pattern = pattern
        
        return best_pattern if best_score > 0.3 else None
    
    def _calculate_request_similarity(self, request1: str, request2: str) -> float:
        """요청 유사도 계산"""
        words1 = set(request1.split())
        words2 = set(request2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def learn_from_interaction(self, request: str, response: str, satisfaction: float):
        """상호작용에서 학습"""
        # 학습 기록 추가
        learning_record = {
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "response": response,
            "satisfaction": satisfaction,
            "pattern_used": None
        }
        
        # 사용된 패턴 찾기
        best_pattern = self.find_best_pattern(request)
        if best_pattern:
            learning_record["pattern_used"] = best_pattern.pattern_id
            best_pattern.usage_count += 1
            best_pattern.last_used = datetime.now().isoformat()
            
            # 성공률 업데이트
            best_pattern.success_rate = (best_pattern.success_rate * 0.9 + satisfaction * 0.1)
            best_pattern.fitness_score = (best_pattern.fitness_score * 0.9 + satisfaction * 0.1)
        
        self.learning_history.append(learning_record)
        
        # 진화 조건 확인
        if len(self.learning_history) % 10 == 0:  # 10번의 상호작용마다
            self.evolve_patterns()
    
    def generate_evolutionary_response(self, request: str) -> Dict[str, Any]:
        """진화형 응답 생성"""
        best_pattern = self.find_best_pattern(request)
        
        if best_pattern:
            # 패턴 기반 응답
            enhanced_response = self._adapt_pattern_to_request(request, best_pattern)
            confidence = best_pattern.fitness_score
            pattern_id = best_pattern.pattern_id
        else:
            # 새로운 패턴 생성
            enhanced_response = self._generate_new_pattern_response(request)
            confidence = 0.6
            pattern_id = "new_pattern"
        
        return {
            "original": request,
            "enhanced": enhanced_response,
            "confidence": confidence,
            "pattern_id": pattern_id,
            "generation": self.generation_counter,
            "evolution_metrics": self._get_current_metrics()
        }
    
    def _adapt_pattern_to_request(self, request: str, pattern: EvolutionaryPattern) -> str:
        """요청에 맞게 패턴 적응"""
        # 기본 응답
        response = pattern.enhanced_response
        
        # 컨텍스트 적응
        context_patterns = self._extract_context_from_request(request)
        
        for context in context_patterns:
            if context == "python_stack":
                response += " Python의 best practice를 적용해서 구현해줘."
            elif context == "react_stack":
                response += " React Hook과 TypeScript를 활용해서 구현해줘."
            elif context == "high_complexity":
                response += " 복잡한 로직을 모듈화하고 설계 패턴을 적용해줘."
            elif context == "high_urgency":
                response += " 빠른 해결을 위해 핵심 기능부터 우선 구현해줘."
        
        return response
    
    def _extract_context_from_request(self, request: str) -> List[str]:
        """요청에서 컨텍스트 추출"""
        context_patterns = []
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["python", "파이썬"]):
            context_patterns.append("python_stack")
        if any(word in request_lower for word in ["react", "리액트"]):
            context_patterns.append("react_stack")
        if any(word in request_lower for word in ["복잡", "고급"]):
            context_patterns.append("high_complexity")
        if any(word in request_lower for word in ["급함", "빨리"]):
            context_patterns.append("high_urgency")
        
        return context_patterns
    
    def _generate_new_pattern_response(self, request: str) -> str:
        """새로운 패턴 응답 생성"""
        base_responses = [
            "요청을 분석해서 최적의 방법으로 처리해드리겠습니다.",
            "Stein님 스타일에 맞춰서 구현해드리겠습니다.",
            "혁신적인 방식으로 접근해서 해결해드리겠습니다."
        ]
        
        return random.choice(base_responses)
    
    def _get_current_metrics(self) -> Dict[str, Any]:
        """현재 메트릭 반환"""
        if not self.evolutionary_patterns:
            return {}
        
        fitness_scores = [p.fitness_score for p in self.evolutionary_patterns.values()]
        
        return {
            "total_patterns": len(self.evolutionary_patterns),
            "average_fitness": np.mean(fitness_scores),
            "best_fitness": max(fitness_scores),
            "generation": self.generation_counter,
            "mutation_rate": self.mutation_rate,
            "learning_progress": len(self.learning_history)
        }
    
    def _update_evolution_metrics(self):
        """진화 메트릭 업데이트"""
        if not self.evolutionary_patterns:
            return
        
        fitness_scores = [p.fitness_score for p in self.evolutionary_patterns.values()]
        best_pattern = max(self.evolutionary_patterns.values(), key=lambda p: p.fitness_score)
        
        self.evolution_metrics.total_patterns = len(self.evolutionary_patterns)
        self.evolution_metrics.average_fitness = np.mean(fitness_scores)
        self.evolution_metrics.best_pattern_id = best_pattern.pattern_id
        self.evolution_metrics.evolution_generation = self.generation_counter
        self.evolution_metrics.mutation_rate = self.mutation_rate
        self.evolution_metrics.adaptation_success_rate = np.mean([p.success_rate for p in self.evolutionary_patterns.values()])
        self.evolution_metrics.learning_progress = len(self.learning_history) / 100  # 정규화
    
    def get_evolution_report(self) -> Dict[str, Any]:
        """진화 리포트 생성"""
        return {
            "evolution_metrics": asdict(self.evolution_metrics),
            "top_patterns": self._get_top_patterns(5),
            "learning_trends": self._get_learning_trends(),
            "adaptation_progress": self._get_adaptation_progress()
        }
    
    def _get_top_patterns(self, count: int) -> List[Dict[str, Any]]:
        """상위 패턴들 반환"""
        sorted_patterns = sorted(
            self.evolutionary_patterns.values(),
            key=lambda p: p.fitness_score,
            reverse=True
        )
        
        return [
            {
                "pattern_id": p.pattern_id,
                "original_request": p.original_request,
                "enhanced_response": p.enhanced_response,
                "fitness_score": p.fitness_score,
                "success_rate": p.success_rate,
                "usage_count": p.usage_count,
                "generation": p.generation
            }
            for p in sorted_patterns[:count]
        ]
    
    def _get_learning_trends(self) -> Dict[str, Any]:
        """학습 트렌드 반환"""
        if len(self.learning_history) < 5:
            return {"trend": "insufficient_data"}
        
        recent_satisfaction = [r["satisfaction"] for r in self.learning_history[-10:]]
        return {
            "average_satisfaction": np.mean(recent_satisfaction),
            "satisfaction_trend": "improving" if recent_satisfaction[-1] > recent_satisfaction[0] else "declining",
            "learning_speed": len(self.learning_history) / max(1, self.generation_counter)
        }
    
    def _get_adaptation_progress(self) -> Dict[str, Any]:
        """적응 진행도 반환"""
        if not self.evolutionary_patterns:
            return {"progress": 0.0}
        
        adaptation_scores = [p.success_rate for p in self.evolutionary_patterns.values()]
        return {
            "average_adaptation": np.mean(adaptation_scores),
            "best_adaptation": max(adaptation_scores),
            "adaptation_progress": np.mean(adaptation_scores) / self.fitness_threshold
        }

def main():
    """테스트 실행"""
    system = SteinAIEvolutionarySystem()
    
    # 초기 집단 생성
    system.create_initial_population()
    
    print("🎯 Stein AI 진화형 시스템")
    print("=" * 60)
    
    # 테스트 요청들
    test_requests = [
        "코드 수정해줘",
        "버그 수정",
        "새로운 기능 구현",
        "성능 개선",
        "테스트 코드 작성"
    ]
    
    # 진화 시뮬레이션
    for i, request in enumerate(test_requests):
        print(f"\n🔄 세대 {system.generation_counter} - 요청 {i+1}")
        
        # 응답 생성
        response = system.generate_evolutionary_response(request)
        print(f"📝 원본: {response['original']}")
        print(f"🚀 향상: {response['enhanced']}")
        print(f"📊 신뢰도: {response['confidence']:.2f}")
        print(f"🎯 패턴 ID: {response['pattern_id']}")
        
        # 학습 시뮬레이션
        satisfaction = 0.8 + (i * 0.05) + random.uniform(-0.1, 0.1)
        system.learn_from_interaction(request, response['enhanced'], satisfaction)
        print(f"📈 만족도: {satisfaction:.2f}")
        
        # 진화 실행
        if i % 2 == 1:  # 2번마다 진화
            system.evolve_patterns()
            print(f"🧬 진화 완료 - 세대 {system.generation_counter}")
        
        print("-" * 40)
    
    # 진화 리포트 출력
    report = system.get_evolution_report()
    print(f"\n📊 진화 리포트:")
    print(f"- 총 패턴: {report['evolution_metrics']['total_patterns']}")
    print(f"- 평균 적합도: {report['evolution_metrics']['average_fitness']:.2f}")
    print(f"- 최고 적합도: {report['evolution_metrics']['best_pattern_id']}")
    print(f"- 진화 세대: {report['evolution_metrics']['evolution_generation']}")
    print(f"- 학습 진행도: {report['evolution_metrics']['learning_progress']:.2f}")
    
    # 상위 패턴들 출력
    print(f"\n🏆 상위 패턴들:")
    for i, pattern in enumerate(report['top_patterns'][:3]):
        print(f"{i+1}. {pattern['pattern_id']} (적합도: {pattern['fitness_score']:.2f})")
        print(f"   요청: {pattern['original_request']}")
        print(f"   응답: {pattern['enhanced_response'][:50]}...")

if __name__ == "__main__":
    main() 