/**
 * 📊 Stein AI 고급 분석 대시보드
 * ML 예측 결과 및 패턴 분석 시각화
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  TrendingUp, 
  BarChart3, 
  Brain,
  Target,
  Activity,
  CheckCircle2,
  AlertCircle,
  Clock,
  Award,
  Zap
} from 'lucide-react';

const AdvancedAnalytics = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'predictions' | 'patterns' | 'insights'>('predictions');

  useEffect(() => {
    // 시뮬레이션을 위한 로딩
    setTimeout(() => setIsLoading(false), 1500);
  }, []);

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                📊 고급 AI 분석 대시보드
              </h1>
              <p className="text-blue-200">
                머신러닝 기반 성능 예측 및 패턴 분석
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white px-6 py-3 rounded-lg font-medium transition-all"
            >
              🎪 ML 데모 실행
            </motion.button>
          </div>

          {/* 탭 네비게이션 */}
          <div className="flex space-x-4">
            {[
              { id: 'predictions', label: '🔮 성능 예측', icon: TrendingUp },
              { id: 'patterns', label: '📈 패턴 분석', icon: BarChart3 },
              { id: 'insights', label: '💡 AI 인사이트', icon: Brain }
            ].map((tab) => (
              <motion.button
                key={tab.id}
                whileHover={{ scale: 1.02 }}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                  activeTab === tab.id
                    ? 'bg-white/20 text-white'
                    : 'bg-white/5 text-blue-200 hover:bg-white/10'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* ML 시스템 상태 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-6 h-6 text-green-400" />
              <div>
                <h3 className="text-white font-bold">ML 시스템 상태</h3>
                <p className="text-green-200">
                  100% 학습 완료 (4/4 모델)
                </p>
              </div>
            </div>
            <div className="flex space-x-2">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="p-2 rounded-lg bg-green-500/20">
                  <CheckCircle2 className="w-4 h-4 text-green-400" />
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* 탭 컨텐츠 */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {activeTab === 'predictions' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white mb-4">🔮 미래 성능 예측</h2>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {[
                    { horizon: '1일', current: 4.2, predicted: 4.5, confidence: '87%', trend: '상승' },
                    { horizon: '1주', current: 4.2, predicted: 4.7, confidence: '82%', trend: '상승' },
                    { horizon: '1개월', current: 4.2, predicted: 4.8, confidence: '75%', trend: '상승' }
                  ].map((pred, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
                    >
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-white font-bold">{pred.horizon} 예측</h3>
                        <div className="flex items-center space-x-1 px-2 py-1 rounded-lg text-green-400 bg-green-500/10 border-green-500/20">
                          <TrendingUp className="w-4 h-4" />
                          <span className="text-sm font-medium">{pred.trend}</span>
                        </div>
                      </div>

                      <div className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-blue-200">현재 점수</span>
                          <span className="text-white font-bold">{pred.current}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-blue-200">예측 점수</span>
                          <span className="text-white font-bold">{pred.predicted}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-blue-200">신뢰도</span>
                          <span className="text-green-400 font-bold">{pred.confidence}</span>
                        </div>
                      </div>

                      <div className="mt-4">
                        <p className="text-blue-200 text-sm mb-2">주요 영향 요인:</p>
                        <div className="flex flex-wrap gap-1">
                          {['질문_품질', '응답_시간', '학습_패턴'].map((factor, idx) => (
                            <span key={idx} className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-xs">
                              {factor}
                            </span>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'patterns' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white mb-4">📈 학습 패턴 분석</h2>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* 시간대별 패턴 */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
                  >
                    <div className="flex items-center space-x-3 mb-4">
                      <Clock className="w-6 h-6 text-orange-400" />
                      <h3 className="text-white font-bold">시간대별 성과</h3>
                    </div>
                    <p className="text-blue-200 mb-4">가장 좋은 성과를 내는 시간: 14시, 20시, 22시</p>
                    <div className="space-y-2">
                      <span className="text-orange-300 text-sm">최적 학습 시간:</span>
                      <div className="flex flex-wrap gap-2">
                        {[14, 20, 22].map(hour => (
                          <span key={hour} className="bg-orange-500/20 text-orange-300 px-3 py-1 rounded-lg">
                            {hour}시
                          </span>
                        ))}
                      </div>
                    </div>
                  </motion.div>

                  {/* 주제별 패턴 */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
                  >
                    <div className="flex items-center space-x-3 mb-4">
                      <Target className="w-6 h-6 text-purple-400" />
                      <h3 className="text-white font-bold">주제별 강점</h3>
                    </div>
                    <p className="text-blue-200 mb-4">가장 강한 영역: 코딩 (평점 4.7)</p>
                    <div className="bg-purple-500/20 p-3 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <Award className="w-5 h-5 text-purple-400" />
                        <span className="text-purple-300 font-medium">
                          최강 영역: 코딩
                        </span>
                      </div>
                    </div>
                  </motion.div>

                  {/* 진화 패턴 */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 lg:col-span-2"
                  >
                    <div className="flex items-center space-x-3 mb-4">
                      <Zap className="w-6 h-6 text-green-400" />
                      <h3 className="text-white font-bold">학습 진화</h3>
                    </div>
                    <p className="text-blue-200 mb-4">학습 진화율: 15.2% 개선</p>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-400">15.2%</div>
                        <div className="text-green-300 text-sm">개선율</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-white">20</div>
                        <div className="text-blue-300 text-sm">총 세션</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-yellow-400">4.6</div>
                        <div className="text-yellow-300 text-sm">평균 평점</div>
                      </div>
                    </div>
                  </motion.div>
                </div>
              </div>
            )}

            {activeTab === 'insights' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white mb-4">💡 AI 인사이트 & 추천</h2>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* 핵심 인사이트 */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
                  >
                    <div className="flex items-center space-x-3 mb-4">
                      <Brain className="w-6 h-6 text-blue-400" />
                      <h3 className="text-white font-bold">핵심 인사이트</h3>
                    </div>
                    <div className="space-y-3">
                      {[
                        '📈 전체 학습 세션: 20회',
                        '⭐ 평균 만족도: 4.6/5.0',
                        '🎯 코딩 영역에서 뛰어남',
                        '⏰ 14시 경에 최고 성과',
                        '📊 지속적인 개선 추세'
                      ].map((insight, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="flex items-center space-x-3 p-3 bg-blue-500/10 rounded-lg"
                        >
                          <div className="w-2 h-2 bg-blue-400 rounded-full flex-shrink-0" />
                          <span className="text-blue-200">{insight}</span>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>

                  {/* AI 추천사항 */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20"
                  >
                    <div className="flex items-center space-x-3 mb-4">
                      <Target className="w-6 h-6 text-purple-400" />
                      <h3 className="text-white font-bold">개선 추천</h3>
                    </div>
                    <div className="space-y-3">
                      {[
                        "🎯 질문을 더 구체적으로 작성하세요",
                        "📚 정기적인 피드백으로 AI 성능 개선",
                        "🧠 다양한 주제로 학습 범위 확장",
                        "⏰ 14-22시 시간대 활용한 학습 계획",
                        "🚀 코딩 강점을 다른 분야에 적용"
                      ].map((recommendation, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="flex items-center space-x-3 p-3 bg-purple-500/10 rounded-lg"
                        >
                          <div className="w-2 h-2 bg-purple-400 rounded-full flex-shrink-0" />
                          <span className="text-purple-200">{recommendation}</span>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};

export default AdvancedAnalytics; 