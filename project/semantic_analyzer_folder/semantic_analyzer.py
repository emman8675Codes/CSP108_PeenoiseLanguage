from typing import Optional
from lexer_folder.token_type import TokenType
from lexer_folder.source_position import SourcePosition
from parser_folder.ast_nodes import (
    ASTVisitor, ProgramNode, DeclarationNode, AssignmentNode, IfNode,
    PihitanNode, KasoNode, IpakitaNode, HintoNode, BlockNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, VariableAccessNode
)


class SemanticError(Exception):
    def __init__(self, message: str, position: SourcePosition):
        self.position = position
        self.message = message
        super().__init__(f"Maling Semantika sa {self.position}: {self.message}")


class SymbolEnvironment:
    def __init__(self, enclosing: Optional['SymbolEnvironment'] = None):
        self.__symbols = {}
        self.__enclosing = enclosing

    def define(self, name: str, type_name: str, pos: SourcePosition):
        if name in self.__symbols:
            raise SemanticError(f"Ang baryabol na '{name}' ay naideklara na sa sakop na ito.", pos)
        self.__symbols[name] = type_name

    def lookup(self, name: str) -> Optional[str]:
        if name in self.__symbols:
            return self.__symbols[name]
        if self.__enclosing:
            return self.__enclosing.lookup(name)
        return None


