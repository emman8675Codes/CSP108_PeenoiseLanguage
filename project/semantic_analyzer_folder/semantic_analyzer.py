from typing import Optional, Any
from lexer_folder.token_type import TokenType
from lexer_folder.source_position import SourcePosition
from parser_folder.ast_nodes import (
    ASTVisitor, ProgramNode, DeclarationNode, AssignmentNode, IfNode,
    ElseIfNode, PihitanNode, KasoNode, IpakitaNode, HintoNode, BlockNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, VariableAccessNode
)
from semantic_analyzer_folder.semantic_error import SemanticError
from semantic_analyzer_folder.data_type import DataType
from semantic_analyzer_folder.symbol import Symbol
from semantic_analyzer_folder.symbol_environment import SymbolEnvironment


class SemanticAnalyzer(ASTVisitor):
    """
    Semantic analyzer for Peenoise Language.
    Performs type checking, scope validation, and checks that variables are declared before use.
    """
    def __init__(self):
        self.__current_env = SymbolEnvironment()

    @property
    def current_env(self) -> SymbolEnvironment:
        return self.__current_env

    def analyze(self, program: ProgramNode) -> None:
        """Main entry point to perform semantic analysis on an AST."""
        program.accept(self)

    def visit_program(self, node: ProgramNode) -> None:
        for stmt in node.statements:
            stmt.accept(self)

    def visit_declaration(self, node: DeclarationNode) -> None:
        target_type = DataType.from_token_type(node.type_token.token_type)
        var_name = node.var_name.lexeme

        if node.initializer:
            init_res = node.initializer.accept(self)
            init_type = DataType.from_name(str(init_res)) if init_res is not None else DataType.DI_KILALA
            if not target_type.can_assign_from(init_type):
                raise SemanticError(
                    f"Hindi maipasa ang halagang uri '{init_type.value}' sa baryabol na uri '{target_type.value}'.",
                    node.position
                )

        self.__current_env.define(var_name, target_type, node.position)

    def visit_assignment(self, node: AssignmentNode) -> None:
        var_name = node.var_name.lexeme
        symbol = self.__current_env.lookup_symbol(var_name)

        if not symbol:
            raise SemanticError(f"Hindi pa naidedeklara ang baryabol na '{var_name}'.", node.position)

        val_res = node.value.accept(self)
        val_type = DataType.from_name(str(val_res)) if val_res is not None else DataType.DI_KILALA
        if not symbol.type.can_assign_from(val_type):
            raise SemanticError(
                f"Hindi maipasa ang halagang uri '{val_type.value}' sa baryabol na uri '{symbol.type_name}'.",
                node.position
            )

    def visit_if(self, node: IfNode) -> None:
        cond_res = node.condition.accept(self)
        cond_type = DataType.from_name(str(cond_res)) if cond_res is not None else DataType.DI_KILALA
        if not cond_type.is_boolean():
            raise SemanticError("Ang kondisyon sa 'kung' ay dapat na uri ng katotohanan (boolean).", node.position)

        node.then_branch.accept(self)

        for ei_cond, ei_body in node.else_ifs:
            ei_res = ei_cond.accept(self)
            ei_type = DataType.from_name(str(ei_res)) if ei_res is not None else DataType.DI_KILALA
            if not ei_type.is_boolean():
                raise SemanticError("Ang kondisyon sa 'kundi_kung' ay dapat na uri ng katotohanan.", node.position)
            ei_body.accept(self)

        if node.else_branch:
            node.else_branch.accept(self)

    def visit_pihitan(self, node: PihitanNode) -> None:
        expr_res = node.expr.accept(self)
        expr_type = DataType.from_name(str(expr_res)) if expr_res is not None else DataType.DI_KILALA

        for case in node.cases:
            case_res = case.match_expr.accept(self)
            case_type = DataType.from_name(str(case_res)) if case_res is not None else DataType.DI_KILALA
            if not expr_type.is_compatible_with(case_type):
                raise SemanticError(
                    f"Ang halaga ng kaso ('{case_type.value}') ay hindi tumutugma sa uri ng pihitan ('{expr_type.value}').",
                    case.position
                )
            case.accept(self)

        if node.default_branch:
            for stmt in node.default_branch:
                stmt.accept(self)

    def visit_kaso(self, node: KasoNode) -> None:
        for stmt in node.body:
            stmt.accept(self)

    def visit_ipakita(self, node: IpakitaNode) -> None:
        node.expression.accept(self)

    def visit_hinto(self, node: HintoNode) -> None:
        pass

    def visit_block(self, node: BlockNode) -> None:
        previous_env = self.__current_env
        self.__current_env = SymbolEnvironment(enclosing=previous_env)
        try:
            for stmt in node.statements:
                stmt.accept(self)
        finally:
            self.__current_env = previous_env

    def visit_binary_op(self, node: BinaryOpNode) -> str:
        left_res = node.left.accept(self)
        right_res = node.right.accept(self)
        left_t = DataType.from_name(str(left_res)) if left_res is not None else DataType.DI_KILALA
        right_t = DataType.from_name(str(right_res)) if right_res is not None else DataType.DI_KILALA
        op_t = node.operator.token_type

        # Arithmetic operators (+, -, *, /, %)
        if op_t in (TokenType.DAGDAG, TokenType.BAWAS, TokenType.PARAMI, TokenType.HATI, TokenType.LABIS):
            result_t = left_t.arithmetic_result(op_t, right_t)
            if result_t:
                return result_t.value
            raise SemanticError(
                f"Hindi maaaring gamitin ang operator na '{node.operator.lexeme}' sa '{left_t.value}' at '{right_t.value}'.",
                node.position
            )

        # Relational operators (>, <, >=, <=)
        if op_t in (TokenType.HIGIT, TokenType.MABABA, TokenType.HIGIT_O_PAREHO, TokenType.MABABA_O_PAREHO):
            if left_t.can_compare_relational(right_t):
                return DataType.KATOTOHANAN.value
            raise SemanticError(
                f"Hindi maitatambal ang '{left_t.value}' at '{right_t.value}' sa paghahambing.",
                node.position
            )

        # Equality operators (==, !=)
        if op_t in (TokenType.PAREHO, TokenType.DI_PAREHO):
            if left_t.can_compare_equality(right_t):
                return DataType.KATOTOHANAN.value
            raise SemanticError(
                f"Hindi maipaghahambing ang magkaibang uri na '{left_t.value}' at '{right_t.value}'.",
                node.position
            )

        # Logical operators (&&, ||)
        if op_t in (TokenType.LOHIKAL_AT, TokenType.LOHIKAL_O):
            if left_t.is_boolean() and right_t.is_boolean():
                return DataType.KATOTOHANAN.value
            raise SemanticError(
                "Ang lohikal na operator ay para lamang sa uri ng katotohanan.",
                node.position
            )

        return DataType.DI_KILALA.value

    def visit_unary_op(self, node: UnaryOpNode) -> str:
        right_res = node.right.accept(self)
        right_t = DataType.from_name(str(right_res)) if right_res is not None else DataType.DI_KILALA
        op_t = node.operator.token_type

        if op_t == TokenType.LOHIKAL_HINDI:
            if right_t.is_boolean():
                return DataType.KATOTOHANAN.value
            raise SemanticError("Ang '!' ay para lamang sa uri ng katotohanan.", node.position)

        if op_t == TokenType.BAWAS:
            if right_t.is_numeric():
                return right_t.value
            raise SemanticError("Ang negatibong sign '-' ay para lamang sa mga numero.", node.position)

        return DataType.DI_KILALA.value

    def visit_literal(self, node: LiteralNode) -> str:
        return node.type_name

    def visit_variable_access(self, node: VariableAccessNode) -> str:
        var_name = node.var_token.lexeme
        symbol = self.__current_env.lookup_symbol(var_name)
        if not symbol:
            raise SemanticError(f"Hindi pa naidedeklara ang baryabol na '{var_name}'.", node.position)
        return symbol.type_name