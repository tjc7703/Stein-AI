"""
🧠 Stein AI 핵심 엔진 - 고급 학습 및 메타인지 시스템
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class QuestionQuality(Enum):
    """질문 품질 등급"""
    EXCELLENT = "excellent"  # 9-10점
    GOOD = "good"           # 7-8점  
    AVERAGE = "average"     # 5-6점
    POOR = "poor"          # 1-4점

class LearningDepth(Enum):
    """학습 깊이 수준"""
    SURFACE = "surface"     # 표면적 이해
    SHALLOW = "shallow"     # 얕은 이해
    DEEP = "deep"          # 깊은 이해
    EXPERT = "expert"      # 전문가 수준

@dataclass
class QuestionAnalysis:
    """질문 분석 결과"""
    quality_score: float
    quality_level: QuestionQuality
    clarity_score: float
    specificity_score: float
    context_score: float
    suggestions: List[str]
    optimized_question: str

@dataclass
class PaperInfo:
    """논문 정보"""
    title: str
    authors: List[str]
    url: str
    license: str
    source: str
    access_type: str  # "open", "restricted", "fair_use"

class SteinMetaCognitiveEngine:
    """Stein AI 메타인지 엔진"""
    
    def __init__(self):
        self.question_patterns = {
            "goal_oriented": r"(목표|달성|결과|원하는|만들고|구현)",
            "problem_solving": r"(문제|에러|해결|수정|고치)",
            "learning_focused": r"(배우|학습|이해|알고|설명)",
            "comparison": r"(비교|차이|대신|vs|또는)",
            "optimization": r"(최적|효율|성능|개선|향상)"
        }
        
        self.quality_indicators = {
            "specific_terms": r"(\w+\.\w+|\w+==\d+|API|JWT|React|FastAPI)",
            "context_words": r"(현재|프로젝트|상황|조건|환경)",
            "action_words": r"(구현|생성|만들|설계|분석|테스트)",
            "constraint_words": r"(제한|조건|요구사항|필수|선택)"
        }

    def analyze_question(self, question: str) -> QuestionAnalysis:
        """질문 품질 분석 및 개선 제안"""
        
        # 1. 명확성 점수 (Clarity Score)
        clarity_score = self._calculate_clarity(question)
        
        # 2. 구체성 점수 (Specificity Score) 
        specificity_score = self._calculate_specificity(question)
        
        # 3. 컨텍스트 점수 (Context Score)
        context_score = self._calculate_context(question)
        
        # 4. 전체 품질 점수
        quality_score = (clarity_score + specificity_score + context_score) / 3
        
        # 5. 품질 등급 결정
        quality_level = self._determine_quality_level(quality_score)
        
        # 6. 개선 제안 생성
        suggestions = self._generate_suggestions(question, clarity_score, specificity_score, context_score)
        
        # 7. 최적화된 질문 생성
        optimized_question = self._optimize_question(question, suggestions)
        
        return QuestionAnalysis(
            quality_score=quality_score,
            quality_level=quality_level,
            clarity_score=clarity_score,
            specificity_score=specificity_score,
            context_score=context_score,
            suggestions=suggestions,
            optimized_question=optimized_question
        )

    def _calculate_clarity(self, question: str) -> float:
        """명확성 점수 계산"""
        score = 5.0  # 기본 점수
        
        # 긍정적 요소들
        if len(question) > 20:  # 충분한 길이
            score += 1.0
        if '?' in question:  # 질문 형태
            score += 1.0
        if any(word in question.lower() for word in ['어떻게', '왜', '무엇을', '언제', '어디서']):
            score += 1.5
        
        # 부정적 요소들
        if len(question) < 10:  # 너무 짧음
            score -= 2.0
        if '이거' in question or '그거' in question:  # 지시대명사 사용
            score -= 1.0
        if '좋게' in question and '어떻게' not in question:  # 모호한 표현
            score -= 1.5
            
        return max(0.0, min(10.0, score))

    def _calculate_specificity(self, question: str) -> float:
        """구체성 점수 계산"""
        score = 3.0
        
        # 구체적 기술 용어 사용
        for pattern in self.quality_indicators.values():
            matches = len(re.findall(pattern, question, re.IGNORECASE))
            score += matches * 0.5
            
        # 숫자나 버전 명시
        if re.search(r'\d+', question):
            score += 1.0
            
        # 구체적 도구/프레임워크 언급
        tools = ['Python', 'FastAPI', 'React', 'JWT', 'Docker', 'PostgreSQL']
        mentioned_tools = sum(1 for tool in tools if tool.lower() in question.lower())
        score += mentioned_tools * 0.8
        
        return max(0.0, min(10.0, score))

    def _calculate_context(self, question: str) -> float:
        """컨텍스트 점수 계산"""
        score = 4.0
        
        # 상황 설명
        context_indicators = ['현재', '프로젝트에서', '상황', '환경', '조건']
        for indicator in context_indicators:
            if indicator in question:
                score += 1.0
                
        # 제약조건 명시
        constraint_indicators = ['제한', '요구사항', '필수', '조건']
        for constraint in constraint_indicators:
            if constraint in question:
                score += 1.5
                
        return max(0.0, min(10.0, score))

    def _determine_quality_level(self, score: float) -> QuestionQuality:
        """품질 등급 결정"""
        if score >= 8.5:
            return QuestionQuality.EXCELLENT
        elif score >= 7.0:
            return QuestionQuality.GOOD
        elif score >= 5.0:
            return QuestionQuality.AVERAGE
        else:
            return QuestionQuality.POOR

    def _generate_suggestions(self, question: str, clarity: float, specificity: float, context: float) -> List[str]:
        """개선 제안 생성"""
        suggestions = []
        
        if clarity < 6.0:
            suggestions.append("🎯 목표를 더 명확하게 표현해보세요 (예: '성능을 개선하고 싶어' → '응답 속도를 50% 개선하고 싶어')")
            
        if specificity < 6.0:
            suggestions.append("🔧 구체적인 기술이나 도구를 명시해보세요 (예: 'API' → 'FastAPI REST API')")
            
        if context < 6.0:
            suggestions.append("📍 현재 상황과 제약조건을 추가해보세요 (예: '현재 React 프로젝트에서 인증 기능을 추가하려는데...')")
            
        if '이거' in question or '그거' in question:
            suggestions.append("📝 지시대명사 대신 구체적인 명칭을 사용해보세요")
            
        if '좋게' in question and '어떻게' not in question:
            suggestions.append("📊 개선 방향을 구체화해보세요 (성능, 보안, 가독성, 유지보수성 등)")
            
        return suggestions

    def _optimize_question(self, question: str, suggestions: List[str]) -> str:
        """질문 최적화"""
        if not suggestions:
            return question + " (이미 훌륭한 질문입니다! 👍)"
            
        # 기본적인 최적화 패턴들
        optimized = question
        
        # 지시대명사 개선
        optimized = re.sub(r'이거|그거', '[구체적 대상]', optimized)
        
        # 모호한 표현 개선
        if '좋게' in optimized:
            optimized = optimized.replace('좋게', '[어떤 측면에서] 개선')
            
        # 질문 구조화 제안
        if '?' not in optimized:
            optimized += "?"
            
        return f"🎯 최적화 제안: {optimized}\n\n💡 추가 고려사항:\n" + "\n".join(f"- {s}" for s in suggestions[:3])

class SteinPaperLearningSystem:
    """Stein AI 논문 학습 시스템"""
    
    def __init__(self):
        self.open_access_sources = {
            "arxiv.org": "완전 오픈 액세스",
            "biorxiv.org": "생물학 프리프린트",
            "plos.org": "PLOS 저널",
            "doaj.org": "오픈 액세스 저널 디렉토리"
        }
        
        self.fair_use_guidelines = {
            "max_quote_length": 250,  # 최대 인용 길이
            "summary_allowed": True,   # 요약 허용
            "methodology_learning": True,  # 방법론 학습 허용
            "full_text_copy": False   # 전문 복사 금지
        }

    def analyze_paper_access(self, paper_info: PaperInfo) -> Dict[str, any]:
        """논문 접근성 분석"""
        
        analysis = {
            "can_learn": False,
            "access_type": "unknown",
            "restrictions": [],
            "alternatives": []
        }
        
        # 오픈 액세스 확인
        if any(source in paper_info.url.lower() for source in self.open_access_sources.keys()):
            analysis["can_learn"] = True
            analysis["access_type"] = "open_access"
            analysis["learning_scope"] = "full"
            
        # Creative Commons 라이센스 확인
        elif "cc-" in paper_info.license.lower() or "creative commons" in paper_info.license.lower():
            analysis["can_learn"] = True
            analysis["access_type"] = "cc_licensed"
            analysis["learning_scope"] = "full_with_attribution"
            
        # 페어유즈 범위 확인
        elif "fair use" in paper_info.license.lower() or paper_info.source.lower() in ["academic", "research"]:
            analysis["can_learn"] = True
            analysis["access_type"] = "fair_use"
            analysis["learning_scope"] = "limited"
            analysis["restrictions"] = [
                f"인용 길이 {self.fair_use_guidelines['max_quote_length']}자 이하",
                "요약 및 방법론 학습만 가능",
                "상업적 사용 금지"
            ]
            
        else:
            analysis["can_learn"] = False
            analysis["access_type"] = "restricted"
            analysis["restrictions"] = ["저작권 보호로 학습 불가"]
            analysis["alternatives"] = self._find_open_alternatives(paper_info.title)
            
        return analysis

    def _find_open_alternatives(self, title: str) -> List[str]:
        """오픈 액세스 대안 논문 검색"""
        # 실제로는 arXiv API나 DOAJ API를 사용
        keywords = self._extract_keywords(title)
        alternatives = [
            f"arXiv 검색: {' '.join(keywords[:3])}",
            f"PLOS ONE 검색: {' '.join(keywords[:2])}",
            f"Nature Communications 오픈 액세스 섹션"
        ]
        return alternatives

    def _extract_keywords(self, title: str) -> List[str]:
        """제목에서 키워드 추출"""
        # 간단한 키워드 추출 (실제로는 더 정교한 NLP 사용)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\w+', title.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return keywords[:5]  # 상위 5개 키워드

    def ethical_learning_summary(self, paper_info: PaperInfo, learning_depth: LearningDepth = LearningDepth.SHALLOW) -> str:
        """윤리적 논문 학습 요약"""
        
        access_analysis = self.analyze_paper_access(paper_info)
        
        if not access_analysis["can_learn"]:
            return f"""