class SemanticAnalyzer(ASTVisitor):
    def __init__(self):
        self.__current_env = SymbolEnvironment()

    def analyze(self, program: ProgramNode):
        program.accept(self)

    def __map_token_type(self, token_type: TokenType) -> str:
        if token_type == TokenType.URI_BUONG_NUMERO: return "buong_numero"
        if token_type == TokenType.URI_LUTANG_NUMERO: return "lutang_numero"
        if token_type == TokenType.URI_SALITA: return "salita"
        if token_type == TokenType.URI_TITIK: return "titik_uri"
        if token_type == TokenType.URI_KATOTOHANAN: return "katotohanan"
        return "di_kilala"

    def __are_types_compatible(self, target: str, source: str) -> bool:
        if target == source:
            return True
        if target == "lutang_numero" and source == "buong_numero":
            return True
        return False

    def visit_program(self, node: ProgramNode):
        for stmt in node.statements:
            stmt.accept(self)

    def visit_declaration(self, node: DeclarationNode):
        target_type = self.__map_token_type(node.type_token.token_type)
        var_name = node.var_name.lexeme

        if node.initializer:
            init_type = node.initializer.accept(self)
            if not self.__are_types_compatible(target_type, init_type):
                raise SemanticError(
                    f"Hindi maipasa ang halagang uri '{init_type}' sa baryabol na uri '{target_type}'.",
                    node.position
                )

        self.__current_env.define(var_name, target_type, node.position)

    def visit_assignment(self, node: AssignmentNode):
        var_name = node.var_name.lexeme
        target_type = self.__current_env.lookup(var_name)

        if not target_type:
            raise SemanticError(f"Hindi pa naidedeklara ang baryabol na '{var_name}'.", node.position)

        val_type = node.value.accept(self)
        if not self.__are_types_compatible(target_type, val_type):
            raise SemanticError(
                f"Hindi maipasa ang halagang uri '{val_type}' sa baryabol na uri '{target_type}'.",
                node.position
            )

    def visit_if(self, node: IfNode):
        cond_type = node.condition.accept(self)
        if cond_type != "katotohanan":
            raise SemanticError("Ang kondisyon sa 'kung' ay dapat na uri ng katotohanan (boolean).", node.position)

        node.then_branch.accept(self)

        for ei_cond, ei_body in node.else_ifs:
            if ei_cond.accept(self) != "katotohanan":
                raise SemanticError("Ang kondisyon sa 'kundi_kung' ay dapat na uri ng katotohanan.", node.position)
            ei_body.accept(self)

        if node.else_branch:
            node.else_branch.accept(self)

    def visit_pihitan(self, node: PihitanNode):
        expr_type = node.expr.accept(self)

        for case in node.cases:
            case_type = case.match_expr.accept(self)
            if not self.__are_types_compatible(expr_type, case_type):
                raise SemanticError(
                    f"Ang halaga ng kaso ('{case_type}') ay hindi tumutugma sa uri ng pihitan ('{expr_type}').",
                    case.position
                )
            case.accept(self)

        if node.default_branch:
            for stmt in node.default_branch:
                stmt.accept(self)

    def visit_kaso(self, node: KasoNode):
        for stmt in node.body:
            stmt.accept(self)

    def visit_ipakita(self, node: IpakitaNode):
        node.expression.accept(self)

    def visit_hinto(self, node: HintoNode):
        pass

    def visit_block(self, node: BlockNode):
        previous_env = self.__current_env
        self.__current_env = SymbolEnvironment(enclosing=previous_env)
        try:
            for stmt in node.statements:
                stmt.accept(self)
        finally:
            self.__current_env = previous_env

    def visit_binary_op(self, node: BinaryOpNode) -> str:
        left_t = node.left.accept(self)
        right_t = node.right.accept(self)
        op_t = node.operator.token_type

        if op_t in (TokenType.DAGDAG, TokenType.BAWAS, TokenType.PARAMI, TokenType.HATI, TokenType.LABIS):
            if left_t in ("buong_numero", "lutang_numero") and right_t in ("buong_numero", "lutang_numero"):
                return "lutang_numero" if (left_t == "lutang_numero" or right_t == "lutang_numero") else "buong_numero"
            if op_t == TokenType.DAGDAG and (left_t == "salita" or right_t == "salita"):
                return "salita"
            raise SemanticError(f"Hindi maaaring gamitin ang operator na '{node.operator.lexeme}' sa '{left_t}' at '{right_t}'.", node.position)

        if op_t in (TokenType.HIGIT, TokenType.MABABA, TokenType.HIGIT_O_PAREHO, TokenType.MABABA_O_PAREHO):
            if left_t in ("buong_numero", "lutang_numero") and right_t in ("buong_numero", "lutang_numero"):
                return "katotohanan"
            raise SemanticError(f"Hindi maitatambal ang '{left_t}' at '{right_t}' sa paghahambing.", node.position)

        if op_t in (TokenType.PAREHO, TokenType.DI_PAREHO):
            if self.__are_types_compatible(left_t, right_t) or self.__are_types_compatible(right_t, left_t):
                return "katotohanan"
            raise SemanticError(f"Hindi maipaghahambing ang magkaibang uri na '{left_t}' at '{right_t}'.", node.position)

        if op_t in (TokenType.LOHIKAL_AT, TokenType.LOHIKAL_O):
            if left_t == "katotohanan" and right_t == "katotohanan":
                return "katotohanan"
            raise SemanticError("Ang lohikal na operator ay para lamang sa uri ng katotohanan.", node.position)

        return "di_kilala"

    def visit_unary_op(self, node: UnaryOpNode) -> str:
        right_t = node.right.accept(self)
        op_t = node.operator.token_type

        if op_t == TokenType.LOHIKAL_HINDI:
            if right_t == "katotohanan":
                return "katotohanan"
            raise SemanticError("Ang '!' ay para lamang sa uri ng katotohanan.", node.position)

        if op_t == TokenType.BAWAS:
            if right_t in ("buong_numero", "lutang_numero"):
                return right_t
            raise SemanticError("Ang negatibong sign '-' ay para lamang sa mga numero.", node.position)

        return "di_kilala"

    def visit_literal(self, node: LiteralNode) -> str:
        return node.type_name

    def visit_variable_access(self, node: VariableAccessNode) -> str:
        var_name = node.var_token.lexeme
        var_type = self.__current_env.lookup(var_name)
        if not var_type:
            raise SemanticError(f"Hindi pa naidedeklara ang baryabol na '{var_name}'.", node.position)
        return var_type