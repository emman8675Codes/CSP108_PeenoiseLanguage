from lexer_folder.token import Token
from lexer_folder.source_position import SourcePosition


class ASTNode:
    def __init__(self, position):
        self.position = position

    def accept(self, visitor):
        raise NotImplementedError("Dapat ipatupad ang accept method sa sub-class.")


class ASTVisitor:
    def visit_program(self, node): pass
    def visit_declaration(self, node): pass
    def visit_assignment(self, node): pass
    def visit_if(self, node): pass
    def visit_pihitan(self, node): pass
    def visit_kaso(self, node): pass
    def visit_ipakita(self, node): pass
    def visit_hinto(self, node): pass
    def visit_block(self, node): pass
    def visit_binary_op(self, node): pass
    def visit_unary_op(self, node): pass
    def visit_literal(self, node): pass
    def visit_variable_access(self, node): pass


class ProgramNode(ASTNode):
    def __init__(self, statements, position):
        super().__init__(position)
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_program(self)


class DeclarationNode(ASTNode):
    def __init__(self, type_token, var_name, initializer, position):
        super().__init__(position)
        self.type_token = type_token
        self.var_name = var_name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_declaration(self)


class AssignmentNode(ASTNode):
    def __init__(self, var_name, value, position):
        super().__init__(position)
        self.var_name = var_name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment(self)


class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_ifs, else_branch, position):
        super().__init__(position)
        self.condition = condition
        self.then_branch = then_branch
        self.else_ifs = else_ifs
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if(self)


class KasoNode(ASTNode):
    def __init__(self, match_expr, body, position):
        super().__init__(position)
        self.match_expr = match_expr
        self.body = body

    def accept(self, visitor):
        return visitor.visit_kaso(self)


class PihitanNode(ASTNode):
    def __init__(self, expr, cases, default_branch, position):
        super().__init__(position)
        self.expr = expr
        self.cases = cases
        self.default_branch = default_branch

    def accept(self, visitor):
        return visitor.visit_pihitan(self)


class IpakitaNode(ASTNode):
    def __init__(self, expression, position):
        super().__init__(position)
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_ipakita(self)


class HintoNode(ASTNode):
    def __init__(self, position):
        super().__init__(position)

    def accept(self, visitor):
        return visitor.visit_hinto(self)


class BlockNode(ASTNode):
    def __init__(self, statements, position):
        super().__init__(position)
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)


class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right, position):
        super().__init__(position)
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_op(self)


class UnaryOpNode(ASTNode):
    def __init__(self, operator, right, position):
        super().__init__(position)
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_op(self)


class LiteralNode(ASTNode):
    def __init__(self, value, type_name, position):
        super().__init__(position)
        self.value = value
        self.type_name = type_name

    def accept(self, visitor):
        return visitor.visit_literal(self)


class VariableAccessNode(ASTNode):
    def __init__(self, var_token, position):
        super().__init__(position)
        self.var_token = var_token

    def accept(self, visitor):
        return visitor.visit_variable_access(self)