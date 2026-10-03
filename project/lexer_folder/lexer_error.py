from lexer_folder.source_position import SourcePosition

class LexerError(Exception):
    def __init__(self, message: str, position: SourcePosition):
        self.__position = position
        self.__message = message
        super().__init__(f"Maling Karakter sa {self.__position}: {self.__message}")

    @property
    def position(self) -> SourcePosition:
        return self.__position

    @property
    def message(self) -> str:
        return self.__message