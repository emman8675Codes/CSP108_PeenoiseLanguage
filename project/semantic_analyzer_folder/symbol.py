from lexer_folder.source_position import SourcePosition
from semantic_analyzer_folder.data_type import DataType


class Symbol:
    """Represents an entry in the symbol table with name, type, and source position."""
    def __init__(self, name: str, data_type: DataType, position: SourcePosition):
        self.__name = name
        self.__type = data_type if isinstance(data_type, DataType) else DataType.from_name(str(data_type))
        self.__position = position

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> DataType:
        return self.__type

    @property
    def type_name(self) -> str:
        return self.__type.value

    @property
    def position(self) -> SourcePosition:
        return self.__position

    def __str__(self) -> str:
        return f"Symbol({self.__name}: {self.__type.value} at {self.__position})"

    def __repr__(self) -> str:
        return f"Symbol(name='{self.__name}', type={self.__type.value}, pos={self.__position})"
