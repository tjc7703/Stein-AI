"""
🎮 마케팅 게임 API 라우터
Stein AI 마케팅 학습 게임의 웹 인터페이스
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime

from ..core.marketing_learning_game import marketing_game

router = APIRouter(prefix="/marketing-game", tags=["마케팅 게임"])

@router.get("/", response_class=HTMLResponse)
async def marketing_game_dashboard():
    """마케팅 게임 대시보드"""
    try:
        status = marketing_game.get_game_status()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🎮 Stein AI 마케팅 마스터 게임</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background: #0a0e27;
                    color: white;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    border-radius: 20px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: rgba(255, 255, 255, 0.08);
                    padding: 20px;
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }}
                .stat-card h3 {{
                    color: #64ffda;
                    margin-bottom: 10px;
                }}
                .stat-card .value {{
                    font-size: 2rem;
                    font-weight: bold;
                }}
                .btn {{
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 25px;
                    text-decoration: none;
                    display: inline-block;
                    margin: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎮 마케팅 마스터 게임</h1>
                    <p>30일 과정으로 마케팅 전문가가 되어보세요!</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>📅 현재 일차</h3>
                        <div class="value">{status['current_day']}/30</div>
                    </div>
                    
                    <div class="stat-card">
                        <h3>🏆 총 점수</h3>
                        <div class="value">{status['total_score']:,}</div>
                    </div>
                    
                    <div class="stat-card">
                        <h3>✅ 완료 미션</h3>
                        <div class="value">{status['completed_missions']}/{status['total_missions']}</div>
                    </div>
                    
                    <div class="stat-card">
                        <h3>🔥 연속 완주</h3>
                        <div class="value">{status['current_streak']}일</div>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <a href="/marketing-game/start" class="btn">🎮 게임 시작</a>
                    <a href="/marketing-game/missions" class="btn">📋 미션 목록</a>
                    <a href="/marketing-game/status" class="btn">📊 상태 확인</a>
                </div>
                
                {f'''
                <div style="margin-top: 30px; padding: 20px; background: rgba(255, 255, 255, 0.05); border-radius: 15px;">
                    <h3>🎯 다음 미션</h3>
                    <p><strong>{status.get('next_mission', {}).get('title', '미션을 시작해주세요')}</strong></p>
                    <p>{status.get('next_mission', {}).get('description', '게임을 시작하면 첫 번째 미션이 나타납니다.')}</p>
                </div>
                ''' if status.get('next_mission') else ''}
            </div>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>🎮 마케팅 게임 - 오류</title>
        </head>
        <body style="background: #0a0e27; color: white; font-family: Arial, sans-serif; padding: 20px;">
            <h1>🎮 마케팅 마스터 게임</h1>
            <p>오류가 발생했습니다: {str(e)}</p>
            <p>서버를 재시작해주세요.</p>
        </body>
        </html>
        """

@router.get("/start")
async def start_game():
    """게임 시작"""
    await marketing_game.load_progress()
    result = await marketing_game.start_game()
    return result

@router.get("/status")
async def get_game_status():
    """게임 상태 조회"""
    await marketing_game.load_progress()
    return marketing_game.get_game_status()

@router.get("/missions")
async def get_missions():
    """미션 목록 조회"""
    await marketing_game.load_progress()
    return {
        "missions": [
            {
                "id": mission.id,
                "day": mission.day,
                "title": mission.title,
                "description": mission.description,
                "mission_type": mission.mission_type.value,
                "difficulty": mission.difficulty.value,
                "completed": mission.completed,
                "score": mission.score,
                "rewards": mission.rewards
            }
            for mission in marketing_game.missions
        ]
    }

@router.post("/complete/{mission_id}")
async def complete_mission(mission_id: str, answers: Optional[Dict[str, Any]] = None):
    """미션 완료"""
    await marketing_game.load_progress()
    result = await marketing_game.complete_mission(mission_id, answers or {})
    return result

@router.get("/leaderboard")
async def get_leaderboard():
    """리더보드"""
    # 실제로는 데이터베이스에서 가져와야 함
    return {
        "leaderboard": [
            {"rank": 1, "name": "Stein", "score": 15000, "completed": 30},
            {"rank": 2, "name": "AI_Learner", "score": 12000, "completed": 25},
            {"rank": 3, "name": "Marketing_Pro", "score": 10000, "completed": 20},
        ]
    }

@router.get("/reset")
async def reset_game():
    """게임 리셋"""
    marketing_game.player_progress = marketing_game.player_progress.__class__()
    for mission in marketing_game.missions:
        mission.completed = False
        mission.score = 0
        mission.completed_at = None
    await marketing_game._save_progress()
    return {"message": "게임이 리셋되었습니다."} 