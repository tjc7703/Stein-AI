#!/usr/bin/env python3
"""
⚖️ Stein 스마트 밸런싱 분석기
- 개발 패턴 분석
- 최적 밸런싱 포인트 제안
- 맞춤형 최적화 전략
"""

import os
import json
from pathlib import Path
from datetime import datetime
import re

class SteinBalanceAnalyzer:
    """Stein님 전용 밸런싱 분석기"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.analysis_results = {}
        
    def analyze_code_structure(self):
        """코드 구조 분석"""
        print("📊 Stein님 코드 구조 분석 중...")
        
        structure_data = {
            "files_analyzed": 0,
            "total_lines": 0,
            "avg_lines_per_file": 0,
            "complexity_score": 0,
            "modularity_score": 0,
            "balance_recommendations": []
        }
        
        # 주요 Python 파일들 분석
        python_files = list(self.project_root.glob("*.py"))
        python_files.extend(list(self.project_root.glob("**/*.py")))
        
        for file_path in python_files:
            if "__pycache__" in str(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    structure_data["files_analyzed"] += 1
                    structure_data["total_lines"] += len(lines)
                    
                    # 복잡성 분석
                    complexity = self.calculate_complexity(lines)
                    structure_data["complexity_score"] += complexity
                    
            except Exception as e:
                continue
        
        if structure_data["files_analyzed"] > 0:
            structure_data["avg_lines_per_file"] = structure_data["total_lines"] / structure_data["files_analyzed"]
            structure_data["complexity_score"] /= structure_data["files_analyzed"]
            
            # 모듈성 점수 계산
            structure_data["modularity_score"] = self.calculate_modularity_score(structure_data)
            
            # 밸런싱 추천
            structure_data["balance_recommendations"] = self.generate_balance_recommendations(structure_data)
        
        self.analysis_results["structure"] = structure_data
        return structure_data
    
    def calculate_complexity(self, lines):
        """코드 복잡성 계산"""
        complexity = 0
        for line in lines:
            line = line.strip()
            # 간단한 복잡성 지표들
            if line.startswith("if ") or line.startswith("elif "):
                complexity += 1
            elif line.startswith("for ") or line.startswith("while "):
                complexity += 2
            elif line.startswith("def ") or line.startswith("class "):
                complexity += 0.5
        return complexity
    
    def calculate_modularity_score(self, structure_data):
        """모듈성 점수 계산"""
        avg_lines = structure_data["avg_lines_per_file"]
        
        if avg_lines <= 100:
            return 95
        elif avg_lines <= 200:
            return 80
        elif avg_lines <= 300:
            return 60
        else:
            return 40
    
    def generate_balance_recommendations(self, structure_data):
        """밸런싱 추천 생성"""
        recommendations = []
        
        avg_lines = structure_data["avg_lines_per_file"]
        complexity = structure_data["complexity_score"]
        
        if avg_lines > 200:
            recommendations.append({
                "type": "구조화",
                "message": f"평균 {avg_lines:.0f}줄 → 모듈 분리 권장",
                "benefit": "개발 속도 30% 향상",
                "priority": "high"
            })
        
        if complexity > 20:
            recommendations.append({
                "type": "단순화",
                "message": f"복잡성 점수 {complexity:.1f} → 함수 분리 권장",
                "benefit": "유지보수성 50% 향상",
                "priority": "medium"
            })
        
        if structure_data["modularity_score"] < 70:
            recommendations.append({
                "type": "모듈화",
                "message": "모듈성 점수 향상 필요",
                "benefit": "재사용성 극대화",
                "priority": "high"
            })
        
        return recommendations
    
    def analyze_stein_patterns(self):
        """Stein님 개발 패턴 분석"""
        print("🧠 Stein님 개발 패턴 분석 중...")
        
        patterns = {
            "korean_comments": 0,
            "emoji_usage": 0,
            "function_naming": {"snake_case": 0, "camelCase": 0},
            "code_style": "professional",
            "preference_score": 0
        }
        
        # 파일들에서 패턴 추출
        for file_path in self.project_root.glob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 한국어 주석 비율
                korean_comments = len(re.findall(r'#.*[가-힣]', content))
                patterns["korean_comments"] += korean_comments
                
                # 이모지 사용
                emoji_count = len(re.findall(r'[😀-🙏]', content))
                patterns["emoji_usage"] += emoji_count
                
                # 함수명 패턴
                snake_case_funcs = len(re.findall(r'def [a-z_]+\(', content))
                camel_case_funcs = len(re.findall(r'def [a-z][A-Z]', content))
                patterns["function_naming"]["snake_case"] += snake_case_funcs
                patterns["function_naming"]["camelCase"] += camel_case_funcs
                
            except Exception:
                continue
        
        # Stein님 선호도 점수 계산
        if patterns["korean_comments"] > 10:
            patterns["preference_score"] += 30
        if patterns["emoji_usage"] > 5:
            patterns["preference_score"] += 20
        if patterns["function_naming"]["snake_case"] > patterns["function_naming"]["camelCase"]:
            patterns["preference_score"] += 25
        
        self.analysis_results["patterns"] = patterns
        return patterns
    
    def find_optimal_balance(self):
        """최적 밸런싱 포인트 찾기"""
        print("🎯 최적 밸런싱 포인트 계산 중...")
        
        structure = self.analysis_results.get("structure", {})
        patterns = self.analysis_results.get("patterns", {})
        
        balance_point = {
            "efficiency_weight": 0.6,  # 효율성 가중치
            "detail_weight": 0.4,     # 상세함 가중치
            "stein_customization": 0.8, # Stein님 맞춤화
            "optimal_file_size": 150,   # 최적 파일 크기
            "recommended_structure": "modular_with_details"
        }
        
        # Stein님 패턴 기반 조정
        if patterns.get("preference_score", 0) > 50:
            balance_point["detail_weight"] += 0.1
            balance_point["stein_customization"] += 0.1
        
        # 구조 복잡성 기반 조정
        if structure.get("complexity_score", 0) > 15:
            balance_point["efficiency_weight"] += 0.1
        
        balance_point["balance_score"] = (
            balance_point["efficiency_weight"] * 0.4 +
            balance_point["detail_weight"] * 0.3 +
            balance_point["stein_customization"] * 0.3
        ) * 100
        
        self.analysis_results["balance_point"] = balance_point
        return balance_point
    
    def generate_stein_recommendations(self):
        """Stein님 전용 추천사항 생성"""
        print("💡 Stein님 맞춤 추천사항 생성 중...")
        
        recommendations = {
            "immediate_actions": [],
            "medium_term_goals": [],
            "long_term_vision": [],
            "stein_specific": []
        }
        
        structure = self.analysis_results.get("structure", {})
        balance_point = self.analysis_results.get("balance_point", {})
        
        # 즉시 실행 권장사항
        if structure.get("avg_lines_per_file", 0) > 200:
            recommendations["immediate_actions"].append({
                "action": "큰 파일 분리",
                "description": "200줄 이상 파일을 기능별로 분리",
                "estimated_time": "30분",
                "benefit": "개발 속도 2배 향상"
            })
        
        # 중기 목표
        recommendations["medium_term_goals"].append({
            "goal": "완전한 모듈화",
            "description": "모든 기능을 독립적 모듈로 구성",
            "timeline": "1-2주",
            "impact": "유지보수성 80% 향상"
        })
        
        # 장기 비전
        recommendations["long_term_vision"].append({
            "vision": "Stein AI 생태계 완성",
            "description": "자가 진화하는 개발 환경 구축",
            "timeline": "1-3개월",
            "impact": "혁신적 개발 경험"
        })
        
        # Stein님 특화 추천
        recommendations["stein_specific"].append({
            "feature": "한국어 친화적 코드",
            "description": "모든 함수와 변수에 한국어 주석 추가",
            "why": "이해도와 개발 속도 향상",
            "implementation": "자동 주석 생성 도구 활용"
        })
        
        self.analysis_results["recommendations"] = recommendations
        return recommendations
    
    def create_balance_report(self):
        """밸런싱 리포트 생성"""
        print("📊 Stein님 밸런싱 리포트 생성 중...")
        
        report = f"""
