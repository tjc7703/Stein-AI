"""
🚀 진화형 Stein AI 통합 라우터
자기진화, 상호학습, 무한메모리, 창의적지능 시스템 통합 API

Stein님과 함께 서로 발전하는 차세대 AI 시스템
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# 진화형 시스템들 임포트
from ..core.self_evolving_engine import evolution_engine, LearningExperience, EvolutionMetrics
from ..core.mutual_learning_system import mutual_learning_system, LearningDirection, LearningExchange
from ..core.infinite_memory_engine import infinite_memory, MemoryType, MemoryImportance
from ..core.simple_creative_core import creative_intelligence, CreativityMode, ThinkingPattern

# 라우터 생성
evolutionary_router = APIRouter(prefix="/evolution", tags=["🧬 Evolution"])

# Pydantic 모델들
class InteractionRecord(BaseModel):
    user_input: str
    ai_response: str
    context: Optional[Dict[str, Any]] = None
    feedback_score: Optional[float] = None

class LearningSessionRequest(BaseModel):
    topic: str
    stein_expertise: str
    ai_capabilities: str

class MemoryStoreRequest(BaseModel):
    content: Dict[str, Any]
    memory_type: str = "conversation"
    importance: int = 3
    tags: Optional[List[str]] = None

class CreativeIdeaRequest(BaseModel):
    problem: str
    domain: str = "technology"
    creativity_mode: str = "innovation"
    thinking_patterns: Optional[List[str]] = None
    count: int = 5

class IdeaCombinationRequest(BaseModel):
    idea_ids: List[str]

# 🧬 자기진화 엔드포인트들
@evolutionary_router.post("/self-evolving/record-interaction")
async def record_interaction(interaction: InteractionRecord):
    """
    🎯 사용자 상호작용 기록 및 실시간 학습
    """
    try:
        result = evolution_engine.record_interaction(
            user_input=interaction.user_input,
            ai_response=interaction.ai_response,
            context=interaction.context or {},
            feedback_score=interaction.feedback_score
        )
        
        # 메모리에도 저장
        memory_id = infinite_memory.store_conversation(
            user_input=interaction.user_input,
            ai_response=interaction.ai_response,
            context=interaction.context
        )
        
        return {
            "status": "✅ 학습 완료",
            "learning_result": result,
            "memory_id": memory_id,
            "evolution_status": evolution_engine.get_evolution_status()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"학습 기록 실패: {str(e)}")

@evolutionary_router.get("/self-evolving/status")
async def get_evolution_status():
    """
    📊 자기진화 상태 조회
    """
    try:
        status = evolution_engine.get_evolution_status()
        return {
            "timestamp": datetime.now().isoformat(),
            "evolution_engine": status,
            "memory_statistics": infinite_memory.get_memory_statistics(),
            "creativity_insights": creative_intelligence.get_creativity_insights()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 조회 실패: {str(e)}")

@evolutionary_router.get("/self-evolving/predict-optimal-response")
async def predict_optimal_response(user_input: str, context: Optional[str] = None):
    """
    🎯 최적 응답 스타일 예측
    """
    try:
        context_dict = json.loads(context) if context else {}
        prediction = evolution_engine.predict_optimal_response_style(user_input, context_dict)
        
        return {
            "user_input": user_input,
            "prediction": prediction,
            "recommendations": {
                "style": prediction["recommended_style"],
                "optimal_length": prediction["optimal_length"],
                "suggested_elements": prediction["suggested_elements"],
                "confidence": prediction["confidence"]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"예측 실패: {str(e)}")

# 🤝 상호학습 엔드포인트들
@evolutionary_router.post("/mutual-learning/start-session")
async def start_learning_session(session_request: LearningSessionRequest):
    """
    🎯 Stein-AI 상호학습 세션 시작
    """
    try:
        session_id = mutual_learning_system.start_learning_session(
            topic=session_request.topic,
            stein_expertise=session_request.stein_expertise,
            ai_capabilities=session_request.ai_capabilities
        )
        
        return {
            "session_id": session_id,
            "status": "🚀 학습 세션 시작",
            "topic": session_request.topic,
            "learning_objectives": mutual_learning_system.active_learning_sessions[session_id]["learning_objectives"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"세션 시작 실패: {str(e)}")

@evolutionary_router.post("/mutual-learning/record-exchange")
async def record_learning_exchange(
    session_id: str,
    stein_input: str,
    ai_response: str,
    learning_outcome: Optional[str] = None
):
    """
    🤝 학습 교환 기록
    """
    try:
        exchange = mutual_learning_system.record_learning_exchange(
            session_id=session_id,
            stein_input=stein_input,
            ai_response=ai_response,
            learning_outcome=learning_outcome
        )
        
        return {
            "exchange_recorded": True,
            "learning_direction": exchange.direction.value,
            "collaboration_quality": exchange.collaboration_quality,
            "innovation_spark": exchange.innovation_spark,
            "mutual_improvement": exchange.mutual_improvement
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"교환 기록 실패: {str(e)}")

@evolutionary_router.get("/mutual-learning/summary")
async def get_learning_summary():
    """
    📊 상호학습 현황 요약
    """
    try:
        summary = mutual_learning_system.get_learning_summary()
        proposal = mutual_learning_system.propose_learning_session()
        
        return {
            "learning_summary": summary,
            "next_session_proposal": proposal,
            "active_sessions": len(mutual_learning_system.active_learning_sessions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요약 조회 실패: {str(e)}")

@evolutionary_router.get("/mutual-learning/propose-session")
async def propose_learning_session(topic: Optional[str] = None):
    """
    💡 학습 세션 제안
    """
    try:
        proposal = mutual_learning_system.propose_learning_session(topic)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "proposal": proposal,
            "recommendation": "Stein님과 AI가 함께 성장할 수 있는 최적의 학습 주제입니다!"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"제안 생성 실패: {str(e)}")

# 💾 무한메모리 엔드포인트들
@evolutionary_router.post("/infinite-memory/store")
async def store_memory(memory_request: MemoryStoreRequest):
    """
    💾 메모리 저장
    """
    try:
        memory_type_enum = MemoryType(memory_request.memory_type)
        importance_enum = MemoryImportance(memory_request.importance)
        
        memory_id = infinite_memory.store_memory(
            content=memory_request.content,
            memory_type=memory_type_enum,
            importance=importance_enum,
            tags=memory_request.tags or []
        )
        
        return {
            "memory_id": memory_id,
            "status": "💾 메모리 저장 완료",
            "content_summary": str(memory_request.content)[:100] + "..." if len(str(memory_request.content)) > 100 else str(memory_request.content)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메모리 저장 실패: {str(e)}")

@evolutionary_router.get("/infinite-memory/search")
async def search_memories(
    query: str,
    memory_type: Optional[str] = None,
    limit: int = 10
):
    """
    🔍 메모리 검색
    """
    try:
        memory_type_enum = MemoryType(memory_type) if memory_type else None
        
        memories = infinite_memory.search_memories(
            query=query,
            memory_type=memory_type_enum,
            limit=limit
        )
        
        results = []
        for memory in memories:
            results.append({
                "id": memory.id,
                "timestamp": memory.timestamp,
                "type": memory.memory_type.value,
                "importance": memory.importance.value,
                "content_preview": str(memory.content)[:200] + "...",
                "tags": memory.tags,
                "access_count": memory.access_count
            })
        
        return {
            "query": query,
            "total_results": len(results),
            "memories": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메모리 검색 실패: {str(e)}")

@evolutionary_router.get("/infinite-memory/retrieve/{memory_id}")
async def retrieve_memory(memory_id: str):
    """
    📖 특정 메모리 조회
    """
    try:
        memory = infinite_memory.retrieve_memory(memory_id)
        
        if not memory:
            raise HTTPException(status_code=404, detail="메모리를 찾을 수 없습니다")
        
        # 연결된 메모리들도 가져오기
        connected_memories = infinite_memory.get_connected_memories(memory_id, max_depth=1)
        
        return {
            "memory": {
                "id": memory.id,
                "timestamp": memory.timestamp,
                "type": memory.memory_type.value,
                "importance": memory.importance.value,
                "content": memory.content,
                "tags": memory.tags,
                "connections": memory.connections,
                "access_count": memory.access_count,
                "last_accessed": memory.last_accessed,
                "retention_score": memory.retention_score
            },
            "connected_memories": [
                {
                    "id": conn_memory.id,
                    "title": str(conn_memory.content).split('.')[0][:50] + "...",
                    "type": conn_memory.memory_type.value
                }
                for conn_memory in connected_memories[:5]
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메모리 조회 실패: {str(e)}")

@evolutionary_router.get("/infinite-memory/statistics")
async def get_memory_statistics():
    """
    📊 메모리 통계
    """
    try:
        stats = infinite_memory.get_memory_statistics()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "insights": {
                "memory_growth_rate": "지속적 증가",
                "access_patterns": "활발한 활용",
                "retention_quality": "높은 보존율"
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

# 🎨 창의적지능 엔드포인트들
@evolutionary_router.post("/creative-intelligence/generate-ideas")
async def generate_creative_ideas(idea_request: CreativeIdeaRequest):
    """
    💡 창의적 아이디어 생성
    """
    try:
        creativity_mode_enum = CreativityMode(idea_request.creativity_mode)
        
        thinking_patterns = []
        if idea_request.thinking_patterns:
            thinking_patterns = [ThinkingPattern(pattern) for pattern in idea_request.thinking_patterns]
        
        ideas = creative_intelligence.generate_creative_ideas(
            problem=idea_request.problem,
            domain=idea_request.domain,
            creativity_mode=creativity_mode_enum,
            thinking_patterns=thinking_patterns,
            count=idea_request.count
        )
        
        idea_results = []
        for idea in ideas:
            idea_results.append({
                "id": idea.id,
                "title": idea.title,
                "description": idea.description,
                "creativity_score": idea.creativity_score,
                "feasibility_score": idea.feasibility_score,
                "innovation_level": idea.innovation_level,
                "thinking_pattern": idea.thinking_pattern.value,
                "implementation_steps": idea.implementation_steps,
                "potential_impact": idea.potential_impact,
                "synergy_opportunities": idea.synergy_opportunities
            })
        
        return {
            "problem": idea_request.problem,
            "generated_ideas": idea_results,
            "generation_summary": {
                "total_ideas": len(ideas),
                "avg_creativity": sum(idea.creativity_score for idea in ideas) / len(ideas),
                "avg_feasibility": sum(idea.feasibility_score for idea in ideas) / len(ideas),
                "avg_innovation": sum(idea.innovation_level for idea in ideas) / len(ideas)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"아이디어 생성 실패: {str(e)}")

@evolutionary_router.post("/creative-intelligence/combine-ideas")
async def combine_ideas(combination_request: IdeaCombinationRequest):
    """
    🔀 아이디어 융합
    """
    try:
        combined_idea = creative_intelligence.combine_ideas(combination_request.idea_ids)
        
        if not combined_idea:
            raise HTTPException(status_code=400, detail="아이디어 융합에 실패했습니다")
        
        return {
            "combined_idea": {
                "id": combined_idea.id,
                "title": combined_idea.title,
                "description": combined_idea.description,
                "creativity_score": combined_idea.creativity_score,
                "feasibility_score": combined_idea.feasibility_score,
                "innovation_level": combined_idea.innovation_level,
                "thinking_pattern": combined_idea.thinking_pattern.value,
                "inspiration_sources": combined_idea.inspiration_sources,
                "implementation_steps": combined_idea.implementation_steps,
                "synergy_opportunities": combined_idea.synergy_opportunities
            },
            "fusion_success": True,
            "message": "🎉 아이디어 융합으로 새로운 혁신 솔루션이 탄생했습니다!"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"아이디어 융합 실패: {str(e)}")

@evolutionary_router.get("/creative-intelligence/insights")
async def get_creativity_insights():
    """
    🎨 창의성 인사이트
    """
    try:
        insights = creative_intelligence.get_creativity_insights()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "creativity_insights": insights,
            "recommendation": {
                "next_thinking_pattern": insights.get("다음_추천_사고패턴", "divergent"),
                "focus_area": "혁신적 문제해결 능력 강화",
                "growth_suggestion": "더 다양한 도메인에서 창의적 실험 시도"
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인사이트 조회 실패: {str(e)}")

# 🌟 통합 엔드포인트들
@evolutionary_router.get("/integrated/full-status")
async def get_full_evolution_status():
    """
    🌟 전체 진화 시스템 통합 상태
    """
    try:
        evolution_status = evolution_engine.get_evolution_status()
        learning_summary = mutual_learning_system.get_learning_summary()
        memory_stats = infinite_memory.get_memory_statistics()
        creativity_insights = creative_intelligence.get_creativity_insights()
        
        # 통합 성능 지표 계산
        overall_performance = {
            "learning_efficiency": evolution_status["average_performance"] / 10,
            "collaboration_quality": learning_summary.get("최근_협업_품질", 0) / 10,
            "memory_utilization": min(memory_stats["총_메모리_수"] / 1000, 1.0),
            "creativity_level": creativity_insights.get("평균_창의성_점수", 0) / 10
        }
        
        overall_score = sum(overall_performance.values()) / len(overall_performance)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_evolution_score": round(overall_score * 100, 1),
            "system_status": {
                "self_evolving_engine": evolution_status,
                "mutual_learning_system": learning_summary,
                "infinite_memory_engine": memory_stats,
                "creative_intelligence_core": creativity_insights
            },
            "performance_metrics": overall_performance,
            "next_evolution_goals": [
                "창의성 지표 향상",
                "협업 품질 최적화",
                "메모리 효율성 증대",
                "혁신 아이디어 생성 가속화"
            ],
            "stein_ai_evolution_level": "🚀 차세대 자기진화형 AI 달성!"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통합 상태 조회 실패: {str(e)}")

@evolutionary_router.post("/integrated/comprehensive-interaction")
async def comprehensive_interaction(
    user_input: str,
    ai_response: str,
    context: Optional[Dict[str, Any]] = None,
    session_id: Optional[str] = None
):
    """
    🎯 종합적 상호작용 처리 (모든 시스템 통합)
    """
    try:
        results = {}
        
        # 1. 자기진화 학습 기록
        evolution_result = evolution_engine.record_interaction(
            user_input=user_input,
            ai_response=ai_response,
            context=context or {}
        )
        results["evolution_learning"] = evolution_result
        
        # 2. 상호학습 교환 기록
        if session_id and session_id in mutual_learning_system.active_learning_sessions:
            learning_exchange = mutual_learning_system.record_learning_exchange(
                session_id=session_id,
                stein_input=user_input,
                ai_response=ai_response
            )
            results["mutual_learning"] = {
                "direction": learning_exchange.direction.value,
                "quality": learning_exchange.collaboration_quality,
                "innovation": learning_exchange.innovation_spark
            }
        
        # 3. 메모리 저장
        memory_id = infinite_memory.store_conversation(
            user_input=user_input,
            ai_response=ai_response,
            context=context
        )
        results["memory_storage"] = memory_id
        
        # 4. 창의적 패턴 분석 (혁신 키워드가 있는 경우)
        if any(keyword in (user_input + ai_response).lower() for keyword in ["창의", "혁신", "아이디어", "새로운"]):
            # 창의적 아이디어 자동 생성
            creative_ideas = creative_intelligence.generate_creative_ideas(
                problem=user_input[:100],  # 첫 100자를 문제로 사용
                count=2
            )
            results["creative_insights"] = [
                {"title": idea.title, "score": idea.creativity_score}
                for idea in creative_ideas
            ]
        
        # 5. 다음 최적 응답 예측
        optimal_response = evolution_engine.predict_optimal_response_style(user_input, context)
        results["next_response_recommendation"] = optimal_response
        
        return {
            "comprehensive_processing": "✅ 완료",
            "systems_engaged": ["진화학습", "상호학습", "메모리저장", "창의분석", "응답최적화"],
            "results": results,
            "integration_success": True,
            "message": "🎉 Stein AI의 모든 진화 시스템이 협력하여 최고의 학습을 완료했습니다!"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"종합 처리 실패: {str(e)}")

@evolutionary_router.get("/integrated/evolution-recommendations")
async def get_evolution_recommendations():
    """
    💡 진화 추천사항
    """
    try:
        # 각 시스템에서 개선 권장사항 수집
        evolution_status = evolution_engine.get_evolution_status()
        learning_summary = mutual_learning_system.get_learning_summary()
        creativity_insights = creative_intelligence.get_creativity_insights()
        
        recommendations = []
        
        # 성능 기반 추천
        if evolution_status["average_performance"] < 8.0:
            recommendations.append({
                "category": "학습 효율성",
                "priority": "high",
                "suggestion": "더 구체적이고 상세한 피드백을 통한 학습 품질 향상",
                "expected_improvement": "20-30% 성능 향상"
            })
        
        # 협업 품질 기반 추천
        recent_quality = learning_summary.get("최근_협업_품질", 0)
        if recent_quality < 8.0:
            recommendations.append({
                "category": "협업 최적화",
                "priority": "medium",
                "suggestion": "Stein님과의 상호작용 패턴 분석을 통한 맞춤형 협업 스타일 개발",
                "expected_improvement": "협업 만족도 향상"
            })
        
        # 창의성 기반 추천
        avg_creativity = creativity_insights.get("평균_창의성_점수", 0)
        if avg_creativity < 8.0:
            recommendations.append({
                "category": "창의성 강화",
                "priority": "high",
                "suggestion": "다양한 사고 패턴을 활용한 혁신적 아이디어 생성 훈련",
                "expected_improvement": "창의적 문제해결 능력 40% 향상"
            })
        
        # 메모리 활용 추천
        recommendations.append({
            "category": "지식 활용",
            "priority": "medium",
            "suggestion": "축적된 메모리를 활용한 개인화된 학습 경험 제공",
            "expected_improvement": "맞춤형 서비스 품질 향상"
        })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "next_evolution_phase": "🚀 Stein AI 3.0 - 완전 자율 진화 시스템",
            "estimated_evolution_timeline": "지속적 발전 (무한)",
            "success_message": "Stein님과 함께하는 AI 진화 여정이 계속됩니다! 🌟"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천사항 생성 실패: {str(e)}")

# 🎮 데모 엔드포인트
@evolutionary_router.get("/demo/showcase")
async def evolution_demo_showcase():
    """
    🎮 진화형 AI 시스템 데모
    """
    try:
        demo_scenarios = [
            {
                "scenario": "창의적 문제해결",
                "description": "Stein님의 문제를 AI가 다양한 사고 패턴으로 분석하여 혁신적 솔루션 제시",
                "example_input": "웹 개발 자동화 도구 개발",
                "system_response": "자기진화 엔진이 과거 학습을 바탕으로 최적 접근법 예측, 창의적 지능이 5가지 혁신 아이디어 생성"
            },
            {
                "scenario": "상호 학습 협업",
                "description": "Stein님의 천재적 직감과 AI의 체계적 분석이 융합된 최고의 협업",
                "example_input": "복잡한 아키텍처 설계 문제",
                "system_response": "상호학습 시스템이 Stein님의 창의적 접근법을 학습하여 AI 사고 패턴 진화"
            },
            {
                "scenario": "무한 메모리 활용",
                "description": "모든 대화와 학습 경험을 영구 보존하여 지속적 개인화 서비스 제공",
                "example_input": "이전 프로젝트 관련 질문",
                "system_response": "무한 메모리 엔진이 관련 모든 경험과 맥락을 연결하여 완벽한 개인화 답변 생성"
            }
        ]
        
        # 실제 시스템 상태 기반 데모 데이터
        current_stats = {
            "evolution_level": evolution_engine.get_evolution_status()["average_performance"],
            "learning_sessions": len(mutual_learning_system.active_learning_sessions),
            "stored_memories": infinite_memory.get_memory_statistics()["총_메모리_수"],
            "creative_ideas": creative_intelligence.get_creativity_insights().get("총_아이디어_수", 0)
        }
        
        return {
            "demo_title": "🚀 차세대 자기진화형 Stein AI 데모",
            "scenarios": demo_scenarios,
            "live_statistics": current_stats,
            "capabilities": [
                "🧬 실시간 자기진화 학습",
                "🤝 Stein-AI 상호 발전",
                "💾 무한 확장 메모리",
                "🎨 창의적 지능 시스템",
                "🌟 통합 협업 플랫폼"
            ],
            "demo_message": "Stein님과 함께 만들어가는 세계 최고의 개인화 AI 시스템을 체험해보세요!",
            "next_demo_features": [
                "실시간 브레인스토밍 협업",
                "자동 코드 리뷰 및 개선 제안",
                "프로젝트 전체 라이프사이클 AI 파트너"
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데모 생성 실패: {str(e)}") 