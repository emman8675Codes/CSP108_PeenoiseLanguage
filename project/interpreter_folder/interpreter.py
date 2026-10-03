from lexer_folder.token import Token
from lexer_folder.token_type import TokenType
from lexer_folder.source_position import SourcePosition
from parser_folder.ast_nodes import (
    ASTVisitor, ProgramNode, DeclarationNode, AssignmentNode,
    IfNode, PihitanNode, KasoNode, IpakitaNode, HintoNode,
    BlockNode, BinaryOpNode, UnaryOpNode, LiteralNode, VariableAccessNode
)


class BreakException(Exception):
    pass


class RuntimeError_(Exception):
    def __init__(self, message, position):
        self.position = position
        self.message = message
        super().__init__(f"Maling Pagpapatupad sa {self.position}: {self.message}")


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name_token, value):
        name = name_token.lexeme
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing:
            self.enclosing.assign(name_token, value)
            return
        raise RuntimeError_(f"Hindi nahanap ang baryabol na '{name}'.", name_token.position)

    def get(self, name_token):
        name = name_token.lexeme
        if name in self.values:
            return self.values[name]
        if self.enclosing:
            return self.enclosing.get(name_token)
        raise RuntimeError_(f"Hindi pa naitatala ang halaga ng '{name}'.", name_token.position)


class Interpreter(ASTVisitor):
    def __init__(self):
        self.global_env = Environment()
        self.environment = self.global_env

    def interpret(self, program):
        program.accept(self)

    def visit_program(self, node):
        for stmt in node.statements:
            stmt.accept(self)

    def visit_declaration(self, node):
        val = None
        if node.initializer:
            val = node.initializer.accept(self)
        self.environment.define(node.var_name.lexeme, val)

    def visit_assignment(self, node):
        val = node.value.accept(self)
        self.environment.assign(node.var_name, val)

    def visit_ipakita(self, node):
        value = node.expression.accept(self)

        # Print raw output directly like System.out.println
        if isinstance(value, bool):
            print("totoo" if value else "mali")
        else:
            print(value)

    def visit_if(self, node):
        cond_val = node.condition.accept(self)
        if cond_val is True:
            node.then_branch.accept(self)
            return

        for ei_cond, ei_body in node.else_ifs:
            if ei_cond.accept(self) is True:
                ei_body.accept(self)
                return

        if node.else_branch:
            node.else_branch.accept(self)

    def visit_pihitan(self, node):
        expr_val = node.expr.accept(self)
        matched = False

        try:
            for case in node.cases:
                case_val = case.match_expr.accept(self)
                if matched or case_val == expr_val:
                    matched = True
                    case.accept(self)

            if not matched and node.default_branch:
                for stmt in node.default_branch:
                    stmt.accept(self)
        except BreakException:
            pass

    def visit_kaso(self, node):
        for stmt in node.body:
            stmt.accept(self)

    def visit_hinto(self, node):
        raise BreakException()

    def visit_block(self, node):
        previous_env = self.environment
        self.environment = Environment(enclosing=previous_env)
        try:
            for stmt in node.statements:
                stmt.accept(self)
        finally:
            self.environment = previous_env

    def visit_literal(self, node):
        return node.value

    def visit_variable_access(self, node):
        return self.environment.get(node.var_token)

    def visit_binary_op(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        op = node.operator.token_type

        # Arithmetic
        if op == TokenType.DAGDAG:
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op == TokenType.BAWAS: return left - right
        if op == TokenType.PARAMI: return left * right
        if op == TokenType.HATI:
            if right == 0:
                raise RuntimeError_("Hindi maaaring mag-hati sa sero (Division by zero).", node.position)
            return left / right
        if op == TokenType.LABIS: return left % right

        # Relational
        if op == TokenType.HIGIT: return left > right
        if op == TokenType.MABABA: return left < right
        if op == TokenType.HIGIT_O_PAREHO: return left >= right
        if op == TokenType.MABABA_O_PAREHO: return left <= right
        if op == TokenType.PAREHO: return left == right
        if op == TokenType.DI_PAREHO: return left != right

        # Logical
        if op == TokenType.LOHIKAL_AT: return bool(left and right)
        if op == TokenType.LOHIKAL_O: return bool(left or right)

        return None

    def visit_unary_op(self, node):
        right = node.right.accept(self)
        op = node.operator.token_type

        if op == TokenType.LOHIKAL_HINDI:
            return not right
        if op == TokenType.BAWAS:
            return -right
        return None