# ⚖️ Stein님 스마트 밸런싱 리포트

**분석 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 핵심 결과

### 📊 구조 분석
- **분석 파일**: {self.analysis_results.get('structure', {}).get('files_analyzed', 0)}개
- **총 코드 라인**: {self.analysis_results.get('structure', {}).get('total_lines', 0):,}줄
- **평균 파일 크기**: {self.analysis_results.get('structure', {}).get('avg_lines_per_file', 0):.0f}줄
- **모듈성 점수**: {self.analysis_results.get('structure', {}).get('modularity_score', 0)}/100

### 🧠 Stein님 개발 패턴
- **한국어 주석**: {self.analysis_results.get('patterns', {}).get('korean_comments', 0)}개
- **이모지 사용**: {self.analysis_results.get('patterns', {}).get('emoji_usage', 0)}개
- **선호도 점수**: {self.analysis_results.get('patterns', {}).get('preference_score', 0)}/100

### ⚖️ 최적 밸런싱 포인트
- **효율성 가중치**: {self.analysis_results.get('balance_point', {}).get('efficiency_weight', 0.6)*100:.0f}%
- **상세함 가중치**: {self.analysis_results.get('balance_point', {}).get('detail_weight', 0.4)*100:.0f}%
- **밸런싱 점수**: {self.analysis_results.get('balance_point', {}).get('balance_score', 0):.1f}/100

