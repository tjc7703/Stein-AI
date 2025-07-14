import ast
import re
import os
import subprocess
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import traceback

class QualityLevel(Enum):
    """코드 품질 수준"""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    CRITICAL = "critical"

class IssueType(Enum):
    """이슈 유형"""
    SYNTAX = "syntax"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    STYLE = "style"
    DOCUMENTATION = "documentation"

@dataclass
class QualityIssue:
    """품질 이슈"""
    issue_type: IssueType
    severity: str
    message: str
    file_path: str
    line_number: int
    suggestion: str
    auto_fixable: bool

@dataclass
class QualityMetrics:
    """품질 메트릭"""
    overall_score: float
    complexity_score: float
    maintainability_score: float
    performance_score: float
    security_score: float
    test_coverage: float
    documentation_score: float
    issues: List[QualityIssue]

class CodeQualityEngine:
    """🔧 고급 코드 품질 분석 및 개선 엔진"""
    
    def __init__(self):
        self.quality_history = []
        self.best_practices = self._load_best_practices()
        self.auto_fixes = {}
        
    def analyze_code_quality(self, file_path: str) -> QualityMetrics:
        """📊 코드 품질 종합 분석"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            issues = []
            
            # 1. 구문 분석 (Syntax Analysis)
            syntax_issues = self._analyze_syntax(code, file_path)
            issues.extend(syntax_issues)
            
            # 2. 복잡도 분석 (Complexity Analysis)
            complexity_issues = self._analyze_complexity(code, file_path)
            issues.extend(complexity_issues)
            
            # 3. 성능 분석 (Performance Analysis)
            performance_issues = self._analyze_performance(code, file_path)
            issues.extend(performance_issues)
            
            # 4. 보안 분석 (Security Analysis)
            security_issues = self._analyze_security(code, file_path)
            issues.extend(security_issues)
            
            # 5. 스타일 분석 (Style Analysis)
            style_issues = self._analyze_style(code, file_path)
            issues.extend(style_issues)
            
            # 6. 문서화 분석 (Documentation Analysis)
            doc_issues = self._analyze_documentation(code, file_path)
            issues.extend(doc_issues)
            
            # 점수 계산
            scores = self._calculate_quality_scores(code, issues)
            
            return QualityMetrics(
                overall_score=scores['overall'],
                complexity_score=scores['complexity'],
                maintainability_score=scores['maintainability'],
                performance_score=scores['performance'],
                security_score=scores['security'],
                test_coverage=scores['test_coverage'],
                documentation_score=scores['documentation'],
                issues=issues
            )
            
        except Exception as e:
            return QualityMetrics(
                overall_score=0.0,
                complexity_score=0.0,
                maintainability_score=0.0,
                performance_score=0.0,
                security_score=0.0,
                test_coverage=0.0,
                documentation_score=0.0,
                issues=[QualityIssue(
                    issue_type=IssueType.SYNTAX,
                    severity="high",
                    message=f"파일 분석 중 오류 발생: {str(e)}",
                    file_path=file_path,
                    line_number=1,
                    suggestion="파일 구문을 확인해주세요.",
                    auto_fixable=False
                )]
            )
    
    def _analyze_syntax(self, code: str, file_path: str) -> List[QualityIssue]:
        """구문 분석"""
        issues = []
        
        try:
            # AST 파싱으로 구문 오류 검사
            tree = ast.parse(code)
            
            # 일반적인 구문 문제 검사
            for node in ast.walk(tree):
                # 미사용 변수 검사
                if isinstance(node, ast.Name) and node.id.startswith('_'):
                    issues.append(QualityIssue(
                        issue_type=IssueType.STYLE,
                        severity="low",
                        message=f"미사용 변수 가능성: {node.id}",
                        file_path=file_path,
                        line_number=getattr(node, 'lineno', 1),
                        suggestion="미사용 변수는 제거하거나 의미있는 이름으로 변경하세요.",
                        auto_fixable=True
                    ))
                
                # 긴 함수 검사
                if isinstance(node, ast.FunctionDef):
                    if hasattr(node, 'body') and len(node.body) > 20:
                        issues.append(QualityIssue(
                            issue_type=IssueType.MAINTAINABILITY,
                            severity="medium",
                            message=f"함수 '{node.name}'이 너무 깁니다 ({len(node.body)} 라인)",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="함수를 더 작은 단위로 분리하세요.",
                            auto_fixable=False
                        ))
        
        except SyntaxError as e:
            issues.append(QualityIssue(
                issue_type=IssueType.SYNTAX,
                severity="high",
                message=f"구문 오류: {e.msg}",
                file_path=file_path,
                line_number=e.lineno or 1,
                suggestion="구문 오류를 수정하세요.",
                auto_fixable=False
            ))
        
        return issues
    
    def _analyze_complexity(self, code: str, file_path: str) -> List[QualityIssue]:
        """복잡도 분석"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_cyclomatic_complexity(node)
                    
                    if complexity > 10:
                        issues.append(QualityIssue(
                            issue_type=IssueType.MAINTAINABILITY,
                            severity="high" if complexity > 15 else "medium",
                            message=f"함수 '{node.name}'의 복잡도가 높습니다 (복잡도: {complexity})",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="함수를 더 작은 단위로 분리하거나 조건문을 단순화하세요.",
                            auto_fixable=False
                        ))
        
        except Exception as e:
            pass
        
        return issues
    
    def _analyze_performance(self, code: str, file_path: str) -> List[QualityIssue]:
        """성능 분석"""
        issues = []
        
        # 성능 안티패턴 검사
        performance_antipatterns = [
            (r'for.*in.*range\(len\(.*\)\)', "리스트 인덱스 대신 직접 순회를 사용하세요"),
            (r'\.append\(.*\)', "많은 append 호출 대신 list comprehension 사용을 고려하세요"),
            (r'import \*', "전체 모듈 import 대신 필요한 것만 import하세요"),
            (r'str\(.*\) \+', "문자열 연결 대신 f-string이나 join()을 사용하세요")
        ]
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, suggestion in performance_antipatterns:
                if re.search(pattern, line):
                    issues.append(QualityIssue(
                        issue_type=IssueType.PERFORMANCE,
                        severity="medium",
                        message=f"성능 개선 가능: {line.strip()}",
                        file_path=file_path,
                        line_number=i,
                        suggestion=suggestion,
                        auto_fixable=True
                    ))
        
        return issues
    
    def _analyze_security(self, code: str, file_path: str) -> List[QualityIssue]:
        """보안 분석"""
        issues = []
        
        # 보안 취약점 패턴
        security_patterns = [
            (r'eval\(', "eval() 사용은 보안 위험이 있습니다"),
            (r'exec\(', "exec() 사용은 보안 위험이 있습니다"),
            (r'os\.system\(', "os.system() 대신 subprocess 사용을 권장합니다"),
            (r'password.*=.*["\'].*["\']', "하드코딩된 비밀번호는 보안 위험입니다"),
            (r'api_key.*=.*["\'].*["\']', "하드코딩된 API 키는 보안 위험입니다")
        ]
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, message in security_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(QualityIssue(
                        issue_type=IssueType.SECURITY,
                        severity="high",
                        message=message,
                        file_path=file_path,
                        line_number=i,
                        suggestion="보안 모범 사례를 따르세요.",
                        auto_fixable=False
                    ))
        
        return issues
    
    def _analyze_style(self, code: str, file_path: str) -> List[QualityIssue]:
        """스타일 분석"""
        issues = []
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # 긴 줄 검사
            if len(line) > 100:
                issues.append(QualityIssue(
                    issue_type=IssueType.STYLE,
                    severity="low",
                    message=f"줄이 너무 깁니다 ({len(line)} 문자)",
                    file_path=file_path,
                    line_number=i,
                    suggestion="줄을 100자 이하로 줄이세요.",
                    auto_fixable=True
                ))
            
            # 불필요한 공백 검사
            if line.rstrip() != line:
                issues.append(QualityIssue(
                    issue_type=IssueType.STYLE,
                    severity="low",
                    message="줄 끝 공백이 있습니다",
                    file_path=file_path,
                    line_number=i,
                    suggestion="줄 끝 공백을 제거하세요.",
                    auto_fixable=True
                ))
        
        return issues
    
    def _analyze_documentation(self, code: str, file_path: str) -> List[QualityIssue]:
        """문서화 분석"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # docstring 확인
                    if not ast.get_docstring(node):
                        issues.append(QualityIssue(
                            issue_type=IssueType.DOCUMENTATION,
                            severity="medium",
                            message=f"함수 '{node.name}'에 docstring이 없습니다",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="함수에 docstring을 추가하세요.",
                            auto_fixable=True
                        ))
                    
                    # 타입 힌트 확인
                    if not node.returns:
                        issues.append(QualityIssue(
                            issue_type=IssueType.DOCUMENTATION,
                            severity="low",
                            message=f"함수 '{node.name}'에 반환 타입 힌트가 없습니다",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="반환 타입 힌트를 추가하세요.",
                            auto_fixable=True
                        ))
        
        except Exception as e:
            pass
        
        return issues
    
    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """순환 복잡도 계산"""
        complexity = 1  # 기본 복잡도
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_quality_scores(self, code: str, issues: List[QualityIssue]) -> Dict[str, float]:
        """품질 점수 계산"""
        
        # 기본 점수 (100점 만점)
        scores = {
            'overall': 100.0,
            'complexity': 100.0,
            'maintainability': 100.0,
            'performance': 100.0,
            'security': 100.0,
            'test_coverage': 80.0,  # 기본 값
            'documentation': 100.0
        }
        
        # 이슈별 점수 차감
        for issue in issues:
            deduction = {
                'high': 10.0,
                'medium': 5.0,
                'low': 2.0
            }.get(issue.severity, 1.0)
            
            scores['overall'] -= deduction
            
            # 특정 카테고리 점수 차감
            if issue.issue_type == IssueType.PERFORMANCE:
                scores['performance'] -= deduction * 2
            elif issue.issue_type == IssueType.SECURITY:
                scores['security'] -= deduction * 3
            elif issue.issue_type == IssueType.MAINTAINABILITY:
                scores['maintainability'] -= deduction * 2
            elif issue.issue_type == IssueType.DOCUMENTATION:
                scores['documentation'] -= deduction
        
        # 0점 이하로 내려가지 않도록 조정
        for key in scores:
            scores[key] = max(0.0, scores[key])
        
        return scores
    
    def apply_auto_fixes(self, file_path: str, issues: List[QualityIssue]) -> Dict[str, Any]:
        """자동 수정 적용"""
        
        fixes_applied = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            modified_code = original_code
            
            for issue in issues:
                if issue.auto_fixable:
                    fixed_code = self._apply_single_fix(modified_code, issue)
                    if fixed_code != modified_code:
                        modified_code = fixed_code
                        fixes_applied.append(issue.message)
            
            # 수정된 코드 저장
            if modified_code != original_code:
                backup_path = f"{file_path}.backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_code)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_code)
            
            return {
                'success': True,
                'fixes_applied': fixes_applied,
                'backup_created': modified_code != original_code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fixes_applied': []
            }
    
    def _apply_single_fix(self, code: str, issue: QualityIssue) -> str:
        """개별 수정 적용"""
        
        lines = code.split('\n')
        
        if issue.line_number <= len(lines):
            line = lines[issue.line_number - 1]
            
            # 간단한 수정 적용
            if "줄 끝 공백" in issue.message:
                lines[issue.line_number - 1] = line.rstrip()
            
            elif "f-string" in issue.suggestion:
                # 간단한 문자열 연결을 f-string으로 변환
                # 복잡한 패턴 매칭이 필요하므로 여기서는 주석만 추가
                lines[issue.line_number - 1] = f"# TODO: f-string 변환 고려 - {line}"
            
            elif "docstring" in issue.message:
                # 함수 다음 줄에 기본 docstring 추가
                if issue.line_number < len(lines):
                    indent = len(line) - len(line.lstrip())
                    docstring = ' ' * (indent + 4) + '"""TODO: 함수 설명 추가"""'
                    lines.insert(issue.line_number, docstring)
        
        return '\n'.join(lines)
    
    def generate_quality_report(self, metrics: QualityMetrics) -> str:
        """품질 보고서 생성"""
        
        report = f"""
