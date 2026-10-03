from typing import List, Optional, Any
from lexer_folder.token import Token
from lexer_folder.source_position import SourcePosition


class ASTNode:
    def __init__(self, position: SourcePosition):
        self.position = position

    def accept(self, visitor: 'ASTVisitor') -> Any:
        raise NotImplementedError("Dapat ipatupad ang accept method sa sub-class.")


class ASTVisitor:
    def visit_program(self, node: 'ProgramNode') -> Any: pass
    def visit_declaration(self, node: 'DeclarationNode') -> Any: pass
    def visit_assignment(self, node: 'AssignmentNode') -> Any: pass
    def visit_if(self, node: 'IfNode') -> Any: pass
    def visit_pihitan(self, node: 'PihitanNode') -> Any: pass
    def visit_kaso(self, node: 'KasoNode') -> Any: pass
    def visit_ipakita(self, node: 'IpakitaNode') -> Any: pass
    def visit_hinto(self, node: 'HintoNode') -> Any: pass
    def visit_block(self, node: 'BlockNode') -> Any: pass
    def visit_binary_op(self, node: 'BinaryOpNode') -> Any: pass
    def visit_unary_op(self, node: 'UnaryOpNode') -> Any: pass
    def visit_literal(self, node: 'LiteralNode') -> Any: pass
    def visit_variable_access(self, node: 'VariableAccessNode') -> Any: pass


class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.statements = statements

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_program(self)


class DeclarationNode(ASTNode):
    def __init__(self, type_token: Token, var_name: Token, initializer: Optional[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.type_token = type_token
        self.var_name = var_name
        self.initializer = initializer

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_declaration(self)


class AssignmentNode(ASTNode):
    def __init__(self, var_name: Token, value: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.var_name = var_name
        self.value = value

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_assignment(self)


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_ifs: List[tuple], else_branch: Optional[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.condition = condition
        self.then_branch = then_branch
        self.else_ifs = else_ifs
        self.else_branch = else_branch

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_if(self)


class KasoNode(ASTNode):
    def __init__(self, match_expr: ASTNode, body: List[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.match_expr = match_expr
        self.body = body

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_kaso(self)


class PihitanNode(ASTNode):
    def __init__(self, expr: ASTNode, cases: List[KasoNode], default_branch: Optional[List[ASTNode]], position: SourcePosition):
        super().__init__(position)
        self.expr = expr
        self.cases = cases
        self.default_branch = default_branch

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_pihitan(self)


class IpakitaNode(ASTNode):
    def __init__(self, expression: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.expression = expression

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_ipakita(self)


class HintoNode(ASTNode):
    def __init__(self, position: SourcePosition):
        super().__init__(position)

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_hinto(self)


class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.statements = statements

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_block(self)


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, operator: Token, right: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_binary_op(self)


class UnaryOpNode(ASTNode):
    def __init__(self, operator: Token, right: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.operator = operator
        self.right = right

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_unary_op(self)


class LiteralNode(ASTNode):
    def __init__(self, value: Any, type_name: str, position: SourcePosition):
        super().__init__(position)
        self.value = value
        self.type_name = type_name

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_literal(self)


class VariableAccessNode(ASTNode):
    def __init__(self, var_token: Token, position: SourcePosition):
        super().__init__(position)
        self.var_token = var_token

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_variable_access(self)