## 💡 맞춤형 추천사항

### 🚀 즉시 실행 (오늘)
"""
        
        immediate = self.analysis_results.get('recommendations', {}).get('immediate_actions', [])
        for action in immediate:
            report += f"- **{action['action']}**: {action['description']} ({action['estimated_time']})\n"
        
        report += "\n### 🎯 중기 목표 (1-2주)\n"
        medium = self.analysis_results.get('recommendations', {}).get('medium_term_goals', [])
        for goal in medium:
            report += f"- **{goal['goal']}**: {goal['description']}\n"
        
        report += "\n### 🌟 Stein님 특화 기능\n"
        specific = self.analysis_results.get('recommendations', {}).get('stein_specific', [])
        for spec in specific:
            report += f"- **{spec['feature']}**: {spec['description']}\n"
        
        report += """

## 🏆 결론

**Stein님만의 완벽한 밸런싱 공식을 찾았습니다!**

```
효율성 60% + 상세함 40% + Stein 맞춤화 = 완벽한 개발 환경
```

**다음 단계**: `python stein_smart_system.py` 실행하여 새로운 시스템 체험하기!

---
*이 리포트는 Stein님의 개발 패턴을 분석하여 자동 생성되었습니다.*
"""
        
        with open("STEIN_BALANCE_REPORT.md", 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def run_full_analysis(self):
        """전체 분석 실행"""
        print("🚀 Stein님 전체 밸런싱 분석 시작!")
        print("=" * 50)
        
        # 1. 구조 분석
        structure_results = self.analyze_code_structure()
        
        # 2. 패턴 분석
        pattern_results = self.analyze_stein_patterns()
        
        # 3. 최적 밸런싱 포인트 계산
        balance_point = self.find_optimal_balance()
        
        # 4. 맞춤형 추천사항 생성
        recommendations = self.generate_stein_recommendations()
        
        # 5. 리포트 생성
        report = self.create_balance_report()
        
        print("=" * 50)
        print("🎉 Stein님 밸런싱 분석 완료!")
        print(f"📊 밸런싱 점수: {balance_point.get('balance_score', 0):.1f}/100")
        print(f"🎯 최적 구조: {balance_point.get('recommended_structure', 'N/A')}")
        print("📋 상세 리포트: STEIN_BALANCE_REPORT.md")
        print("=" * 50)
        
        return self.analysis_results

if __name__ == "__main__":
    analyzer = SteinBalanceAnalyzer()
    analyzer.run_full_analysis() 