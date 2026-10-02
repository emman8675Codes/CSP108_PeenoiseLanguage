
class SourcePosition:
    def __init__(self, line: int, column: int):
        self.__line = line
        self.__column = column

    @property
    def line(self) -> int:
        return self.__line

    @property
    def column(self) -> int:
        return self.__column

    def __str__(self) -> str:
        return f"Linya {self.__line}, Kolum {self.__column}"

    def __repr__(self) -> str:
        return f"Linya {self.__line}, Kolum {self.__column}"