🔧 코드 품질 분석 보고서
=====================================

📊 전체 품질 점수: {metrics.overall_score:.1f}/100

📈 세부 점수:
- 복잡도: {metrics.complexity_score:.1f}/100
- 유지보수성: {metrics.maintainability_score:.1f}/100
- 성능: {metrics.performance_score:.1f}/100
- 보안: {metrics.security_score:.1f}/100
- 테스트 커버리지: {metrics.test_coverage:.1f}/100
- 문서화: {metrics.documentation_score:.1f}/100

🔍 발견된 이슈 ({len(metrics.issues)}개):
"""
        
        # 이슈를 심각도별로 분류
        high_issues = [i for i in metrics.issues if i.severity == "high"]
        medium_issues = [i for i in metrics.issues if i.severity == "medium"]
        low_issues = [i for i in metrics.issues if i.severity == "low"]
        
        if high_issues:
            report += f"\n🔴 심각한 이슈 ({len(high_issues)}개):\n"
            for issue in high_issues[:5]:  # 최대 5개만 표시
                report += f"  - {issue.message} (라인 {issue.line_number})\n"
        
        if medium_issues:
            report += f"\n🟡 중간 이슈 ({len(medium_issues)}개):\n"
            for issue in medium_issues[:5]:
                report += f"  - {issue.message} (라인 {issue.line_number})\n"
        
        if low_issues:
            report += f"\n🟢 낮은 이슈 ({len(low_issues)}개):\n"
            for issue in low_issues[:3]:
                report += f"  - {issue.message} (라인 {issue.line_number})\n"
        
        # 개선 제안
        report += f"\n💡 개선 제안:\n"
        report += self._generate_improvement_suggestions(metrics)
        
        return report
    
    def _generate_improvement_suggestions(self, metrics: QualityMetrics) -> str:
        """개선 제안 생성"""
        suggestions = []
        
        if metrics.complexity_score < 70:
            suggestions.append("- 복잡한 함수들을 더 작은 단위로 분리하세요")
        
        if metrics.performance_score < 80:
            suggestions.append("- 성능 최적화를 위해 알고리즘을 개선하세요")
        
        if metrics.security_score < 90:
            suggestions.append("- 보안 취약점을 즉시 수정하세요")
        
        if metrics.documentation_score < 70:
            suggestions.append("- 함수와 클래스에 docstring을 추가하세요")
        
        if metrics.test_coverage < 80:
            suggestions.append("- 테스트 커버리지를 80% 이상으로 높이세요")
        
        if not suggestions:
            suggestions.append("- 현재 코드 품질이 우수합니다! 계속 유지하세요")
        
        return '\n'.join(suggestions)
    
    def _load_best_practices(self) -> Dict[str, Any]:
        """베스트 프랙티스 로드"""
        return {
            'python': {
                'max_function_length': 20,
                'max_line_length': 88,
                'max_complexity': 10,
                'require_docstrings': True,
                'require_type_hints': True
            },
            'javascript': {
                'max_function_length': 15,
                'max_line_length': 80,
                'max_complexity': 8,
                'require_jsdoc': True
            }
        }
    
    def get_quality_trends(self) -> Dict[str, Any]:
        """품질 트렌드 분석"""
        if not self.quality_history:
            return {}
        
        recent_scores = [h['overall_score'] for h in self.quality_history[-10:]]
        
        return {
            'current_score': recent_scores[-1] if recent_scores else 0,
            'average_score': sum(recent_scores) / len(recent_scores) if recent_scores else 0,
            'trend': 'improving' if len(recent_scores) > 1 and recent_scores[-1] > recent_scores[0] else 'stable',
            'total_analyses': len(self.quality_history)
        } 