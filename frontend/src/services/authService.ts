// 🔐 Stein AI 인증 서비스 - 프로덕션 레벨 인증 시스템
// 분석된 패턴 적용: export const + AuthBindings + async + error handling

export interface AuthBindings {
  login: (params: LoginParams) => Promise<LoginResult>;
  logout: () => Promise<LogoutResult>;
  checkAuth: () => Promise<AuthCheckResult>;
  getIdentity: () => Promise<UserIdentity | null>;
}

export interface LoginParams {
  email: string;
  password?: string;
}

export interface LoginResult {
  success: boolean;
  redirectTo?: string;
  error?: {
    message: string;
    name: string;
  };
}

export interface LogoutResult {
  success: boolean;
  redirectTo?: string;
}

export interface AuthCheckResult {
  authenticated: boolean;
  redirectTo?: string;
}

export interface UserIdentity {
  id: string;
  name: string;
  email: string;
  role: string;
  avatarUrl?: string;
}

// 🌟 Stein AI 맞춤형 인증 제공자
export const steinAuthProvider: AuthBindings = {
  // 🔑 로그인 함수 - async를 통한 비동기 처리
  login: async ({ email, password }: LoginParams): Promise<LoginResult> => {
    try {
      // 📡 API 호출 - dataProvider.custom 패턴 적용
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST', // HTTP 메소드 - 데이터 변경이므로 POST
        headers: {
          'Content-Type': 'application/json', // JSON 데이터 전송
        },
        body: JSON.stringify({ // 요청 본문 - 로그인 정보
          email,
          password: password || 'demo-password', // 기본값 처리
        }),
      });

      if (!response.ok) {
        throw new Error('인증 실패');
      }

      const data = await response.json();
      
      // 🗄️ localStorage.setItem 패턴 - 토큰 저장
      localStorage.setItem('stein_access_token', data.accessToken);
      localStorage.setItem('stein_user_info', JSON.stringify(data.user));
      
      return {
        success: true,
        redirectTo: '/', // 성공 시 홈으로 리다이렉트
      };
    } catch (error) {
      // 🛡️ try-catch 패턴 - 에러 안전 처리
      return {
        success: false,
        error: {
          message: error instanceof Error ? error.message : '로그인 실패',
          name: 'AuthenticationError',
        },
      };
    }
  },

  // 🚪 로그아웃 함수 - 토큰 제거
  logout: async (): Promise<LogoutResult> => {
    // localStorage 정리 - 보안 중요!
    localStorage.removeItem('stein_access_token');
    localStorage.removeItem('stein_user_info');
    
    return {
      success: true,
      redirectTo: '/login',
    };
  },

  // ✅ 인증 확인 함수 - 토큰 유효성 검사
  checkAuth: async (): Promise<AuthCheckResult> => {
    try {
      const token = localStorage.getItem('stein_access_token');
      
      if (!token) {
        return {
          authenticated: false,
          redirectTo: '/login',
        };
      }

      // 🔍 토큰 검증 API 호출
      const response = await fetch('http://localhost:8000/auth/verify', {
        headers: {
          'Authorization': `Bearer ${token}`, // Bearer 토큰 인증
        },
      });

      if (response.ok) {
        return {
          authenticated: true,
        };
      } else {
        // 토큰 만료 시 정리
        localStorage.removeItem('stein_access_token');
        localStorage.removeItem('stein_user_info');
        
        return {
          authenticated: false,
          redirectTo: '/login',
        };
      }
    } catch (error) {
      return {
        authenticated: false,
        redirectTo: '/login',
      };
    }
  },

  // 👤 사용자 정보 가져오기 함수
  getIdentity: async (): Promise<UserIdentity | null> => {
    try {
      const userInfo = localStorage.getItem('stein_user_info');
      
      if (userInfo) {
        return JSON.parse(userInfo);
      }
      
      return null;
    } catch (error) {
      return null;
    }
  },
};

// 🎯 편의 함수들 - 자주 사용하는 기능들
export const getCurrentUser = (): UserIdentity | null => {
  try {
    const userInfo = localStorage.getItem('stein_user_info');
    return userInfo ? JSON.parse(userInfo) : null;
  } catch {
    return null;
  }
};

export const getAccessToken = (): string | null => {
  return localStorage.getItem('stein_access_token');
};

export const isAuthenticated = (): boolean => {
  return !!getAccessToken();
}; 