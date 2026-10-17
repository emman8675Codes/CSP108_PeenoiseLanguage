from lexer_folder.source_position import SourcePosition


class ParserError(Exception):
    """Represents a syntax or grammar error during parsing."""
    def __init__(self, message: str, position: SourcePosition):
        self.__position = position
        self.__message = message
        super().__init__(f"Maling Grammar sa {self.__position}: {self.__message}")

    @property
    def position(self) -> SourcePosition:
        return self.__position

    @property
    def message(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return f"Maling Grammar sa {self.__position}: {self.__message}"

    def __repr__(self) -> str:
        return f"ParserError({repr(self.__message)}, {repr(self.__position)})"
