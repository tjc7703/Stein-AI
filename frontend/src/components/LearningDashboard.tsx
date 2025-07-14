/**
 * 🎨 Stein AI 학습 대시보드
 * 실시간 학습 상태 모니터링 및 시각화
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  TrendingUp, 
  Users, 
  Target, 
  Zap, 
  BarChart3,
  RefreshCw,
  Star,
  Clock,
  CheckCircle,
  AlertTriangle,
  Lightbulb
} from 'lucide-react';
import { steinApi, apiUtils, type LearningDashboard } from '../services/api';

interface DashboardStats {
  totalQuestions: number;
  averageRating: number;
  learningVelocity: number;
  confidenceScore: number;
}

const LearningDashboard = () => {
  const [dashboardData, setDashboardData] = useState<LearningDashboard | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  // 데이터 로딩
  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const data = await steinApi.getLearningDashboard();
      setDashboardData(data);
      setLastUpdated(new Date());
    } catch (err) {
      setError(apiUtils.getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  // 초기 로딩 및 자동 새로고침
  useEffect(() => {
    loadDashboardData();
    
    // 30초마다 자동 새로고침
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  // 통계 계산
  const stats: DashboardStats = {
    totalQuestions: dashboardData?.pattern_counts.question_patterns || 0,
    averageRating: dashboardData?.learning_metrics.avg_rating || 0,
    learningVelocity: dashboardData?.learning_metrics.learning_velocity || 0,
    confidenceScore: dashboardData?.learning_metrics.confidence_score || 0,
  };

  // 애니메이션 variants
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-16 h-16 border-4 border-white border-t-transparent rounded-full"
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-red-500/10 border border-red-500/20 rounded-lg p-6 text-center"
        >
          <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">연결 오류</h3>
          <p className="text-red-300 mb-4">{error}</p>
          <button
            onClick={loadDashboardData}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            다시 시도
          </button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-6">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-7xl mx-auto"
      >
        {/* 헤더 */}
        <motion.div variants={itemVariants} className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                🤖 Stein AI 학습 대시보드
              </h1>
              <p className="text-blue-200">
                실시간 학습 상태 및 성능 모니터링
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-blue-300">마지막 업데이트</p>
                <p className="text-white font-mono text-sm">
                  {lastUpdated.toLocaleTimeString('ko-KR')}
                </p>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={loadDashboardData}
                disabled={isLoading}
                className="bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white p-3 rounded-lg transition-colors"
              >
                <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
              </motion.button>
            </div>
          </div>
        </motion.div>

        {/* 주요 메트릭 카드들 */}
        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* 총 질문 수 */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Brain className="w-6 h-6 text-blue-400" />
              </div>
              <span className="text-2xl font-bold text-white">
                {stats.totalQuestions}
              </span>
            </div>
            <h3 className="text-blue-200 font-medium">분석된 질문</h3>
            <p className="text-sm text-blue-300 mt-1">누적 학습 데이터</p>
          </motion.div>

          {/* 평균 평점 */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-yellow-500/20 p-3 rounded-lg">
                <Star className="w-6 h-6 text-yellow-400" />
              </div>
              <span className="text-2xl font-bold text-white">
                {stats.averageRating.toFixed(1)}
              </span>
            </div>
            <h3 className="text-yellow-200 font-medium">평균 만족도</h3>
            <p className="text-sm text-yellow-300 mt-1">
              {apiUtils.toStars(stats.averageRating)}
            </p>
          </motion.div>

          {/* 학습 속도 */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-green-500/20 p-3 rounded-lg">
                <Zap className="w-6 h-6 text-green-400" />
              </div>
              <span className="text-2xl font-bold text-white">
                {apiUtils.toPercentage(stats.learningVelocity)}
              </span>
            </div>
            <h3 className="text-green-200 font-medium">학습 속도</h3>
            <p className="text-sm text-green-300 mt-1">실시간 개선율</p>
          </motion.div>

          {/* 신뢰도 점수 */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-purple-500/20 p-3 rounded-lg">
                <Target className="w-6 h-6 text-purple-400" />
              </div>
              <span className="text-2xl font-bold text-white">
                {apiUtils.toPercentage(stats.confidenceScore)}
              </span>
            </div>
            <h3 className="text-purple-200 font-medium">시스템 신뢰도</h3>
            <p className="text-sm text-purple-300 mt-1">예측 정확도</p>
          </motion.div>
        </motion.div>

        {/* 상세 분석 섹션 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* 학습 패턴 분석 */}
          <motion.div
            variants={itemVariants}
            className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center gap-3 mb-6">
              <BarChart3 className="w-6 h-6 text-blue-400" />
              <h2 className="text-xl font-bold text-white">학습 패턴 분석</h2>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-blue-200">질문 패턴</span>
                <span className="text-white font-bold">
                  {dashboardData?.pattern_counts.question_patterns || 0}개
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-blue-200">응답 패턴</span>
                <span className="text-white font-bold">
                  {dashboardData?.pattern_counts.response_patterns || 0}개
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-blue-200">사용자 선호도</span>
                <span className="text-white font-bold">
                  {dashboardData?.pattern_counts.user_preferences || 0}개
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-blue-200">개선 규칙</span>
                <span className="text-white font-bold">
                  {dashboardData?.pattern_counts.improvement_rules || 0}개
                </span>
              </div>
            </div>
          </motion.div>

          {/* 시스템 상태 */}
          <motion.div
            variants={itemVariants}
            className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center gap-3 mb-6">
              <CheckCircle className="w-6 h-6 text-green-400" />
              <h2 className="text-xl font-bold text-white">시스템 상태</h2>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-green-200">상태</span>
                <span className="text-green-400 font-bold">
                  {dashboardData?.system_health.status || '알 수 없음'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-green-200">학습률</span>
                <span className="text-white font-bold">
                  {dashboardData?.system_health.learning_rate || '0%'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-green-200">사용자 만족도</span>
                <span className="text-white font-bold">
                  {dashboardData?.system_health.user_satisfaction || '0/5.0'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-green-200">신뢰도</span>
                <span className="text-white font-bold">
                  {dashboardData?.system_health.confidence || '0%'}
                </span>
              </div>
            </div>
          </motion.div>
        </div>

        {/* 실시간 활동 피드 */}
        <motion.div
          variants={itemVariants}
          className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
        >
          <div className="flex items-center gap-3 mb-6">
            <Clock className="w-6 h-6 text-orange-400" />
            <h2 className="text-xl font-bold text-white">실시간 학습 활동</h2>
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-blue-500/10 rounded-lg">
              <Lightbulb className="w-5 h-5 text-blue-400" />
              <span className="text-blue-200">새로운 질문 패턴 학습 중...</span>
              <span className="text-xs text-blue-300 ml-auto">방금 전</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-green-500/10 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-400" />
              <span className="text-green-200">사용자 만족도 개선 감지</span>
              <span className="text-xs text-green-300 ml-auto">2분 전</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-purple-500/10 rounded-lg">
              <Users className="w-5 h-5 text-purple-400" />
              <span className="text-purple-200">개인화 설정 최적화 완료</span>
              <span className="text-xs text-purple-300 ml-auto">5분 전</span>
            </div>
          </div>
        </motion.div>

        {/* 푸터 정보 */}
        <motion.div
          variants={itemVariants}
          className="mt-8 text-center text-blue-300 text-sm"
        >
          <p>
            🚀 Stein AI는 지속적으로 학습하며 성장하고 있습니다 | 
            마지막 업데이트: {apiUtils.formatTimestamp(lastUpdated.toISOString())}
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default LearningDashboard; 