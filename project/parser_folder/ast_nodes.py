from abc import ABC, abstractmethod
from typing import Any, List, Optional
from lexer_folder.token import Token
from lexer_folder.source_position import SourcePosition


class ASTNode(ABC):
    """Base class for all nodes in the Abstract Syntax Tree (AST)."""
    def __init__(self, position: SourcePosition):
        self.__position = position

    @property
    def position(self) -> SourcePosition:
        return self.__position

    @abstractmethod
    def accept(self, visitor: "ASTVisitor") -> Any:
        """Double-dispatch method for the Visitor pattern."""
        raise NotImplementedError("Subclasses must implement the accept method.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pos={self.__position})"


class ASTVisitor(ABC):
    """Abstract Visitor interface for processing AST nodes."""
    def visit_program(self, node: "ProgramNode") -> Any: pass
    def visit_declaration(self, node: "DeclarationNode") -> Any: pass
    def visit_assignment(self, node: "AssignmentNode") -> Any: pass
    def visit_if(self, node: "IfNode") -> Any: pass
    def visit_else_if(self, node: "ElseIfNode") -> Any: pass
    def visit_pihitan(self, node: "PihitanNode") -> Any: pass
    def visit_kaso(self, node: "KasoNode") -> Any: pass
    def visit_ipakita(self, node: "IpakitaNode") -> Any: pass
    def visit_hinto(self, node: "HintoNode") -> Any: pass
    def visit_block(self, node: "BlockNode") -> Any: pass
    def visit_binary_op(self, node: "BinaryOpNode") -> Any: pass
    def visit_unary_op(self, node: "UnaryOpNode") -> Any: pass
    def visit_literal(self, node: "LiteralNode") -> Any: pass
    def visit_variable_access(self, node: "VariableAccessNode") -> Any: pass


class ProgramNode(ASTNode):
    """Represents the root program containing a list of statements."""
    def __init__(self, statements: List[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.__statements = statements

    @property
    def statements(self) -> List[ASTNode]:
        return self.__statements

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_program(self)

    def __repr__(self) -> str:
        return f"ProgramNode(statements_count={len(self.__statements)}, pos={self.position})"


class DeclarationNode(ASTNode):
    """Represents a variable declaration with an optional initial value."""
    def __init__(self, type_token: Token, var_name: Token, initializer: Optional[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.__type_token = type_token
        self.__var_name = var_name
        self.__initializer = initializer

    @property
    def type_token(self) -> Token:
        return self.__type_token

    @property
    def var_name(self) -> Token:
        return self.__var_name

    @property
    def initializer(self) -> Optional[ASTNode]:
        return self.__initializer

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_declaration(self)

    def __repr__(self) -> str:
        return f"DeclarationNode({self.__type_token.lexeme} {self.__var_name.lexeme}, pos={self.position})"


class AssignmentNode(ASTNode):
    """Represents assigning a new value to an existing variable."""
    def __init__(self, var_name: Token, value: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.__var_name = var_name
        self.__value = value

    @property
    def var_name(self) -> Token:
        return self.__var_name

    @property
    def value(self) -> ASTNode:
        return self.__value

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_assignment(self)

    def __repr__(self) -> str:
        return f"AssignmentNode({self.__var_name.lexeme} = ..., pos={self.position})"


class ElseIfNode(ASTNode):
    """
    Represents an 'else if' (kundi_kung) branch.
    Supports property access and tuple unpacking (condition, body).
    """
    def __init__(self, condition: ASTNode, body: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.__condition = condition
        self.__body = body

    @property
    def condition(self) -> ASTNode:
        return self.__condition

    @property
    def body(self) -> ASTNode:
        return self.__body

    def __iter__(self):
        yield self.__condition
        yield self.__body

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_else_if(self)

    def __repr__(self) -> str:
        return f"ElseIfNode(pos={self.position})"


class IfNode(ASTNode):
    """Represents an if conditional statement (kung / kundi_kung / kundi)."""
    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_ifs: List[Any], else_branch: Optional[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.__condition = condition
        self.__then_branch = then_branch
        self.__else_ifs = else_ifs
        self.__else_branch = else_branch

    @property
    def condition(self) -> ASTNode:
        return self.__condition

    @property
    def then_branch(self) -> ASTNode:
        return self.__then_branch

    @property
    def else_ifs(self) -> List[Any]:
        return self.__else_ifs

    @property
    def else_branch(self) -> Optional[ASTNode]:
        return self.__else_branch

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_if(self)

    def __repr__(self) -> str:
        return f"IfNode(else_ifs_count={len(self.__else_ifs)}, has_else={self.__else_branch is not None}, pos={self.position})"


class KasoNode(ASTNode):
    """Represents a single case branch inside a switch statement (pihitan)."""
    def __init__(self, match_expr: ASTNode, body: List[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.__match_expr = match_expr
        self.__body = body

    @property
    def match_expr(self) -> ASTNode:
        return self.__match_expr

    @property
    def body(self) -> List[ASTNode]:
        return self.__body

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_kaso(self)

    def __repr__(self) -> str:
        return f"KasoNode(pos={self.position})"


class PihitanNode(ASTNode):
    """Represents a switch statement (pihitan) with cases and default branch."""
    def __init__(self, expr: ASTNode, cases: List[KasoNode], default_branch: Optional[List[ASTNode]], position: SourcePosition):
        super().__init__(position)
        self.__expr = expr
        self.__cases = cases
        self.__default_branch = default_branch

    @property
    def expr(self) -> ASTNode:
        return self.__expr

    @property
    def cases(self) -> List[KasoNode]:
        return self.__cases

    @property
    def default_branch(self) -> Optional[List[ASTNode]]:
        return self.__default_branch

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_pihitan(self)

    def __repr__(self) -> str:
        return f"PihitanNode(cases_count={len(self.__cases)}, pos={self.position})"


class IpakitaNode(ASTNode):
    """Represents a print statement (ipakita) to output an expression."""
    def __init__(self, expression: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.__expression = expression

    @property
    def expression(self) -> ASTNode:
        return self.__expression

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_ipakita(self)

    def __repr__(self) -> str:
        return f"IpakitaNode(pos={self.position})"


class HintoNode(ASTNode):
    """Represents a break statement (hinto) in loops or switch cases."""
    def __init__(self, position: SourcePosition):
        super().__init__(position)

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_hinto(self)

    def __repr__(self) -> str:
        return f"HintoNode(pos={self.position})"


class BlockNode(ASTNode):
    """Represents a block of statements enclosed in curly braces {}."""
    def __init__(self, statements: List[ASTNode], position: SourcePosition):
        super().__init__(position)
        self.__statements = statements

    @property
    def statements(self) -> List[ASTNode]:
        return self.__statements

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_block(self)

    def __repr__(self) -> str:
        return f"BlockNode(statements_count={len(self.__statements)}, pos={self.position})"


class BinaryOpNode(ASTNode):
    """Represents a binary operation with left operand, operator, and right operand."""
    def __init__(self, left: ASTNode, operator: Token, right: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.__left = left
        self.__operator = operator
        self.__right = right

    @property
    def left(self) -> ASTNode:
        return self.__left

    @property
    def operator(self) -> Token:
        return self.__operator

    @property
    def right(self) -> ASTNode:
        return self.__right

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_binary_op(self)

    def __repr__(self) -> str:
        return f"BinaryOpNode({self.__operator.lexeme}, pos={self.position})"


class UnaryOpNode(ASTNode):
    """Represents a unary operation with an operator and a right operand."""
    def __init__(self, operator: Token, right: ASTNode, position: SourcePosition):
        super().__init__(position)
        self.__operator = operator
        self.__right = right

    @property
    def operator(self) -> Token:
        return self.__operator

    @property
    def right(self) -> ASTNode:
        return self.__right

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_unary_op(self)

    def __repr__(self) -> str:
        return f"UnaryOpNode({self.__operator.lexeme}, pos={self.position})"


class LiteralNode(ASTNode):
    """Represents a constant literal value like number, string, or boolean."""
    def __init__(self, value: Any, type_name: str, position: SourcePosition):
        super().__init__(position)
        self.__value = value
        self.__type_name = type_name

    @property
    def value(self) -> Any:
        return self.__value

    @property
    def type_name(self) -> str:
        return self.__type_name

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_literal(self)

    def __repr__(self) -> str:
        return f"LiteralNode({repr(self.__value)}: {self.__type_name}, pos={self.position})"


class VariableAccessNode(ASTNode):
    """Represents reading or accessing a variable's value."""
    def __init__(self, var_token: Token, position: SourcePosition):
        super().__init__(position)
        self.__var_token = var_token

    @property
    def var_token(self) -> Token:
        return self.__var_token

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_variable_access(self)

    def __repr__(self) -> str:
        return f"VariableAccessNode({self.__var_token.lexeme}, pos={self.position})"