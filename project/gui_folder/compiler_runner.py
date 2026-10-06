"""
Compiler Runner for Peenoise Language.
Orchestrates the 4 compiler phases (Lexer -> Parser -> SemanticAnalyzer -> Interpreter),
captures terminal outputs, tracks execution time, extracts token streams, 
formats AST trees, and provides comprehensive error diagnostics with code pointers.
"""

import io
import time
import contextlib
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from lexer_folder.lexer import Lexer
from lexer_folder.lexer_error import LexerError
from lexer_folder.token import Token
from lexer_folder.token_type import TokenType

from parser_folder.parser import Parser, ParserError
from parser_folder.ast_nodes import (
    ASTVisitor, ASTNode, ProgramNode, DeclarationNode, AssignmentNode,
    IfNode, PihitanNode, KasoNode, IpakitaNode, HintoNode,
    BlockNode, BinaryOpNode, UnaryOpNode, LiteralNode, VariableAccessNode
)

from semantic_analyzer_folder.semantic_analyzer import SemanticAnalyzer, SemanticError
from interpreter_folder.interpreter import Interpreter, RuntimeError_


@dataclass
class TokenInfo:
    line: int
    column: int
    token_type: str
    lexeme: str
    literal: Any


@dataclass
class ExecutionResult:
    success: bool
    output: str
    tokens: List[TokenInfo] = field(default_factory=list)
    ast_tree: str = ""
    variables: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    phase: str = ""
    error_type: str = ""
    error_message: str = ""
    error_line: Optional[int] = None
    error_column: Optional[int] = None
    error_snippet: str = ""


class ASTTreeFormatter(ASTVisitor):
    """Generates a clean, hierarchical ASCII/Unicode tree representation of the AST."""
    def __init__(self):
        self.lines = []
        self.indent = 0

    def format(self, node: ASTNode) -> str:
        self.lines = []
        self.indent = 0
        if node:
            node.accept(self)
        return "\n".join(self.lines)

    def _add(self, text: str):
        prefix = "    " * self.indent
        self.lines.append(f"{prefix}{text}")

    def visit_program(self, node: ProgramNode):
        self._add(f"📜 Program ({node.position})")
        self.indent += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent -= 1

    def visit_declaration(self, node: DeclarationNode):
        type_str = node.type_token.lexeme
        var_str = node.var_name.lexeme
        self._add(f"🔹 Deklarasyon: {type_str} {var_str} ({node.position})")
        if node.initializer:
            self.indent += 1
            self._add("Halaga / Initializer:")
            self.indent += 1
            node.initializer.accept(self)
            self.indent -= 2

    def visit_assignment(self, node: AssignmentNode):
        self._add(f"📝 Pagtatakda: {node.var_name.lexeme} = ... ({node.position})")
        self.indent += 1
        node.value.accept(self)
        self.indent -= 1

    def visit_if(self, node: IfNode):
        self._add(f"🔀 Kung-Pahayag ({node.position})")
        self.indent += 1
        self._add("Kondisyon:")
        self.indent += 1
        node.condition.accept(self)
        self.indent -= 1
        
        self._add("Kung-Sangay (Then):")
        self.indent += 1
        node.then_branch.accept(self)
        self.indent -= 1

        for idx, (ei_cond, ei_body) in enumerate(node.else_ifs):
            self._add(f"Kundi-Kung #{idx + 1}:")
            self.indent += 1
            self._add("Kondisyon:")
            self.indent += 1
            ei_cond.accept(self)
            self.indent -= 1
            self._add("Katawan:")
            self.indent += 1
            ei_body.accept(self)
            self.indent -= 2

        if node.else_branch:
            self._add("Kundi-Sangay (Else):")
            self.indent += 1
            node.else_branch.accept(self)
            self.indent -= 1
        self.indent -= 1

    def visit_pihitan(self, node: PihitanNode):
        self._add(f"🎛️ Pihitan (Switch) ({node.position})")
        self.indent += 1
        self._add("Sinusuring Ekspresyon:")
        self.indent += 1
        node.expr.accept(self)
        self.indent -= 1

        for case in node.cases:
            case.accept(self)

        if node.default_branch:
            self._add("Likas (Default):")
            self.indent += 1
            for stmt in node.default_branch:
                stmt.accept(self)
            self.indent -= 1
        self.indent -= 1

    def visit_kaso(self, node: KasoNode):
        self._add(f"🔸 Kaso ({node.position}):")
        self.indent += 1
        self._add("Halagang Itutugma:")
        self.indent += 1
        node.match_expr.accept(self)
        self.indent -= 1
        self._add("Katawan ng Kaso:")
        self.indent += 1
        for stmt in node.body:
            stmt.accept(self)
        self.indent -= 2

    def visit_ipakita(self, node: IpakitaNode):
        self._add(f"📢 Ipakita (Print) ({node.position})")
        self.indent += 1
        node.expression.accept(self)
        self.indent -= 1

    def visit_hinto(self, node: HintoNode):
        self._add(f"🛑 Hinto (Break) ({node.position})")

    def visit_block(self, node: BlockNode):
        self._add(f"📦 Sakop / Block ({node.position})")
        self.indent += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent -= 1

    def visit_binary_op(self, node: BinaryOpNode):
        self._add(f"⚙️ BinaryOp [{node.operator.lexeme}] ({node.position})")
        self.indent += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent -= 1

    def visit_unary_op(self, node: UnaryOpNode):
        self._add(f"⚡ UnaryOp [{node.operator.lexeme}] ({node.position})")
        self.indent += 1
        node.right.accept(self)
        self.indent -= 1

    def visit_literal(self, node: LiteralNode):
        val_repr = repr(node.value)
        self._add(f"🏷️ Literal ({node.type_name}): {val_repr}")

    def visit_variable_access(self, node: VariableAccessNode):
        self._add(f"🔖 Baryabol: {node.var_token.lexeme} ({node.position})")


