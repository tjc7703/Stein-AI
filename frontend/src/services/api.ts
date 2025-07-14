/**
 * 🚀 Stein AI API 서비스
 * 백엔드와의 모든 통신을 관리하는 중앙화된 API 레이어
 */

import axios from 'axios';

// API 베이스 URL 설정
const API_BASE_URL = 'http://localhost:8000';

// Axios 인스턴스 생성
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 응답 인터셉터 - 에러 처리
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API 요청 오류:', error);
    return Promise.reject(error);
  }
);

// 🔄 자동 학습 루프 관련 API
export interface FeedbackRequest {
  user_id?: string;
  session_id: string;
  question: string;
  response: string;
  rating: number; // 1-5
  feedback_text?: string;
  response_time?: number;
  quality_score?: number;
}

export interface LearningMetrics {
  avg_rating: number;
  response_time_trend: number;
  question_quality_improvement: number;
  user_satisfaction_trend: number;
  learning_velocity: number;
  confidence_score: number;
}

export interface LearningDashboard {
  learning_metrics: LearningMetrics;
  pattern_counts: {
    question_patterns: number;
    response_patterns: number;
    user_preferences: number;
    improvement_rules: number;
  };
  system_health: {
    status: string;
    confidence: string;
    learning_rate: string;
    user_satisfaction: string;
  };
}

export interface QuestionAnalysis {
  original_question: string;
  quality_analysis: {
    score: number;
    level: string;
  };
  suggestions: string[];
  optimized_question: string;
  stein_personalization: any;
}

// API 함수들
export const steinApi = {
  // 📊 대시보드 데이터 조회
  async getLearningDashboard(): Promise<LearningDashboard> {
    const response = await api.get('/stein/learning/dashboard');
    return response.data.learning_dashboard;
  },

  // 📈 상세 학습 통계
  async getLearningStats() {
    const response = await api.get('/stein/learning/stats');
    return response.data;
  },

  // 💬 피드백 제출
  async submitFeedback(feedback: FeedbackRequest) {
    const response = await api.post('/stein/learning/feedback', feedback);
    return response.data;
  },

  // 💡 개선 제안 요청
  async getImprovementSuggestions(question: string) {
    const response = await api.post('/stein/learning/suggestions', {
      question,
      analyze_depth: 'full',
    });
    return response.data;
  },

  // 🚀 학습 적용
  async applyLearning(question: string) {
    const response = await api.post('/stein/learning/apply', {
      question,
    });
    return response.data;
  },

  // 🎮 학습 데모 실행
  async runLearningDemo() {
    const response = await api.post('/stein/learning/demo');
    return response.data;
  },

  // 🧠 질문 분석
  async analyzeQuestion(question: string): Promise<QuestionAnalysis> {
    const response = await api.post('/stein/analyze-question', {
      question,
      analyze_depth: 'full',
    });
    return response.data;
  },

  // 🤖 자동 판별
  async autoDetect(question: string) {
    const response = await api.post('/stein/auto-detect', {
      question,
      include_personalization: true,
    });
    return response.data;
  },

  // 🔍 시스템 상태 확인
  async getHealthCheck() {
    const response = await api.get('/stein/health');
    return response.data;
  },

  // 📋 질문 패턴 가이드
  async getQuestionPatterns() {
    const response = await api.get('/stein/question-patterns');
    return response.data;
  },

  // 🎯 데모 실행
  async runDemo() {
    const response = await api.post('/stein/demo/analyze');
    return response.data;
  },

  // 💎 천재 개발자 분석
  async getGeniusAnalysis(question: string) {
    const response = await api.post('/stein/genius-analysis', {
      question,
    });
    return response.data;
  },

  // 📊 정직한 평가
  async getHonestEvaluation() {
    const response = await api.post('/stein/honest-evaluation', {
      question: 'Stein의 현재 능력 평가',
    });
    return response.data;
  },
};

// 유틸리티 함수들
export const apiUtils = {
  // 에러 메시지 추출
  getErrorMessage(error: any): string {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }
    if (error.message) {
      return error.message;
    }
    return '알 수 없는 오류가 발생했습니다.';
  },

  // 성공 여부 확인
  isSuccess(response: any): boolean {
    return response?.status === 'success' || response?.success === true;
  },

  // 데이터 변환
  formatTimestamp(timestamp: string): string {
    return new Date(timestamp).toLocaleString('ko-KR');
  },

  // 점수를 백분율로 변환
  toPercentage(value: number): string {
    return `${(value * 100).toFixed(1)}%`;
  },

  // 평점을 별점으로 변환
  toStars(rating: number): string {
    const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    return `${stars} (${rating.toFixed(1)})`;
  },
};

export default steinApi; 