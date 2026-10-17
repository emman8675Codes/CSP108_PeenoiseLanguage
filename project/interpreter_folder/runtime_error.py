from lexer_folder.source_position import SourcePosition


class RuntimeError_(Exception):
    """Represents an error that occurs during program runtime execution."""
    def __init__(self, message: str, position: SourcePosition):
        self.__position = position
        self.__message = message
        super().__init__(f"Maling Pagpapatupad sa {self.__position}: {self.__message}")

    @property
    def position(self) -> SourcePosition:
        return self.__position

    @property
    def message(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return f"Maling Pagpapatupad sa {self.__position}: {self.__message}"

    def __repr__(self) -> str:
        return f"RuntimeError_({repr(self.__message)}, {repr(self.__position)})"