class CompilerRunner:
    """Manages compilation and execution of Peenoise Language scripts."""

    @classmethod
    def create_error_snippet(cls, source_code: str, line: Optional[int], column: Optional[int]) -> str:
        """Creates a visual code pointer showing line number and caret under error column."""
        if not source_code or not line:
            return ""
        lines = source_code.splitlines()
        if 1 <= line <= len(lines):
            target_line = lines[line - 1]
            caret_col = max(1, column if column else 1)
            # Indent caret according to column position
            caret_line = " " * (caret_col - 1) + "^"
            return f"  Linya {line}: {target_line}\n           {caret_line}"
        return ""

    @classmethod
    def run(cls, source_code: str) -> ExecutionResult:
        """Executes the Peenoise source code through all four compiler phases."""
        start_time = time.perf_counter()
        token_infos: List[TokenInfo] = []
        captured_output = ""
        ast_tree_str = ""
        variables: Dict[str, Any] = {}

        # Strip surrounding whitespace for check
        if not source_code.strip():
            return ExecutionResult(
                success=True,
                output="(Walang nakasulat na kodigo. Maglagay ng kodigo sa kaliwa at pindutin ang Patakbuhin.)",
                execution_time_ms=0.0
            )

        # -------------------------------------------------------------
        # PHASE 1: LEXICAL ANALYSIS (Lexer)
        # -------------------------------------------------------------
        current_phase = "Pagsusuring Leksikal (Lexer)"
        try:
            lexer = Lexer(source_code)
            tokens: List[Token] = lexer.tokenize()

            for tok in tokens:
                token_infos.append(TokenInfo(
                    line=tok.position.line,
                    column=tok.position.column,
                    token_type=tok.token_type.name,
                    lexeme=tok.lexeme,
                    literal=tok.literal
                ))
        except LexerError as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            line = err.position.line if hasattr(err, "position") else None
            col = err.position.column if hasattr(err, "position") else None
            snippet = cls.create_error_snippet(source_code, line, col)
            return ExecutionResult(
                success=False,
                output="",
                tokens=token_infos,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type="LexerError",
                error_message=str(err),
                error_line=line,
                error_column=col,
                error_snippet=snippet
            )
        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                success=False,
                output="",
                tokens=token_infos,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type=type(err).__name__,
                error_message=f"Di-inaasahang error sa Lexer: {err}",
            )

        # -------------------------------------------------------------
        # PHASE 2: SYNTAX ANALYSIS (Parser)
        # -------------------------------------------------------------
        current_phase = "Pagsusuring Sintaktiko (Parser)"
        ast = None
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            # Format AST representation
            formatter = ASTTreeFormatter()
            ast_tree_str = formatter.format(ast)
        except ParserError as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            line = err.position.line if hasattr(err, "position") else None
            col = err.position.column if hasattr(err, "position") else None
            snippet = cls.create_error_snippet(source_code, line, col)
            return ExecutionResult(
                success=False,
                output="",
                tokens=token_infos,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type="ParserError",
                error_message=str(err),
                error_line=line,
                error_column=col,
                error_snippet=snippet
            )
        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                success=False,
                output="",
                tokens=token_infos,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type=type(err).__name__,
                error_message=f"Di-inaasahang error sa Parser: {err}",
            )

        # -------------------------------------------------------------
        # PHASE 3: SEMANTIC ANALYSIS (Type Checking & Scope)
        # -------------------------------------------------------------
        current_phase = "Pagsusuring Semantika (Semantic Analyzer)"
        try:
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
        except SemanticError as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            line = err.position.line if hasattr(err, "position") else None
            col = err.position.column if hasattr(err, "position") else None
            snippet = cls.create_error_snippet(source_code, line, col)
            return ExecutionResult(
                success=False,
                output="",
                tokens=token_infos,
                ast_tree=ast_tree_str,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type="SemanticError",
                error_message=str(err),
                error_line=line,
                error_column=col,
                error_snippet=snippet
            )
        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                success=False,
                output="",
                tokens=token_infos,
                ast_tree=ast_tree_str,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type=type(err).__name__,
                error_message=f"Di-inaasahang error sa Semantika: {err}",
            )

        # -------------------------------------------------------------
        # PHASE 4: RUNTIME EXECUTION (Interpreter)
        # -------------------------------------------------------------
        current_phase = "Pagpapatupad (Interpreter)"
        try:
            stdout_buffer = io.StringIO()
            with contextlib.redirect_stdout(stdout_buffer):
                interpreter = Interpreter()
                interpreter.interpret(ast)

            captured_output = stdout_buffer.getvalue()
            if hasattr(interpreter, "global_env") and hasattr(interpreter.global_env, "values"):
                variables = dict(interpreter.global_env.values)

        except RuntimeError_ as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            line = err.position.line if hasattr(err, "position") else None
            col = err.position.column if hasattr(err, "position") else None
            snippet = cls.create_error_snippet(source_code, line, col)
            return ExecutionResult(
                success=False,
                output=captured_output,
                tokens=token_infos,
                ast_tree=ast_tree_str,
                variables=variables,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type="RuntimeError_",
                error_message=str(err),
                error_line=line,
                error_column=col,
                error_snippet=snippet
            )
        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                success=False,
                output=captured_output,
                tokens=token_infos,
                ast_tree=ast_tree_str,
                variables=variables,
                execution_time_ms=elapsed_ms,
                phase=current_phase,
                error_type=type(err).__name__,
                error_message=f"Di-inaasahang error sa Pagpapatupad: {err}",
            )

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return ExecutionResult(
            success=True,
            output=captured_output,
            tokens=token_infos,
            ast_tree=ast_tree_str,
            variables=variables,
            execution_time_ms=elapsed_ms,
            phase="Natapos nang Tagumpay"
        )
