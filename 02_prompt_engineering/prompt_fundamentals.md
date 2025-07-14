# 🎨 프롬프트 엔지니어링 마스터 가이드

## 📋 프롬프트 엔지니어링이란?

프롬프트 엔지니어링은 AI 모델로부터 원하는 결과를 얻기 위해 입력 텍스트(프롬프트)를 체계적으로 설계하고 최적화하는 기술입니다. Stein AI 개발에서 가장 핵심적인 스킬입니다.

## 🎯 프롬프트의 핵심 구조

### 1. 기본 구조 (CARE Framework)
```
Context (맥락): 상황과 배경 정보 제공
Action (행동): 구체적인 작업 요청
Result (결과): 원하는 출력 형태 명시
Example (예시): 참고할 만한 예시 제공
```

### 2. 효과적인 프롬프트 구성 요소
```
# 완전한 프롬프트 구조
[역할 설정] + [컨텍스트] + [명확한 지시] + [출력 형식] + [제약사항] + [예시]
```

## 💡 프롬프트 작성 기본 원칙

### 1. 명확성 (Clarity)
```
❌ 나쁜 예: "코드 만들어줘"
✅ 좋은 예: "React TypeScript 환경에서 사용자 인증을 위한 로그인 컴포넌트를 만들어줘. 
useState와 useForm 훅을 사용하고, 이메일/비밀번호 유효성 검사를 포함해줘."
```

### 2. 구체성 (Specificity)
```
❌ 나쁜 예: "API 만들어줘"
✅ 좋은 예: "Express.js로 RESTful API를 만들어줘. 
- 엔드포인트: GET /users, POST /users, PUT /users/:id, DELETE /users/:id
- MongoDB 연동
- JWT 인증 미들웨어 적용
- 입력 데이터 유효성 검사 포함"
```

### 3. 맥락 제공 (Context)
```
❌ 나쁜 예: "버그 고쳐줘"
✅ 좋은 예: "Next.js 프로젝트에서 동적 라우팅이 작동하지 않는 문제가 있어. 
pages/[slug].js 파일에서 getServerSideProps를 사용하고 있고, 
현재 에러 메시지는 '404 - This page could not be found'야. 
슬러그 값이 제대로 전달되지 않는 것 같아."
```

## 🚀 고급 프롬프트 기법

### 1. Chain of Thought (CoT) 프롬프팅
```
# 복잡한 문제를 단계별로 해결
"다음 요구사항을 단계별로 분석해서 구현해줘:

1단계: 요구사항 분석
- 사용자 스토리 파악
- 기술적 제약사항 확인
- 데이터 플로우 설계

2단계: 아키텍처 설계
- 컴포넌트 구조 정의
- 상태 관리 방식 결정
- API 설계

3단계: 구현
- 핵심 로직 구현
- UI 컴포넌트 개발
- 테스트 코드 작성

각 단계별로 상세한 설명과 함께 코드를 작성해줘."
```

### 2. Role Playing 기법
```
# AI에게 특정 역할 부여
"당신은 10년 경력의 시니어 풀스택 개발자입니다. 
주니어 개발자가 React 성능 최적화에 대해 질문했을 때처럼 
자세하고 이해하기 쉽게 설명해주세요.

질문: 리스트 렌더링 성능을 어떻게 최적화할 수 있나요?"
```

### 3. Few-Shot Learning 기법
```
# 여러 예시를 통한 패턴 학습
"다음 예시들을 참고해서 비슷한 함수를 만들어줘:

예시 1:
// 사용자 생성
const createUser = async (userData) => {
  try {
    const user = await User.create(userData);
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

예시 2:
// 사용자 조회
const getUser = async (userId) => {
  try {
    const user = await User.findById(userId);
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

이제 상품(Product) 관련 CRUD 함수들을 같은 패턴으로 만들어줘."
```

## 🎯 Stein AI를 위한 특화 프롬프트

### 1. 개인화 학습 프롬프트
```
"Stein AI는 사용자의 코딩 스타일과 선호도를 학습해야 해. 
다음 코드 스타일 패턴을 분석해서 일관성 있는 코드를 생성하는 
개인화 알고리즘을 설계해줘:

사용자 코딩 패턴:
- 함수형 프로그래밍 선호
- 명시적 타입 정의
- 상세한 주석 작성
- 단위 테스트 필수

이 패턴을 학습하고 적용하는 시스템을 만들어줘."
```

### 2. 점진적 학습 프롬프트
```
"Stein AI가 사용자와의 상호작용을 통해 점진적으로 학습하도록 
피드백 루프 시스템을 구현해줘:

1. 사용자 요청 분석
2. 코드 생성 및 제안
3. 사용자 피드백 수집
4. 개선사항 학습 및 적용
5. 다음 요청에서 학습된 내용 반영

이 순환 구조를 코드로 구현해줘."
```

