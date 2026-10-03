from typing import List
from project.lexer.lexer import Token, TokenType, SourcePosition
from project.parser.ast_nodes import (
    ASTNode, ProgramNode, DeclarationNode, AssignmentNode,
    IfNode, PihitanNode, KasoNode, IpakitaNode, HintoNode,
    BlockNode, BinaryOpNode, UnaryOpNode, LiteralNode, VariableAccessNode
)


class ParserError(Exception):
    def __init__(self, message: str, position: SourcePosition):
        self.position = position
        self.message = message
        super().__init__(f"Maling Grammar sa {self.position}: {self.message}")


class Parser:
    def __init__(self, tokens: List[Token]):
        self.__tokens = tokens
        self.__current = 0

    def __is_at_end(self) -> bool:
        return self.__peek().token_type == TokenType.DULO

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.__current += 1
        return self.__previous()

    def __check(self, token_type: TokenType) -> bool:
        if self.__is_at_end():
            return False
        return self.__peek().token_type == token_type

    def __match(self, *types: TokenType) -> bool:
        for t in types:
            if self.__check(t):
                self.__advance()
                return True
        return False

    def __consume(self, token_type: TokenType, error_message: str) -> Token:
        if self.__check(token_type):
            return self.__advance()
        raise ParserError(error_message, self.__peek().position)

    def parse(self) -> ProgramNode:
        statements = []
        start_pos = self.__peek().position if self.__tokens else SourcePosition(1, 1)

        while not self.__is_at_end():
            stmt = self.__declaration_or_statement()
            if stmt:
                statements.append(stmt)

        return ProgramNode(statements, start_pos)

    def __declaration_or_statement(self) -> ASTNode:
        if self.__match(
            TokenType.URI_BUONG_NUMERO,
            TokenType.URI_LUTANG_NUMERO,
            TokenType.URI_SALITA,
            TokenType.URI_TITIK,
            TokenType.URI_KATOTOHANAN
        ):
            return self.__var_declaration()

        return self.__statement()

    def __var_declaration(self) -> DeclarationNode:
        type_tok = self.__previous()
        var_name = self.__consume(TokenType.TAGATUKOY, "Inaasahan ang pangalan ng baryabol.")

        initializer = None
        if self.__match(TokenType.PAGTATAKDA):
            initializer = self.__expression()

        self.__consume(TokenType.TULDOK_KUWIT, "Inaasahan ang ';' sa dulo ng deklarasyon.")
        return DeclarationNode(type_tok, var_name, initializer, type_tok.position)

    def __statement(self) -> ASTNode:
        if self.__match(TokenType.ITAKDA):
            return self.__var_assignment()
        if self.__match(TokenType.KUNG):
            return self.__if_statement()
        if self.__match(TokenType.PIHITAN):
            return self.__pihitan_statement()
        if self.__match(TokenType.IPAKITA):
            return self.__ipakita_statement()
        if self.__match(TokenType.HINTO):
            pos = self.__previous().position
            self.__consume(TokenType.TULDOK_KUWIT, "Inaasahan ang ';' pagkatapos ng 'hinto'.")
            return HintoNode(pos)
        if self.__match(TokenType.KALIWANG_KUKO):
            return self.__block_statement()

        if self.__check(TokenType.TAGATUKOY) and self.__peek_next_is(TokenType.PAGTATAKDA):
            var_name = self.__advance()
            self.__advance()
            val = self.__expression()
            self.__consume(TokenType.TULDOK_KUWIT, "Inaasahan ang ';' sa dulo ng pagtatakda.")
            return AssignmentNode(var_name, val, var_name.position)

        raise ParserError(f"Di-kilalang pahayag o utos '{self.__peek().lexeme}'.", self.__peek().position)

    def __peek_next_is(self, token_type: TokenType) -> bool:
        if self.__current + 1 >= len(self.__tokens):
            return False
        return self.__tokens[self.__current + 1].token_type == token_type

    def __var_assignment(self) -> AssignmentNode:
        var_name = self.__consume(TokenType.TAGATUKOY, "Inaasahan ang pangalan ng baryabol pagkatapos ng 'itakda'.")
        self.__consume(TokenType.PAGTATAKDA, "Inaasahan ang '=' sa pagtatakda ng halaga.")
        val = self.__expression()
        self.__consume(TokenType.TULDOK_KUWIT, "Inaasahan ang ';' sa dulo ng pagtatakda.")
        return AssignmentNode(var_name, val, var_name.position)

    def __if_statement(self) -> IfNode:
        pos = self.__previous().position
        self.__consume(TokenType.KALIWANG_PANIPI, "Inaasahan ang '(' pagkatapos ng 'kung'.")
        condition = self.__expression()
        self.__consume(TokenType.KANANG_PANIPI, "Inaasahan ang ')' pagkatapos ng kondisyon.")

        then_branch = self.__statement()

        else_ifs = []
        while self.__match(TokenType.KUNDI_KUNG):
            self.__consume(TokenType.KALIWANG_PANIPI, "Inaasahan ang '(' pagkatapos ng 'kundi_kung'.")
            ei_cond = self.__expression()
            self.__consume(TokenType.KANANG_PANIPI, "Inaasahan ang ')' pagkatapos ng kondisyon.")
            ei_body = self.__statement()
            else_ifs.append((ei_cond, ei_body))

        else_branch = None
        if self.__match(TokenType.KUNDI):
            else_branch = self.__statement()

        return IfNode(condition, then_branch, else_ifs, else_branch, pos)

    def __pihitan_statement(self) -> PihitanNode:
        pos = self.__previous().position
        self.__consume(TokenType.KALIWANG_PANIPI, "Inaasahan ang '(' pagkatapos ng 'pihitan'.")
        expr = self.__expression()
        self.__consume(TokenType.KANANG_PANIPI, "Inaasahan ang ')' pagkatapos ng ekspresyon ng pihitan.")
        self.__consume(TokenType.KALIWANG_KUKO, "Inaasahan ang '{' para buksan ang pihitan.")

        cases = []
        default_branch = None

        while not self.__check(TokenType.KANANG_KUKO) and not self.__is_at_end():
            if self.__match(TokenType.KASO):
                c_pos = self.__previous().position
                match_expr = self.__expression()
                self.__consume(TokenType.TUTULDOK, "Inaasahan ang ':' pagkatapos ng halaga ng kaso.")
                body = []
                while not self.__check(TokenType.KASO) and not self.__check(TokenType.LIKAS) and not self.__check(TokenType.KANANG_KUKO) and not self.__is_at_end():
                    body.append(self.__statement())
                cases.append(KasoNode(match_expr, body, c_pos))

            elif self.__match(TokenType.LIKAS):
                self.__consume(TokenType.TUTULDOK, "Inaasahan ang ':' pagkatapos ng 'likas'.")
                default_branch = []
                while not self.__check(TokenType.KASO) and not self.__check(TokenType.KANANG_KUKO) and not self.__is_at_end():
                    default_branch.append(self.__statement())

            else:
                raise ParserError("Inaasahan ang 'kaso' o 'likas' sa loob ng pihitan.", self.__peek().position)

        self.__consume(TokenType.KANANG_KUKO, "Inaasahan ang '}' para isara ang pihitan.")
        return PihitanNode(expr, cases, default_branch, pos)

    def __ipakita_statement(self) -> IpakitaNode:
        pos = self.__previous().position
        self.__consume(TokenType.KALIWANG_PANIPI, "Inaasahan ang '(' pagkatapos ng 'ipakita'.")
        expr = self.__expression()
        self.__consume(TokenType.KANANG_PANIPI, "Inaasahan ang ')' pagkatapos ng ekspresyon.")
        self.__consume(TokenType.TULDOK_KUWIT, "Inaasahan ang ';' sa dulo ng ipakita.")
        return IpakitaNode(expr, pos)

    def __block_statement(self) -> BlockNode:
        pos = self.__previous().position
        statements = []
        while not self.__check(TokenType.KANANG_KUKO) and not self.__is_at_end():
            statements.append(self.__declaration_or_statement())
        self.__consume(TokenType.KANANG_KUKO, "Inaasahan ang '}' sa dulo ng bloke.")
        return BlockNode(statements, pos)

    def __expression(self) -> ASTNode:
        return self.__logical_or()

    def __logical_or(self) -> ASTNode:
        expr = self.__logical_and()
        while self.__match(TokenType.LOHIKAL_O):
            op = self.__previous()
            right = self.__logical_and()
            expr = BinaryOpNode(expr, op, right, op.position)
        return expr

    def __logical_and(self) -> ASTNode:
        expr = self.__equality()
        while self.__match(TokenType.LOHIKAL_AT):
            op = self.__previous()
            right = self.__equality()
            expr = BinaryOpNode(expr, op, right, op.position)
        return expr

    def __equality(self) -> ASTNode:
        expr = self.__relational()
        while self.__match(TokenType.PAREHO, TokenType.DI_PAREHO):
            op = self.__previous()
            right = self.__relational()
            expr = BinaryOpNode(expr, op, right, op.position)
        return expr

    def __relational(self) -> ASTNode:
        expr = self.__additive()
        while self.__match(TokenType.HIGIT, TokenType.MABABA, TokenType.HIGIT_O_PAREHO, TokenType.MABABA_O_PAREHO):
            op = self.__previous()
            right = self.__additive()
            expr = BinaryOpNode(expr, op, right, op.position)
        return expr

    def __additive(self) -> ASTNode:
        expr = self.__multiplicative()
        while self.__match(TokenType.DAGDAG, TokenType.BAWAS):
            op = self.__previous()
            right = self.__multiplicative()
            expr = BinaryOpNode(expr, op, right, op.position)
        return expr

    def __multiplicative(self) -> ASTNode:
        expr = self.__unary()
        while self.__match(TokenType.PARAMI, TokenType.HATI, TokenType.LABIS):
            op = self.__previous()
            right = self.__unary()
            expr = BinaryOpNode(expr, op, right, op.position)
        return expr

    def __unary(self) -> ASTNode:
        if self.__match(TokenType.LOHIKAL_HINDI, TokenType.BAWAS):
            op = self.__previous()
            right = self.__unary()
            return UnaryOpNode(op, right, op.position)
        return self.__primary()

    def __primary(self) -> ASTNode:
        if self.__match(TokenType.BILANG):
            tok = self.__previous()
            t_name = "lutang_numero" if isinstance(tok.literal, float) else "buong_numero"
            return LiteralNode(tok.literal, t_name, tok.position)

        if self.__match(TokenType.TITIK):
            tok = self.__previous()
            return LiteralNode(tok.literal, "salita", tok.position)

        if self.__match(TokenType.KARAKTER):
            tok = self.__previous()
            return LiteralNode(tok.literal, "titik_uri", tok.position)

        if self.__match(TokenType.TOTOO):
            return LiteralNode(True, "katotohanan", self.__previous().position)

        if self.__match(TokenType.MALI):
            return LiteralNode(False, "katotohanan", self.__previous().position)

        if self.__match(TokenType.TAGATUKOY):
            return VariableAccessNode(self.__previous(), self.__previous().position)

        if self.__match(TokenType.KALIWANG_PANIPI):
            expr = self.__expression()
            self.__consume(TokenType.KANANG_PANIPI, "Inaasahan ang ')' pagkatapos ng ekspresyon.")
            return expr

        raise ParserError(f"Maling ekspresyon o simbolo '{self.__peek().lexeme}'.", self.__peek().position)