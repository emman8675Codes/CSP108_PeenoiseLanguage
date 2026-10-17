from lexer_folder.source_position import SourcePosition


class SemanticError(Exception):
    """Represents a semantic error such as a type mismatch or undeclared variable."""
    def __init__(self, message: str, position: SourcePosition):
        self.__position = position
        self.__message = message
        super().__init__(f"Maling Semantika sa {self.__position}: {self.__message}")

    @property
    def position(self) -> SourcePosition:
        return self.__position

    @property
    def message(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return f"Maling Semantika sa {self.__position}: {self.__message}"

    def __repr__(self) -> str:
        return f"SemanticError({repr(self.__message)}, {repr(self.__position)})"
