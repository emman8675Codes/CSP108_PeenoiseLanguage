from lexer_folder.token_type import TokenType
from lexer_folder.source_position import SourcePosition

class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal, position: SourcePosition):
        self.__token_type = token_type
        self.__lexeme = lexeme
        self.__literal = literal
        self.__position = position

    @property
    def token_type(self) -> TokenType:
        return self.__token_type

    @property
    def lexeme(self) -> str:
        return self.__lexeme

    @property
    def literal(self):
        return self.__literal

    @property
    def position(self) -> SourcePosition:
        return self.__position

    def __str__(self) -> str:
        value_display = f", Halaga={repr(self.__literal)}" if self.__literal is not None else ""
        return f"Token({self.__token_type.name}, '{self.__lexeme}'{value_display} sa {self.__position})"

    def __repr__(self) -> str:
        return self.__str__()