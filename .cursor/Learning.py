def hello():
    print("안녕하세요! 반갑습니다.")

hello()

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

# 새로운 계산기 함수들 추가
def divide(a, b):
    """나누기 함수 - 0으로 나누기 에러 처리 포함"""
    if b == 0:
        return "❌ 에러: 0으로 나눌 수 없습니다!"
    return a / b

def power(a, b):
    """제곱 함수"""
    return a ** b

def modulo(a, b):
    """나머지 함수"""
    if b == 0:
        return "❌ 에러: 0으로 나눌 수 없습니다!"
    return a % b

def square_root(a):
    """제곱근 함수"""
    if a < 0:
        return "❌ 에러: 음수의 제곱근은 계산할 수 없습니다!"
    return a ** 0.5

def factorial(n):
    """팩토리얼 함수"""
    if n < 0:
        return "❌ 에러: 음수의 팩토리얼은 계산할 수 없습니다!"
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# 함수들 테스트해보기
print("\n🧮 계산기 함수 테스트:")
print(f"10 + 5 = {add(10, 5)}")
print(f"10 - 5 = {subtract(10, 5)}")
print(f"10 × 5 = {multiply(10, 5)}")
print(f"10 ÷ 5 = {divide(10, 5)}")
print(f"10 ÷ 0 = {divide(10, 0)}")  # 에러 처리 테스트
print(f"2³ = {power(2, 3)}")
print(f"10 % 3 = {modulo(10, 3)}")
print(f"√16 = {square_root(16)}")
print(f"5! = {factorial(5)}")