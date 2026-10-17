from typing import Optional, Any
from lexer_folder.token import Token
from lexer_folder.token_type import TokenType
from lexer_folder.source_position import SourcePosition
from parser_folder.ast_nodes import (
    ASTVisitor, ProgramNode, DeclarationNode, AssignmentNode,
    IfNode, ElseIfNode, PihitanNode, KasoNode, IpakitaNode, HintoNode,
    BlockNode, BinaryOpNode, UnaryOpNode, LiteralNode, VariableAccessNode
)
from interpreter_folder.runtime_error import RuntimeError_
from interpreter_folder.break_exception import BreakException
from interpreter_folder.output_device import OutputDevice, ConsoleOutput, BufferedOutput
from interpreter_folder.environment import Environment


class Interpreter(ASTVisitor):
    """
    Runtime execution engine (Interpreter) for Peenoise Language.
    Evaluates AST nodes using the Visitor pattern, scoped Environments, and OutputDevice.
    """
    def __init__(self, output_device: Optional[OutputDevice] = None):
        self.__global_env = Environment()
        self.__environment = self.__global_env
        self.__output_device = output_device if output_device is not None else ConsoleOutput()

    @property
    def global_env(self) -> Environment:
        return self.__global_env

    @property
    def environment(self) -> Environment:
        return self.__environment

    @environment.setter
    def environment(self, env: Environment) -> None:
        self.__environment = env

    @property
    def output_device(self) -> OutputDevice:
        return self.__output_device

    def interpret(self, program: ProgramNode) -> None:
        """Main entry point to execute an AST."""
        program.accept(self)

    def visit_program(self, node: ProgramNode) -> None:
        for stmt in node.statements:
            stmt.accept(self)

    def visit_declaration(self, node: DeclarationNode) -> None:
        val = None
        if node.initializer:
            val = node.initializer.accept(self)
        self.__environment.define(node.var_name.lexeme, val)

    def visit_assignment(self, node: AssignmentNode) -> None:
        val = node.value.accept(self)
        self.__environment.assign(node.var_name, val)

    def visit_ipakita(self, node: IpakitaNode) -> None:
        value = node.expression.accept(self)
        self.__output_device.write_line(value)

    def visit_if(self, node: IfNode) -> None:
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

    def visit_pihitan(self, node: PihitanNode) -> None:
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

    def visit_kaso(self, node: KasoNode) -> None:
        for stmt in node.body:
            stmt.accept(self)

    def visit_hinto(self, node: HintoNode) -> None:
        raise BreakException()

    def visit_block(self, node: BlockNode) -> None:
        previous_env = self.__environment
        self.__environment = Environment(enclosing=previous_env)
        try:
            for stmt in node.statements:
                stmt.accept(self)
        finally:
            self.__environment = previous_env

    def visit_literal(self, node: LiteralNode) -> Any:
        return node.value

    def visit_variable_access(self, node: VariableAccessNode) -> Any:
        return self.__environment.get(node.var_token)

    def visit_binary_op(self, node: BinaryOpNode) -> Any:
        left = node.left.accept(self)
        right = node.right.accept(self)
        op = node.operator.token_type

        # Arithmetic operations
        if op in (TokenType.DAGDAG, TokenType.BAWAS, TokenType.PARAMI, TokenType.HATI, TokenType.LABIS):
            return self.__evaluate_arithmetic(op, left, right, node.position)

        # Relational operations
        if op in (TokenType.HIGIT, TokenType.MABABA, TokenType.HIGIT_O_PAREHO, TokenType.MABABA_O_PAREHO, TokenType.PAREHO, TokenType.DI_PAREHO):
            return self.__evaluate_relational(op, left, right)

        # Logical operations
        if op in (TokenType.LOHIKAL_AT, TokenType.LOHIKAL_O):
            return self.__evaluate_logical(op, left, right)

        return None

    def __evaluate_arithmetic(self, op: TokenType, left: Any, right: Any, pos: SourcePosition) -> Any:
        if op == TokenType.DAGDAG:
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op == TokenType.BAWAS:
            return left - right
        if op == TokenType.PARAMI:
            return left * right
        if op == TokenType.HATI:
            if right == 0:
                raise RuntimeError_("Hindi maaaring mag-hati sa sero (Division by zero).", pos)
            return left / right
        if op == TokenType.LABIS:
            return left % right
        return None

    def __evaluate_relational(self, op: TokenType, left: Any, right: Any) -> bool:
        if op == TokenType.HIGIT:
            return left > right
        if op == TokenType.MABABA:
            return left < right
        if op == TokenType.HIGIT_O_PAREHO:
            return left >= right
        if op == TokenType.MABABA_O_PAREHO:
            return left <= right
        if op == TokenType.PAREHO:
            return left == right
        if op == TokenType.DI_PAREHO:
            return left != right
        return False

    def __evaluate_logical(self, op: TokenType, left: Any, right: Any) -> bool:
        if op == TokenType.LOHIKAL_AT:
            return bool(left and right)
        if op == TokenType.LOHIKAL_O:
            return bool(left or right)
        return False

    def visit_unary_op(self, node: UnaryOpNode) -> Any:
        right = node.right.accept(self)
        op = node.operator.token_type

        if op == TokenType.LOHIKAL_HINDI:
            return not right
        if op == TokenType.BAWAS:
            return -right
        return None