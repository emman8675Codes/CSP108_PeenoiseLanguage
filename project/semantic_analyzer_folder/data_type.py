from enum import Enum
from typing import Optional
from lexer_folder.token_type import TokenType


class DataType(str, Enum):
    """
    Represents the data types in Peenoise Language.
    Encapsulates type compatibility and operator rules within the DataType class.
    """
    BUONG_NUMERO = "buong_numero"
    LUTANG_NUMERO = "lutang_numero"
    SALITA = "salita"
    TITIK = "titik_uri"
    KATOTOHANAN = "katotohanan"
    DI_KILALA = "di_kilala"

    @classmethod
    def from_token_type(cls, token_type: TokenType) -> "DataType":
        """Maps a TokenType to its corresponding DataType."""
        mapping = {
            TokenType.URI_BUONG_NUMERO: cls.BUONG_NUMERO,
            TokenType.URI_LUTANG_NUMERO: cls.LUTANG_NUMERO,
            TokenType.URI_SALITA: cls.SALITA,
            TokenType.URI_TITIK: cls.TITIK,
            TokenType.URI_KATOTOHANAN: cls.KATOTOHANAN,
        }
        return mapping.get(token_type, cls.DI_KILALA)

    @classmethod
    def from_name(cls, name: str) -> "DataType":
        """Returns a DataType matching the given type name string."""
        for dt in cls:
            if dt.value == name:
                return dt
        return cls.DI_KILALA

    def is_numeric(self) -> bool:
        """Returns True if the type is a number (integer or float)."""
        return self in (DataType.BUONG_NUMERO, DataType.LUTANG_NUMERO)

    def is_boolean(self) -> bool:
        """Returns True if the type is a boolean (katotohanan)."""
        return self == DataType.KATOTOHANAN

    def is_text(self) -> bool:
        """Returns True if the type is a string (salita) or character (titik_uri)."""
        return self in (DataType.SALITA, DataType.TITIK)

    def is_compatible_with(self, source: "DataType") -> bool:
        """
        Checks if this target type can accept the source type.
        Allows assigning integer into float (widening).
        """
        if self == source:
            return True
        if self == DataType.LUTANG_NUMERO and source == DataType.BUONG_NUMERO:
            return True
        return False

    def can_assign_from(self, source: "DataType") -> bool:
        """Alias for is_compatible_with."""
        return self.is_compatible_with(source)

    def can_compare_relational(self, other: "DataType") -> bool:
        """Relational comparisons (>, <, >=, <=) require both types to be numeric."""
        return self.is_numeric() and other.is_numeric()

    def can_compare_equality(self, other: "DataType") -> bool:
        """Equality comparisons (==, !=) require mutually compatible types."""
        return self.is_compatible_with(other) or other.is_compatible_with(self)

    def arithmetic_result(self, op: TokenType, other: "DataType") -> Optional["DataType"]:
        """
        Returns the resulting DataType after an arithmetic operation.
        Returns None if the operation is invalid for these types.
        """
        # String concatenation (+)
        if op == TokenType.DAGDAG and (self == DataType.SALITA or other == DataType.SALITA):
            return DataType.SALITA

        # Arithmetic between numbers
        if self.is_numeric() and other.is_numeric():
            if self == DataType.LUTANG_NUMERO or other == DataType.LUTANG_NUMERO:
                return DataType.LUTANG_NUMERO
            return DataType.BUONG_NUMERO

        return None
