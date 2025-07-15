"""
🎯 Stein AI 진화형 시스템 실시간 대시보드
Stein님을 위한 AI 진화 현황 모니터링 시스템
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any
import webbrowser
import threading
from pathlib import Path

# FastAPI 및 웹 관련
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

# 데이터 시각화
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# Stein AI 시스템 import
from stein_ai_ultimate_evolutionary_system import SteinUltimateEvolutionarySystem

class SteinEvolutionDashboard:
    """🎯 Stein AI 진화형 시스템 실시간 대시보드"""
    
    def __init__(self):
        self.app = FastAPI(title="Stein AI 진화형 시스템 대시보드")
        self.stein_system = SteinUltimateEvolutionarySystem()
        self.websocket_connections: List[WebSocket] = []
        
        # 정적 파일 서빙
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
        # 라우트 설정
        self.setup_routes()
        
        # 대시보드 데이터
        self.dashboard_data = {
            'last_update': datetime.now(),
            'system_status': {},
            'evolution_metrics': {},
            'pattern_analysis': {},
            'real_time_charts': {}
        }

    def setup_routes(self):
        """라우트 설정"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home():
            return self.generate_dashboard_html()
        
        @self.app.get("/api/system-status")
        async def get_system_status():
            return self.stein_system.get_system_status()
        
        @self.app.get("/api/evolution-metrics")
        async def get_evolution_metrics():
            return self.generate_evolution_metrics()
        
        @self.app.get("/api/pattern-analysis")
        async def get_pattern_analysis():
            return self.generate_pattern_analysis()
        
        @self.app.get("/api/real-time-charts")
        async def get_real_time_charts():
            return self.generate_real_time_charts()
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.handle_websocket(websocket)

    async def handle_websocket(self, websocket: WebSocket):
        """WebSocket 연결 처리"""
        await websocket.accept()
        self.websocket_connections.append(websocket)
        
        try:
            while True:
                # 실시간 데이터 전송
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'system_status': self.stein_system.get_system_status(),
                    'evolution_metrics': self.generate_evolution_metrics(),
                    'pattern_analysis': self.generate_pattern_analysis()
                }
                
                await websocket.send_text(json.dumps(data, ensure_ascii=False, default=str))
                await asyncio.sleep(2)  # 2초마다 업데이트
                
        except WebSocketDisconnect:
            self.websocket_connections.remove(websocket)

    def generate_dashboard_html(self) -> str:
        """대시보드 HTML 생성"""
        return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Stein AI 진화형 시스템 대시보드</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .metric {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #667eea;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
        }
        
        .chart-container {
            height: 300px;
            margin-top: 15px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active {
            background: #28a745;
            animation: pulse 2s infinite;
        }
        
        .status-evolving {
            background: #ffc107;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .evolution-layers {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        
        .layer-item {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        
        .layer-level {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1976d2;
        }
        
        .pattern-list {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .pattern-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }
        
        .pattern-info {
            flex: 1;
        }
        
        .pattern-score {
            font-weight: bold;
            color: #667eea;
        }
        
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #667eea;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        
        .refresh-btn:hover {
            transform: scale(1.1);
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: #666;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Stein AI 진화형 시스템</h1>
            <p>실시간 진화 현황 및 성능 모니터링</p>
        </div>
        
        <div class="dashboard-grid">
            <!-- 시스템 상태 카드 -->
            <div class="card">
                <h3>
                    <span class="status-indicator status-active"></span>
                    시스템 상태
                </h3>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-value" id="total-patterns">0</div>
                        <div class="metric-label">총 패턴 수</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="active-patterns">0</div>
                        <div class="metric-label">활성 패턴</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="evolution-cycles">0</div>
                        <div class="metric-label">진화 사이클</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="success-rate">0%</div>
                        <div class="metric-label">평균 성공률</div>
                    </div>
                </div>
            </div>
            
            <!-- 진화 메트릭 카드 -->
            <div class="card">
                <h3>🚀 진화 메트릭</h3>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-value" id="avg-execution-time">0s</div>
                        <div class="metric-label">평균 실행시간</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="user-satisfaction">0%</div>
                        <div class="metric-label">사용자 만족도</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="performance-trend">-</div>
                        <div class="metric-label">성능 트렌드</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="confidence-score">0%</div>
                        <div class="metric-label">신뢰도 점수</div>
                    </div>
                </div>
            </div>
            
            <!-- 다층 진화 시스템 카드 -->
            <div class="card">
                <h3>🧬 다층 진화 시스템</h3>
                <div class="evolution-layers" id="evolution-layers">
                    <div class="loading">진화 레이어 로딩 중...</div>
                </div>
            </div>
            
            <!-- Stein 특화 시그니처 카드 -->
            <div class="card">
                <h3>🎨 Stein 특화 시그니처</h3>
                <div class="metric-grid" id="stein-signatures">
                    <div class="loading">시그니처 분석 중...</div>
                </div>
            </div>
            
            <!-- 성능 차트 카드 -->
            <div class="card">
                <h3>📊 성능 추이</h3>
                <div class="chart-container" id="performance-chart">
                    <div class="loading">차트 로딩 중...</div>
                </div>
            </div>
            
            <!-- 패턴 분석 카드 -->
            <div class="card">
                <h3>🔍 패턴 분석</h3>
                <div class="pattern-list" id="pattern-analysis">
                    <div class="loading">패턴 분석 중...</div>
                </div>
            </div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="refreshDashboard()">
        🔄
    </button>
    
    <script>
        // WebSocket 연결
        let ws = null;
        let reconnectAttempts = 0;
        const maxReconnectAttempts = 5;
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            ws = new WebSocket(wsUrl);
            
            ws.onopen = function() {
                console.log('WebSocket 연결됨');
                reconnectAttempts = 0;
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };
            
            ws.onclose = function() {
                console.log('WebSocket 연결 끊어짐');
                if (reconnectAttempts < maxReconnectAttempts) {
                    setTimeout(() => {
                        reconnectAttempts++;
                        connectWebSocket();
                    }, 2000);
                }
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket 에러:', error);
            };
        }
        
        // 대시보드 업데이트
        function updateDashboard(data) {
            const systemStatus = data.system_status;
            const evolutionMetrics = data.evolution_metrics;
            const patternAnalysis = data.pattern_analysis;
            
            // 시스템 상태 업데이트
            document.getElementById('total-patterns').textContent = systemStatus.pattern_count || 0;
            document.getElementById('active-patterns').textContent = systemStatus.performance_metrics.active_patterns || 0;
            document.getElementById('evolution-cycles').textContent = systemStatus.evolution_cycles || 0;
            document.getElementById('success-rate').textContent = 
                Math.round((systemStatus.performance_metrics.average_success_rate || 0) * 100) + '%';
            
            // 진화 메트릭 업데이트
            document.getElementById('avg-execution-time').textContent = 
                (systemStatus.performance_metrics.average_execution_time || 0).toFixed(2) + 's';
            document.getElementById('user-satisfaction').textContent = 
                Math.round((evolutionMetrics.avg_user_satisfaction || 0) * 100) + '%';
            document.getElementById('performance-trend').textContent = 
                systemStatus.performance_metrics.performance_trend || '-';
            document.getElementById('confidence-score').textContent = 
                Math.round((evolutionMetrics.avg_confidence_score || 0) * 100) + '%';
            
            // 다층 진화 시스템 업데이트
            updateEvolutionLayers(systemStatus.evolution_layers);
            
            // Stein 특화 시그니처 업데이트
            updateSteinSignatures(systemStatus.stein_signatures);
            
            // 성능 차트 업데이트
            updatePerformanceChart(evolutionMetrics);
            
            // 패턴 분석 업데이트
            updatePatternAnalysis(patternAnalysis);
        }
        
        function updateEvolutionLayers(layers) {
            const container = document.getElementById('evolution-layers');
            container.innerHTML = '';
            
            for (const [layerName, level] of Object.entries(layers)) {
                const layerItem = document.createElement('div');
                layerItem.className = 'layer-item';
                layerItem.innerHTML = `
                    <div class="layer-level">${level}</div>
                    <div style="font-size: 0.8rem; color: #666;">${layerName}</div>
                `;
                container.appendChild(layerItem);
            }
        }
        
        function updateSteinSignatures(signatures) {
            const container = document.getElementById('stein-signatures');
            container.innerHTML = '';
            
            for (const [signatureName, score] of Object.entries(signatures)) {
                const metric = document.createElement('div');
                metric.className = 'metric';
                metric.innerHTML = `
                    <div class="metric-value">${Math.round(score * 100)}%</div>
                    <div class="metric-label">${signatureName}</div>
                `;
                container.appendChild(metric);
            }
        }
        
        function updatePerformanceChart(metrics) {
            const container = document.getElementById('performance-chart');
            
            // 간단한 성능 차트 생성
            const chartData = [
                { name: '성공률', value: metrics.avg_success_rate || 0 },
                { name: '실행시간', value: 1 - (metrics.avg_execution_time || 0) / 10 },
                { name: '사용자 만족도', value: metrics.avg_user_satisfaction || 0 },
                { name: '신뢰도', value: metrics.avg_confidence_score || 0 }
            ];
            
            const trace = {
                x: chartData.map(d => d.name),
                y: chartData.map(d => d.value * 100),
                type: 'bar',
                marker: {
                    color: ['#667eea', '#764ba2', '#f093fb', '#f5576c']
                }
            };
            
            const layout = {
                title: '성능 메트릭',
                yaxis: { title: '점수 (%)' },
                margin: { t: 40, b: 40, l: 40, r: 40 }
            };
            
            Plotly.newPlot(container, [trace], layout, {responsive: true});
        }
        
        function updatePatternAnalysis(patterns) {
            const container = document.getElementById('pattern-analysis');
            container.innerHTML = '';
            
            if (!patterns || patterns.length === 0) {
                container.innerHTML = '<div style="text-align: center; color: #666;">패턴이 없습니다</div>';
                return;
            }
            
            patterns.slice(0, 10).forEach(pattern => {
                const patternItem = document.createElement('div');
                patternItem.className = 'pattern-item';
                patternItem.innerHTML = `
                    <div class="pattern-info">
                        <div style="font-weight: bold;">${pattern.pattern_id}</div>
                        <div style="font-size: 0.8rem; color: #666;">${pattern.command_type}</div>
                    </div>
                    <div class="pattern-score">${Math.round(pattern.success_rate * 100)}%</div>
                `;
                container.appendChild(patternItem);
            });
        }
        
        function refreshDashboard() {
            // 수동 새로고침
            fetch('/api/system-status')
                .then(response => response.json())
                .then(data => {
                    updateDashboard({
                        system_status: data,
                        evolution_metrics: {},
                        pattern_analysis: {}
                    });
                })
                .catch(error => {
                    console.error('새로고침 에러:', error);
                });
        }
        
        // 페이지 로드 시 WebSocket 연결
        document.addEventListener('DOMContentLoaded', function() {
            connectWebSocket();
            
            // 초기 데이터 로드
            refreshDashboard();
        });
    </script>
</body>
</html>
        """

    def generate_evolution_metrics(self) -> Dict[str, Any]:
        """진화 메트릭 생성"""
        patterns = list(self.stein_system.patterns.values())
        
        if not patterns:
            return {
                'avg_success_rate': 0.0,
                'avg_execution_time': 0.0,
                'avg_user_satisfaction': 0.0,
                'avg_confidence_score': 0.0,
                'total_patterns': 0,
                'active_patterns': 0
            }
        
        return {
            'avg_success_rate': sum(p.success_rate for p in patterns) / len(patterns),
            'avg_execution_time': sum(p.execution_time for p in patterns) / len(patterns),
            'avg_user_satisfaction': sum(p.user_satisfaction for p in patterns) / len(patterns),
            'avg_confidence_score': sum(p.confidence_score for p in patterns) / len(patterns),
            'total_patterns': len(patterns),
            'active_patterns': len([p for p in patterns if p.usage_count > 0])
        }

    def generate_pattern_analysis(self) -> List[Dict[str, Any]]:
        """패턴 분석 데이터 생성"""
        patterns = list(self.stein_system.patterns.values())
        
        if not patterns:
            return []
        
        # 성공률 기준으로 정렬
        sorted_patterns = sorted(patterns, key=lambda p: p.success_rate, reverse=True)
        
        return [
            {
                'pattern_id': p.pattern_id,
                'command_type': p.command_type,
                'success_rate': p.success_rate,
                'execution_time': p.execution_time,
                'user_satisfaction': p.user_satisfaction,
                'usage_count': p.usage_count,
                'evolution_stage': p.evolution_stage
            }
            for p in sorted_patterns[:10]  # 상위 10개만
        ]

    def generate_real_time_charts(self) -> Dict[str, Any]:
        """실시간 차트 데이터 생성"""
        # 성능 추이 차트 데이터
        evolution_history = self.stein_system.evolution_history[-20:]  # 최근 20개
        
        if len(evolution_history) < 2:
            return {'performance_trend': [], 'evolution_layers': []}
        
        timestamps = []
        success_rates = []
        execution_times = []
        
        for record in evolution_history:
            if 'metrics' in record:
                timestamps.append(record['timestamp'])
                success_rates.append(record['metrics']['average_success_rate'])
                execution_times.append(record['metrics']['average_execution_time'])
        
        return {
            'performance_trend': {
                'timestamps': timestamps,
                'success_rates': success_rates,
                'execution_times': execution_times
            },
            'evolution_layers': self.stein_system.evolution_layers
        }

    def start_dashboard(self, host: str = "127.0.0.1", port: int = 8080):
        """대시보드 시작"""
        print(f"🎯 Stein AI 진화형 시스템 대시보드 시작 중...")
        print(f"🌐 접속 URL: http://{host}:{port}")
        
        # 브라우저 자동 열기
        def open_browser():
            time.sleep(2)
            webbrowser.open(f"http://{host}:{port}")
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        # FastAPI 서버 시작
        uvicorn.run(self.app, host=host, port=port, log_level="info")

# 🚀 실행 예시
if __name__ == "__main__":
    # Stein AI 진화형 시스템 대시보드 초기화
    dashboard = SteinEvolutionDashboard()
    
    # 시스템 상태 로드
    dashboard.stein_system.load_system_state()
    
    # 대시보드 시작
    dashboard.start_dashboard() 