## 🔧 프롬프트 최적화 기법

### 1. A/B 테스팅으로 프롬프트 개선
```python
# 프롬프트 성능 비교
prompts = {
    "version_a": "코드를 리팩토링해줘",
    "version_b": "다음 관점에서 코드를 개선해줘: 가독성, 성능, 유지보수성",
    "version_c": "레거시 코드를 현대적 패턴으로 리팩토링해줘. 성능 최적화와 타입 안정성을 고려해서"
}

# 각 버전의 결과 품질 측정 및 비교
```

### 2. 템플릿 기반 프롬프트 관리
```javascript
// 프롬프트 템플릿 라이브러리
const promptTemplates = {
  codeGeneration: {
    react: `
      React ${technology} 컴포넌트를 생성해줘:
      - 컴포넌트명: ${componentName}
      - 기능: ${functionality}
      - 스타일링: ${styling}
      - 상태관리: ${stateManagement}
      - 테스트: ${testRequired ? '포함' : '제외'}
    `,
    api: `
      ${framework} API 엔드포인트를 생성해줘:
      - 메소드: ${method}
      - 경로: ${path}
      - 기능: ${functionality}
      - 인증: ${authRequired ? '필요' : '불필요'}
      - 데이터베이스: ${database}
    `
  },
  debugging: `
    다음 에러를 분석하고 해결방법을 제시해줘:
    - 에러 메시지: ${errorMessage}
    - 발생 위치: ${location}
    - 관련 코드: ${codeSnippet}
    - 환경: ${environment}
  `,
  optimization: `
    다음 관점에서 코드를 최적화해줘:
    - 성능: ${performanceAspects}
    - 메모리: ${memoryOptimization}
    - 가독성: ${readabilityImprovement}
    - 보안: ${securityConsiderations}
  `
};
```

## 📊 프롬프트 품질 평가 기준

### 1. 정량적 평가 지표
```
- 응답 정확도: 요구사항 충족 비율
- 코드 실행 성공률: 생성된 코드의 오류 없는 실행 비율
- 응답 시간: 프롬프트 처리 속도
- 일관성: 비슷한 요청에 대한 일관된 품질의 응답
```

### 2. 정성적 평가 기준
```
- 창의성: 혁신적이고 효율적인 솔루션 제안
- 설명력: 코드와 함께 제공되는 설명의 명확성
- 맥락 이해: 프로젝트 전체 맥락에서의 적절성
- 베스트 프랙티스: 업계 표준 및 모범 사례 준수
```

## 🎪 실전 프롬프트 워크샵

### 1. 코드 생성 프롬프트 실습
```
과제: "사용자 대시보드 컴포넌트 생성"

기본 프롬프트:
"대시보드 만들어줘"

개선된 프롬프트:
"React TypeScript로 관리자 대시보드 컴포넌트를 만들어줘.
요구사항:
- 사용자 통계 카드 (총 사용자, 활성 사용자, 신규 가입)
- 월별 가입자 추이 차트 (Chart.js 사용)
- 최근 활동 목록 테이블
- 반응형 디자인 (Tailwind CSS)
- 데이터는 props로 받아오기
- TypeScript 인터페이스 정의 포함
- 로딩 및 에러 상태 처리"
```

### 2. 디버깅 프롬프트 실습
```
과제: "API 호출 오류 해결"

기본 프롬프트:
"API 에러 고쳐줘"

개선된 프롬프트:
"Next.js API 라우트에서 발생하는 CORS 에러를 해결해줘.

현재 상황:
- API: /api/users/[id].js
- 프론트엔드: React (포트 3000)
- 백엔드: Next.js API (포트 3000)
- 에러: 'Access-Control-Allow-Origin' header is missing

현재 코드:
[코드 스니펫 첨부]

목표:
- CORS 설정으로 문제 해결
- 보안 고려사항 포함
- 개발/프로덕션 환경 분리"
```

## ✅ 프롬프트 엔지니어링 마스터 체크리스트

- [ ] CARE 프레임워크로 구조화된 프롬프트 작성 가능
- [ ] Chain of Thought로 복잡한 문제 해결 가능
- [ ] Role Playing 기법으로 특화된 답변 유도 가능
- [ ] Few-Shot Learning으로 패턴 학습 활용 가능
- [ ] 템플릿 기반 프롬프트 관리 시스템 구축
- [ ] A/B 테스팅으로 프롬프트 성능 최적화
- [ ] Stein AI 특화 개인화 프롬프트 설계
- [ ] 프롬프트 품질 평가 및 지속적 개선

> **다음 단계**: 이제 알고리즘 설계로 Stein AI의 두뇌를 만들어보세요! 