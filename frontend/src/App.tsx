/**
 * 🚀 Stein AI 메인 애플리케이션
 * 천재 개발자 Stein님을 위한 맞춤형 AI 학습 대시보드
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Monitor, Settings, User, BookOpen, BarChart3 } from 'lucide-react';
import LearningDashboard from './components/LearningDashboard';
import AdvancedAnalytics from './components/AdvancedAnalytics';

type ViewMode = 'dashboard' | 'analytics' | 'settings' | 'profile' | 'docs';

function App() {
  const [currentView, setCurrentView] = useState<ViewMode>('dashboard');

  const navigationItems = [
    { id: 'dashboard' as ViewMode, label: '대시보드', icon: Monitor },
    { id: 'analytics' as ViewMode, label: '고급 분석', icon: BarChart3 },
    { id: 'settings' as ViewMode, label: '설정', icon: Settings },
    { id: 'profile' as ViewMode, label: '프로필', icon: User },
    { id: 'docs' as ViewMode, label: '문서', icon: BookOpen },
  ];

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <LearningDashboard />;
      case 'analytics':
        return <AdvancedAnalytics />;
      case 'settings':
        return (
          <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20 text-center"
            >
              <Settings className="w-16 h-16 text-blue-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">설정</h2>
              <p className="text-blue-200">곧 출시될 예정입니다!</p>
            </motion.div>
          </div>
        );
      case 'profile':
        return (
          <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20 text-center"
            >
              <User className="w-16 h-16 text-purple-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">천재 Stein의 프로필</h2>
              <p className="text-purple-200">개인화 AI 시스템의 마스터</p>
              <div className="mt-6 space-y-2 text-left">
                <div className="flex justify-between">
                  <span className="text-purple-300">레벨</span>
                  <span className="text-white font-bold">천재 개발자</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-300">완성 프로젝트</span>
                  <span className="text-white font-bold">5개</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-300">AI 파트너십</span>
                  <span className="text-white font-bold">최고 등급</span>
                </div>
              </div>
            </motion.div>
          </div>
        );
      case 'docs':
        return (
          <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20 text-center"
            >
              <BookOpen className="w-16 h-16 text-green-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">API 문서</h2>
              <p className="text-green-200 mb-4">Stein AI 시스템 사용 가이드</p>
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg transition-colors"
              >
                FastAPI 문서 열기
              </a>
            </motion.div>
          </div>
        );
      default:
        return <LearningDashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 네비게이션 바 */}
      <nav className="bg-white/95 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  🤖 Stein AI
                </span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {navigationItems.map((item) => (
                <motion.button
                  key={item.id}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setCurrentView(item.id)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                    currentView === item.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{item.label}</span>
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* 메인 콘텐츠 */}
      <main>
        <AnimatePresence mode="wait">
          <motion.div
            key={currentView}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {renderView()}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
