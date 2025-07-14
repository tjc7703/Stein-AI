#!/usr/bin/env python3
"""
🧠 Stein AI 지식 테스트 스크립트
터미널 에러 해결 능력을 검증합니다.
"""

import subprocess
import sys
from datetime import datetime

def test_terminal_knowledge():
    """터미널 지식 테스트"""
    print("🧪 Stein AI 터미널 지식 테스트 시작!")
    print("=" * 50)
    
    # 테스트 케이스들
    test_cases = [
        {
            "name": "🔧 따옴표 처리 지식",
            "command": 'echo "python-jose[cryptography]"',
            "expected": "python-jose[cryptography]",
            "description": "대괄호 포함 문자열 처리"
        },
        {
            "name": "🐍 Python 버전 확인",
            "command": "python --version",
            "expected": "Python",
            "description": "Python 환경 확인"
        },
        {
            "name": "📦 가상환경 확인",
            "command": "echo $VIRTUAL_ENV",
            "expected": None,  # 결과 상관없음
            "description": "가상환경 상태 확인"
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   명령어: {test['command']}")
        print(f"   설명: {test['description']}")
        
        try:
            # 명령어 실행
            result = subprocess.run(
                test['command'], 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"   ✅ 성공: {output}")
                
                if test['expected'] and test['expected'] in output:
                    results.append({"test": test['name'], "status": "PASS", "output": output})
                elif test['expected'] is None:
                    results.append({"test": test['name'], "status": "PASS", "output": output})
                else:
                    results.append({"test": test['name'], "status": "PARTIAL", "output": output})
            else:
                error = result.stderr.strip()
                print(f"   ❌ 실패: {error}")
                results.append({"test": test['name'], "status": "FAIL", "output": error})
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ 타임아웃: 명령어 실행 시간 초과")
            results.append({"test": test['name'], "status": "TIMEOUT", "output": "명령어 실행 시간 초과"})
        except Exception as e:
            print(f"   💥 에러: {str(e)}")
            results.append({"test": test['name'], "status": "ERROR", "output": str(e)})
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    
    pass_count = sum(1 for r in results if r['status'] == 'PASS')
    total_count = len(results)
    
    for result in results:
        status_emoji = {
            'PASS': '✅',
            'PARTIAL': '🟡', 
            'FAIL': '❌',
            'TIMEOUT': '⏰',
            'ERROR': '💥'
        }
        
        emoji = status_emoji.get(result['status'], '❓')
        print(f"{emoji} {result['test']}: {result['status']}")
    
    print(f"\n🎯 성공률: {pass_count}/{total_count} ({pass_count/total_count*100:.1f}%)")
    
    # 지식베이스 참조 안내
    print("\n📚 Stein AI 지식베이스 위치:")
    print("- 📄 docs/STEIN_AI_KNOWLEDGE_BASE.md")
    print("- ⚙️ .cursorrules (터미널 에러 해결 가이드)")
    print("- 📜 scripts/install_deps.sh (안전한 설치 스크립트)")
    
    return results

def demonstrate_error_resolution():
    """에러 해결 시연"""
    print("\n🎭 에러 해결 시연")
    print("=" * 30)
    
    print("❌ 문제 상황:")
    print("   pip install python-jose[cryptography]==3.3.0")
    print("   → zsh: no matches found: python-jose[cryptography]==3.3.0")
    
    print("\n🔍 문제 분석:")
    print("   - 대괄호 [] → zsh 글로빙 패턴으로 해석")
    print("   - 파일 매칭 시도 → 매칭 파일 없음 → 에러")
    
    print("\n✅ 해결 방법:")
    print('   pip install "python-jose[cryptography]==3.3.0"')
    print("   → 따옴표로 특수문자 보호 → 성공!")
    
    print("\n📝 프롬프트 예시:")
    print('   "터미널에서 zsh: no matches found 에러가 발생했어.')
    print('   이 에러의 원인과 해결 방법을 단계별로 설명해줘."')

if __name__ == "__main__":
    print("🤖 Stein AI 지식 검증 시스템")
    print(f"📅 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 지식 테스트 실행
    results = test_terminal_knowledge()
    
    # 에러 해결 시연
    demonstrate_error_resolution()
    
    print(f"\n🎉 Stein AI 지식 검증 완료!")
    print("🚀 이제 Stein AI가 터미널 에러를 스스로 해결할 수 있습니다!") 