🚫 학습 제한: {paper_info.title}

❌ 사유: {', '.join(access_analysis["restrictions"])}

🔍 대안 검색:
{chr(10).join(f"• {alt}" for alt in access_analysis["alternatives"])}

💡 추천: 오픈 액세스 논문을 활용해보세요!
"""
        
        if access_analysis["access_type"] == "fair_use":
            return f"""
⚖️ 제한적 학습 가능: {paper_info.title}

📋 학습 범위:
• 논문 요약 및 핵심 아이디어 ✅
• 연구 방법론 학습 ✅  
• 기술적 접근법 분석 ✅
• 전문 복사 ❌
• 상업적 활용 ❌

🎯 윤리적 학습 결과:
[여기에 논문의 핵심 내용 요약이 들어갑니다]
"""
        
        return f"""
✅ 완전한 학습 가능: {paper_info.title}

📖 라이센스: {paper_info.license}
🌐 출처: {paper_info.source}

🧠 학습 내용:
[여기에 상세한 논문 분석이 들어갑니다]
"""

class SteinAIEngine:
    """통합 Stein AI 엔진"""
    
    def __init__(self):
        self.metacognitive_engine = SteinMetaCognitiveEngine()
        self.paper_learning_system = SteinPaperLearningSystem()
        self.learning_history = []
        self.user_preferences = self._load_stein_preferences()

    def _load_stein_preferences(self) -> Dict[str, any]:
        """Stein님 개인화 설정 로드"""
        return {
            "coding_style": "snake_case",
            "comment_language": "korean", 
            "explanation_depth": "detailed",
            "tech_stack": ["Python", "FastAPI", "React", "TypeScript"],
            "learning_style": "hands_on",
            "feedback_preference": "immediate"
        }

    def process_question(self, question: str) -> Dict[str, any]:
        """질문 처리 및 최적화"""
        
        # 1. 메타인지 분석
        analysis = self.metacognitive_engine.analyze_question(question)
        
        # 2. 학습 히스토리에 기록
        self.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "original_question": question,
            "quality_score": analysis.quality_score,
            "quality_level": analysis.quality_level.value
        })
        
        # 3. 응답 구성
        response = {
            "original_question": question,
            "quality_analysis": {
                "score": analysis.quality_score,
                "level": analysis.quality_level.value,
                "breakdown": {
                    "clarity": analysis.clarity_score,
                    "specificity": analysis.specificity_score,
                    "context": analysis.context_score
                }
            },
            "suggestions": analysis.suggestions,
            "optimized_question": analysis.optimized_question,
            "stein_personalization": self._apply_stein_style(analysis)
        }
        
        return response

    def _apply_stein_style(self, analysis: QuestionAnalysis) -> Dict[str, str]:
        """Stein님 스타일 적용"""
        
        encouragement = "🎯 Stein님답게 정말 좋은 질문이에요!"
        
        if analysis.quality_level == QuestionQuality.EXCELLENT:
            encouragement = "🏆 완벽한 질문입니다! 천재 개발자 Stein님다워요!"
        elif analysis.quality_level == QuestionQuality.GOOD:
            encouragement = "✨ 훌륭한 질문이에요! 조금만 더 구체화하면 완벽해질 거예요!"
        elif analysis.quality_level == QuestionQuality.AVERAGE:
            encouragement = "👍 좋은 시작이에요! Stein님의 창의성을 더 발휘해보세요!"
        else:
            encouragement = "💪 함께 더 나은 질문으로 발전시켜보겠습니다!"
            
        return {
            "encouragement": encouragement,
            "personalized_tips": f"Stein님의 {', '.join(self.user_preferences['tech_stack'])} 전문성을 활용한 질문으로 발전시켜보세요!",
            "next_steps": "구현하고 싶은 구체적인 기능이나 해결하고 싶은 문제를 명시해주시면 더 정확한 도움을 드릴 수 있어요!"
        }

    def learn_from_paper(self, paper_url: str, title: str = "", learning_depth: LearningDepth = LearningDepth.SHALLOW) -> str:
        """논문으로부터 학습"""
        
        # 논문 정보 구성 (실제로는 URL에서 메타데이터 추출)
        paper_info = PaperInfo(
            title=title or "AI 논문",
            authors=["연구자들"],
            url=paper_url,
            license="unknown",
            source="academic",
            access_type="unknown"
        )
        
        return self.paper_learning_system.ethical_learning_summary(paper_info, learning_depth)

# 🚀 Stein AI 엔진 인스턴스
stein_ai = SteinAIEngine()

def analyze_stein_question(question: str) -> Dict[str, any]:
    """Stein님 질문 분석 함수"""
    return stein_ai.process_question(question)

def learn_from_research(paper_url: str, title: str = "") -> str:
    """연구 논문 학습 함수"""
    return stein_ai.learn_from_paper(paper_url, title) 