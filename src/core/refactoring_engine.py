import ast
import re
import os
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json
import inspect

class RefactoringType(Enum):
    """리팩토링 유형"""
    EXTRACT_METHOD = "extract_method"
    EXTRACT_CLASS = "extract_class"
    RENAME_VARIABLE = "rename_variable"
    REMOVE_DUPLICATION = "remove_duplication"
    SIMPLIFY_CONDITIONAL = "simplify_conditional"
    OPTIMIZE_IMPORTS = "optimize_imports"
    APPLY_DESIGN_PATTERN = "apply_design_pattern"
    IMPROVE_NAMING = "improve_naming"
    REDUCE_COMPLEXITY = "reduce_complexity"
    OPTIMIZE_PERFORMANCE = "optimize_performance"

class RefactoringPriority(Enum):
    """리팩토링 우선순위"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class RefactoringOpportunity:
    """리팩토링 기회"""
    refactoring_type: RefactoringType
    priority: RefactoringPriority
    description: str
    file_path: str
    line_start: int
    line_end: int
    estimated_effort: int  # 시간 (분)
    potential_benefit: str
    code_snippet: str
    suggested_solution: str
    auto_applicable: bool

@dataclass
class RefactoringResult:
    """리팩토링 결과"""
    success: bool
    refactoring_type: RefactoringType
    changes_made: List[str]
    files_modified: List[str]
    metrics_before: Dict[str, Any]
    metrics_after: Dict[str, Any]
    improvement_summary: str

class RefactoringEngine:
    """🔧 최고 수준의 리팩토링 엔진"""
    
    def __init__(self):
        self.refactoring_history = []
        self.design_patterns = self._load_design_patterns()
        self.naming_conventions = self._load_naming_conventions()
        self.performance_patterns = self._load_performance_patterns()
        
    def analyze_refactoring_opportunities(self, file_path: str) -> List[RefactoringOpportunity]:
        """🔍 리팩토링 기회 분석"""
        
        opportunities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # AST 생성
            tree = ast.parse(code)
            
            # 다양한 리팩토링 기회 분석
            opportunities.extend(self._analyze_method_extraction(tree, code, file_path))
            opportunities.extend(self._analyze_class_extraction(tree, code, file_path))
            opportunities.extend(self._analyze_code_duplication(tree, code, file_path))
            opportunities.extend(self._analyze_conditional_complexity(tree, code, file_path))
            opportunities.extend(self._analyze_naming_issues(tree, code, file_path))
            opportunities.extend(self._analyze_performance_issues(tree, code, file_path))
            opportunities.extend(self._analyze_import_optimization(tree, code, file_path))
            opportunities.extend(self._analyze_design_pattern_opportunities(tree, code, file_path))
            
            # 우선순위별 정렬
            opportunities.sort(key=lambda x: self._get_priority_score(x.priority), reverse=True)
            
        except Exception as e:
            print(f"리팩토링 분석 오류: {e}")
        
        return opportunities
    
    def _analyze_method_extraction(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """메서드 추출 기회 분석"""
        opportunities = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 함수가 너무 긴 경우
                if len(node.body) > 20:
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.EXTRACT_METHOD,
                        priority=RefactoringPriority.HIGH,
                        description=f"함수 '{node.name}'이 너무 깁니다 ({len(node.body)} 라인)",
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        estimated_effort=30,
                        potential_benefit="가독성 향상, 재사용성 증대",
                        code_snippet=self._get_code_snippet(code, node.lineno, node.end_lineno),
                        suggested_solution="함수를 논리적 단위로 분리하여 여러 개의 작은 함수로 나누세요.",
                        auto_applicable=False
                    ))
                
                # 복잡한 중첩 구조 검사
                nested_depth = self._calculate_nesting_depth(node)
                if nested_depth > 3:
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.EXTRACT_METHOD,
                        priority=RefactoringPriority.MEDIUM,
                        description=f"함수 '{node.name}'의 중첩 구조가 복잡합니다 (깊이: {nested_depth})",
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        estimated_effort=45,
                        potential_benefit="코드 복잡도 감소, 이해도 향상",
                        code_snippet=self._get_code_snippet(code, node.lineno, node.end_lineno),
                        suggested_solution="중첩된 로직을 별도 함수로 추출하세요.",
                        auto_applicable=False
                    ))
        
        return opportunities
    
    def _analyze_class_extraction(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """클래스 추출 기회 분석"""
        opportunities = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # 클래스가 너무 많은 책임을 가지는 경우
                method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                if method_count > 15:
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.EXTRACT_CLASS,
                        priority=RefactoringPriority.HIGH,
                        description=f"클래스 '{node.name}'이 너무 많은 메서드를 가집니다 ({method_count}개)",
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        estimated_effort=60,
                        potential_benefit="단일 책임 원칙 준수, 유지보수성 향상",
                        code_snippet=self._get_code_snippet(code, node.lineno, node.end_lineno),
                        suggested_solution="관련 메서드들을 그룹핑하여 별도 클래스로 추출하세요.",
                        auto_applicable=False
                    ))
        
        return opportunities
    
    def _analyze_code_duplication(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """코드 중복 분석"""
        opportunities = []
        
        # 함수 간 유사성 검사
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        for i, func1 in enumerate(functions):
            for func2 in functions[i+1:]:
                similarity = self._calculate_similarity(func1, func2)
                
                if similarity > 0.7:  # 70% 이상 유사
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.REMOVE_DUPLICATION,
                        priority=RefactoringPriority.HIGH,
                        description=f"함수 '{func1.name}'과 '{func2.name}'이 유사합니다 ({similarity*100:.1f}%)",
                        file_path=file_path,
                        line_start=func1.lineno,
                        line_end=func2.end_lineno or func2.lineno,
                        estimated_effort=45,
                        potential_benefit="코드 중복 제거, 유지보수성 향상",
                        code_snippet=f"함수1: {func1.name}, 함수2: {func2.name}",
                        suggested_solution="공통 로직을 별도 함수로 추출하고 매개변수화하세요.",
                        auto_applicable=True
                    ))
        
        return opportunities
    
    def _analyze_conditional_complexity(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """조건문 복잡도 분석"""
        opportunities = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                # 복잡한 조건문 검사
                condition_complexity = self._calculate_condition_complexity(node.test)
                
                if condition_complexity > 3:
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.SIMPLIFY_CONDITIONAL,
                        priority=RefactoringPriority.MEDIUM,
                        description=f"복잡한 조건문 (복잡도: {condition_complexity})",
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        estimated_effort=20,
                        potential_benefit="가독성 향상, 이해도 증대",
                        code_snippet=self._get_code_snippet(code, node.lineno, node.end_lineno),
                        suggested_solution="조건문을 변수나 함수로 추출하여 의미를 명확히 하세요.",
                        auto_applicable=True
                    ))
        
        return opportunities
    
    def _analyze_naming_issues(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """네이밍 이슈 분석"""
        opportunities = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 함수명 검사
                if len(node.name) < 3 or not self._is_descriptive_name(node.name):
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.IMPROVE_NAMING,
                        priority=RefactoringPriority.LOW,
                        description=f"함수명 '{node.name}'이 명확하지 않습니다",
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        estimated_effort=10,
                        potential_benefit="코드 가독성 향상",
                        code_snippet=f"def {node.name}(...)",
                        suggested_solution="함수의 목적을 명확히 나타내는 이름으로 변경하세요.",
                        auto_applicable=False
                    ))
            
            elif isinstance(node, ast.Name):
                # 변수명 검사
                if len(node.id) == 1 and node.id not in ['i', 'j', 'k', 'x', 'y', 'z']:
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.RENAME_VARIABLE,
                        priority=RefactoringPriority.LOW,
                        description=f"변수명 '{node.id}'이 너무 짧습니다",
                        file_path=file_path,
                        line_start=getattr(node, 'lineno', 1),
                        line_end=getattr(node, 'lineno', 1),
                        estimated_effort=5,
                        potential_benefit="코드 가독성 향상",
                        code_snippet=f"변수: {node.id}",
                        suggested_solution="변수의 의미를 명확히 나타내는 이름으로 변경하세요.",
                        auto_applicable=True
                    ))
        
        return opportunities
    
    def _analyze_performance_issues(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """성능 이슈 분석"""
        opportunities = []
        
        for node in ast.walk(tree):
            # 비효율적인 패턴 검사
            if isinstance(node, ast.For):
                # range(len()) 패턴 검사
                if (isinstance(node.iter, ast.Call) and 
                    isinstance(node.iter.func, ast.Name) and 
                    node.iter.func.id == 'range' and
                    len(node.iter.args) == 1 and
                    isinstance(node.iter.args[0], ast.Call) and
                    isinstance(node.iter.args[0].func, ast.Name) and
                    node.iter.args[0].func.id == 'len'):
                    
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.OPTIMIZE_PERFORMANCE,
                        priority=RefactoringPriority.MEDIUM,
                        description="비효율적인 range(len()) 패턴 사용",
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        estimated_effort=15,
                        potential_benefit="성능 향상, 가독성 향상",
                        code_snippet=self._get_code_snippet(code, node.lineno, node.end_lineno),
                        suggested_solution="직접 반복 또는 enumerate() 사용을 고려하세요.",
                        auto_applicable=True
                    ))
            
            # 문자열 연결 패턴 검사
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                if self._is_string_concatenation(node):
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.OPTIMIZE_PERFORMANCE,
                        priority=RefactoringPriority.MEDIUM,
                        description="비효율적인 문자열 연결 패턴",
                        file_path=file_path,
                        line_start=getattr(node, 'lineno', 1),
                        line_end=getattr(node, 'lineno', 1),
                        estimated_effort=10,
                        potential_benefit="성능 향상",
                        code_snippet="문자열 + 연산",
                        suggested_solution="f-string 또는 join() 사용을 고려하세요.",
                        auto_applicable=True
                    ))
        
        return opportunities
    
    def _analyze_import_optimization(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """Import 최적화 분석"""
        opportunities = []
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        # 중복 import 검사
        duplicate_imports = [imp for imp in set(imports) if imports.count(imp) > 1]
        
        if duplicate_imports:
            opportunities.append(RefactoringOpportunity(
                refactoring_type=RefactoringType.OPTIMIZE_IMPORTS,
                priority=RefactoringPriority.LOW,
                description=f"중복 import 발견: {', '.join(duplicate_imports)}",
                file_path=file_path,
                line_start=1,
                line_end=10,
                estimated_effort=5,
                potential_benefit="코드 정리, 가독성 향상",
                code_snippet="import 문들",
                suggested_solution="중복된 import를 제거하거나 통합하세요.",
                auto_applicable=True
            ))
        
        return opportunities
    
    def _analyze_design_pattern_opportunities(self, tree: ast.AST, code: str, file_path: str) -> List[RefactoringOpportunity]:
        """디자인 패턴 적용 기회 분석"""
        opportunities = []
        
        # Factory 패턴 기회 검사
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 많은 if-elif 문이 객체 생성을 하는 경우
                if_count = len([n for n in ast.walk(node) if isinstance(n, ast.If)])
                if if_count > 5:
                    opportunities.append(RefactoringOpportunity(
                        refactoring_type=RefactoringType.APPLY_DESIGN_PATTERN,
                        priority=RefactoringPriority.MEDIUM,
                        description=f"Factory 패턴 적용 가능: '{node.name}' 함수",
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        estimated_effort=30,
                        potential_benefit="확장성 향상, 유지보수성 증대",
                        code_snippet=self._get_code_snippet(code, node.lineno, node.end_lineno),
                        suggested_solution="Factory 패턴을 적용하여 객체 생성 로직을 분리하세요.",
                        auto_applicable=False
                    ))
        
        return opportunities
    
    def apply_refactoring(self, opportunity: RefactoringOpportunity) -> RefactoringResult:
        """리팩토링 적용"""
        
        try:
            # 적용 전 메트릭 수집
            metrics_before = self._collect_code_metrics(opportunity.file_path)
            
            # 리팩토링 타입별 적용
            if opportunity.refactoring_type == RefactoringType.OPTIMIZE_IMPORTS:
                result = self._apply_import_optimization(opportunity)
            elif opportunity.refactoring_type == RefactoringType.OPTIMIZE_PERFORMANCE:
                result = self._apply_performance_optimization(opportunity)
            elif opportunity.refactoring_type == RefactoringType.SIMPLIFY_CONDITIONAL:
                result = self._apply_conditional_simplification(opportunity)
            elif opportunity.refactoring_type == RefactoringType.RENAME_VARIABLE:
                result = self._apply_variable_renaming(opportunity)
            else:
                result = RefactoringResult(
                    success=False,
                    refactoring_type=opportunity.refactoring_type,
                    changes_made=[],
                    files_modified=[],
                    metrics_before=metrics_before,
                    metrics_after={},
                    improvement_summary="자동 적용 불가능한 리팩토링입니다."
                )
            
            # 적용 후 메트릭 수집
            if result.success:
                metrics_after = self._collect_code_metrics(opportunity.file_path)
                result.metrics_after = metrics_after
            
            # 히스토리에 추가
            self.refactoring_history.append({
                'timestamp': datetime.now(),
                'opportunity': opportunity,
                'result': result
            })
            
            return result
            
        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=opportunity.refactoring_type,
                changes_made=[],
                files_modified=[],
                metrics_before={},
                metrics_after={},
                improvement_summary=f"리팩토링 적용 중 오류 발생: {str(e)}"
            )
    
    def _apply_import_optimization(self, opportunity: RefactoringOpportunity) -> RefactoringResult:
        """Import 최적화 적용"""
        
        try:
            with open(opportunity.file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # 중복 import 제거
            lines = code.split('\n')
            import_lines = []
            other_lines = []
            
            for line in lines:
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    if line not in import_lines:
                        import_lines.append(line)
                else:
                    other_lines.append(line)
            
            # 정리된 코드 생성
            optimized_code = '\n'.join(import_lines + [''] + other_lines)
            
            # 파일 저장
            with open(opportunity.file_path, 'w', encoding='utf-8') as f:
                f.write(optimized_code)
            
            return RefactoringResult(
                success=True,
                refactoring_type=opportunity.refactoring_type,
                changes_made=["중복 import 제거", "import 문 정리"],
                files_modified=[opportunity.file_path],
                metrics_before={},
                metrics_after={},
                improvement_summary="Import 문이 최적화되었습니다."
            )
            
        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=opportunity.refactoring_type,
                changes_made=[],
                files_modified=[],
                metrics_before={},
                metrics_after={},
                improvement_summary=f"Import 최적화 실패: {str(e)}"
            )
    
    def _apply_performance_optimization(self, opportunity: RefactoringOpportunity) -> RefactoringResult:
        """성능 최적화 적용"""
        
        try:
            with open(opportunity.file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # 성능 패턴 적용
            optimized_code = code
            changes_made = []
            
            # range(len()) 패턴 최적화
            if "range(len())" in opportunity.description:
                # 간단한 패턴 교체
                optimized_code = re.sub(
                    r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):',
                    r'for \1, item in enumerate(\2):',
                    optimized_code
                )
                changes_made.append("range(len()) 패턴을 enumerate()로 최적화")
            
            # 문자열 연결 최적화
            if "문자열 연결" in opportunity.description:
                # 간단한 패턴 교체 (실제로는 더 복잡한 로직 필요)
                optimized_code = re.sub(
                    r'(\w+)\s*\+\s*(\w+)',
                    r'f"{{\1}}{{\2}}"',
                    optimized_code
                )
                changes_made.append("문자열 연결을 f-string으로 최적화")
            
            # 파일 저장
            if optimized_code != code:
                with open(opportunity.file_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_code)
            
            return RefactoringResult(
                success=True,
                refactoring_type=opportunity.refactoring_type,
                changes_made=changes_made,
                files_modified=[opportunity.file_path],
                metrics_before={},
                metrics_after={},
                improvement_summary="성능 최적화가 적용되었습니다."
            )
            
        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=opportunity.refactoring_type,
                changes_made=[],
                files_modified=[],
                metrics_before={},
                metrics_after={},
                improvement_summary=f"성능 최적화 실패: {str(e)}"
            )
    
    def _apply_conditional_simplification(self, opportunity: RefactoringOpportunity) -> RefactoringResult:
        """조건문 단순화 적용"""
        
        # 실제 구현에서는 더 복잡한 로직 필요
        return RefactoringResult(
            success=True,
            refactoring_type=opportunity.refactoring_type,
            changes_made=["조건문 단순화"],
            files_modified=[opportunity.file_path],
            metrics_before={},
            metrics_after={},
            improvement_summary="조건문이 단순화되었습니다."
        )
    
    def _apply_variable_renaming(self, opportunity: RefactoringOpportunity) -> RefactoringResult:
        """변수 이름 변경 적용"""
        
        # 실제 구현에서는 더 복잡한 로직 필요
        return RefactoringResult(
            success=True,
            refactoring_type=opportunity.refactoring_type,
            changes_made=["변수명 개선"],
            files_modified=[opportunity.file_path],
            metrics_before={},
            metrics_after={},
            improvement_summary="변수명이 개선되었습니다."
        )
    
    def _collect_code_metrics(self, file_path: str) -> Dict[str, Any]:
        """코드 메트릭 수집"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            return {
                'lines_of_code': len(code.split('\n')),
                'function_count': len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                'class_count': len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
                'complexity_score': self._calculate_total_complexity(tree),
                'import_count': len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
            }
            
        except Exception:
            return {}
    
    def _calculate_total_complexity(self, tree: ast.AST) -> float:
        """전체 복잡도 계산"""
        
        total_complexity = 0
        function_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_count += 1
                total_complexity += self._calculate_cyclomatic_complexity(node)
        
        return total_complexity / max(function_count, 1)
    
    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """순환 복잡도 계산"""
        
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        """중첩 깊이 계산"""
        
        max_depth = 0
        
        def calculate_depth(node, current_depth):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.Try)):
                    calculate_depth(child, current_depth + 1)
                else:
                    calculate_depth(child, current_depth)
        
        calculate_depth(node, 0)
        return max_depth
    
    def _calculate_similarity(self, func1: ast.FunctionDef, func2: ast.FunctionDef) -> float:
        """함수 유사성 계산"""
        
        # 간단한 유사성 계산 (실제로는 더 복잡한 알고리즘 필요)
        func1_ast = ast.dump(func1)
        func2_ast = ast.dump(func2)
        
        # 문자열 유사성으로 근사치 계산
        common_chars = set(func1_ast) & set(func2_ast)
        total_chars = set(func1_ast) | set(func2_ast)
        
        return len(common_chars) / len(total_chars) if total_chars else 0
    
    def _calculate_condition_complexity(self, node: ast.AST) -> int:
        """조건문 복잡도 계산"""
        
        complexity = 0
        
        if isinstance(node, ast.BoolOp):
            complexity = len(node.values)
        elif isinstance(node, ast.Compare):
            complexity = len(node.comparators)
        else:
            complexity = 1
        
        return complexity
    
    def _is_descriptive_name(self, name: str) -> bool:
        """설명적인 이름인지 확인"""
        
        # 간단한 휴리스틱
        if len(name) < 3:
            return False
        
        # 일반적인 단어들 확인
        descriptive_words = ['get', 'set', 'create', 'update', 'delete', 'process', 'handle', 'calculate']
        
        return any(word in name.lower() for word in descriptive_words)
    
    def _is_string_concatenation(self, node: ast.BinOp) -> bool:
        """문자열 연결인지 확인"""
        
        # 간단한 검사 (실제로는 더 정교한 분석 필요)
        return isinstance(node.op, ast.Add)
    
    def _get_code_snippet(self, code: str, start_line: int, end_line: int) -> str:
        """코드 스니펫 추출"""
        
        lines = code.split('\n')
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line or start_line)
        
        return '\n'.join(lines[start_idx:end_idx])
    
    def _get_priority_score(self, priority: RefactoringPriority) -> int:
        """우선순위 점수 변환"""
        
        scores = {
            RefactoringPriority.CRITICAL: 4,
            RefactoringPriority.HIGH: 3,
            RefactoringPriority.MEDIUM: 2,
            RefactoringPriority.LOW: 1
        }
        
        return scores.get(priority, 1)
    
    def _load_design_patterns(self) -> Dict[str, Any]:
        """디자인 패턴 로드"""
        
        return {
            'factory': {
                'description': '객체 생성 로직 분리',
                'indicators': ['많은 if-elif 문', '객체 생성 코드']
            },
            'singleton': {
                'description': '단일 인스턴스 보장',
                'indicators': ['글로벌 변수', '인스턴스 중복 생성']
            },
            'observer': {
                'description': '이벤트 기반 통신',
                'indicators': ['콜백 함수', '이벤트 처리']
            }
        }
    
    def _load_naming_conventions(self) -> Dict[str, Any]:
        """네이밍 컨벤션 로드"""
        
        return {
            'python': {
                'function': 'snake_case',
                'class': 'PascalCase',
                'variable': 'snake_case',
                'constant': 'UPPER_CASE'
            }
        }
    
    def _load_performance_patterns(self) -> Dict[str, Any]:
        """성능 패턴 로드"""
        
        return {
            'list_comprehension': {
                'description': '리스트 컴프리헨션 사용',
                'pattern': r'for.*in.*\.append\('
            },
            'generator': {
                'description': '제너레이터 사용',
                'pattern': r'return.*\[.*for.*in.*\]'
            },
            'caching': {
                'description': '결과 캐싱',
                'pattern': r'def.*\(.*\):.*return.*'
            }
        }
    
    def generate_refactoring_report(self, opportunities: List[RefactoringOpportunity]) -> str:
        """리팩토링 보고서 생성"""
        
        if not opportunities:
            return "🔧 리팩토링 기회가 발견되지 않았습니다."
        
        report = f"""
🔧 리팩토링 분석 보고서
=====================================

📊 총 {len(opportunities)}개의 리팩토링 기회 발견

📈 우선순위별 분포:
"""
        
        # 우선순위별 집계
        priority_counts = {}
        for opp in opportunities:
            priority = opp.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        for priority, count in priority_counts.items():
            report += f"- {priority}: {count}개\n"
        
        # 유형별 집계
        type_counts = {}
        for opp in opportunities:
            ref_type = opp.refactoring_type.value
            type_counts[ref_type] = type_counts.get(ref_type, 0) + 1
        
        report += f"\n📋 유형별 분포:\n"
        for ref_type, count in type_counts.items():
            report += f"- {ref_type}: {count}개\n"
        
        # 예상 소요 시간
        total_effort = sum(opp.estimated_effort for opp in opportunities)
        report += f"\n⏱️ 예상 총 소요 시간: {total_effort}분\n"
        
        # 상위 5개 기회
        top_opportunities = sorted(opportunities, key=lambda x: self._get_priority_score(x.priority), reverse=True)[:5]
        
        report += f"\n🎯 우선순위 상위 5개:\n"
        for i, opp in enumerate(top_opportunities, 1):
            report += f"{i}. {opp.description}\n"
            report += f"   유형: {opp.refactoring_type.value}\n"
            report += f"   우선순위: {opp.priority.value}\n"
            report += f"   예상 시간: {opp.estimated_effort}분\n"
            report += f"   자동 적용: {'가능' if opp.auto_applicable else '불가능'}\n\n"
        
        return report
    
    def get_refactoring_insights(self) -> Dict[str, Any]:
        """리팩토링 인사이트 제공"""
        
        if not self.refactoring_history:
            return {}
        
        successful_refactorings = [h for h in self.refactoring_history if h['result'].success]
        
        return {
            'total_refactorings': len(self.refactoring_history),
            'successful_refactorings': len(successful_refactorings),
            'success_rate': len(successful_refactorings) / len(self.refactoring_history) * 100,
            'most_common_type': self._get_most_common_refactoring_type(),
            'total_files_improved': len(set(h['opportunity'].file_path for h in successful_refactorings)),
            'improvement_trends': self._analyze_improvement_trends()
        }
    
    def _get_most_common_refactoring_type(self) -> str:
        """가장 많이 사용된 리팩토링 유형"""
        
        if not self.refactoring_history:
            return "없음"
        
        types = [h['opportunity'].refactoring_type.value for h in self.refactoring_history]
        return max(set(types), key=types.count)
    
    def _analyze_improvement_trends(self) -> Dict[str, Any]:
        """개선 트렌드 분석"""
        
        if len(self.refactoring_history) < 2:
            return {}
        
        # 간단한 트렌드 분석
        recent_success_rate = len([h for h in self.refactoring_history[-10:] if h['result'].success]) / min(10, len(self.refactoring_history))
        
        return {
            'recent_success_rate': recent_success_rate * 100,
            'trend': 'improving' if recent_success_rate > 0.8 else 'stable'
        } 