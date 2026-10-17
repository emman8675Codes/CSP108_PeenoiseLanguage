from typing import Optional, Dict, Any
from lexer_folder.source_position import SourcePosition
from semantic_analyzer_folder.semantic_error import SemanticError
from semantic_analyzer_folder.symbol import Symbol
from semantic_analyzer_folder.data_type import DataType


class SymbolEnvironment:
    """Manages variable scopes and symbol lookups during semantic analysis."""
    def __init__(self, enclosing: Optional["SymbolEnvironment"] = None):
        self.__symbols: Dict[str, Symbol] = {}
        self.__enclosing = enclosing

    @property
    def enclosing(self) -> Optional["SymbolEnvironment"]:
        return self.__enclosing

    @property
    def symbols(self) -> Dict[str, Symbol]:
        return self.__symbols

    def define(self, name: str, type_name: Any, pos: SourcePosition) -> Symbol:
        """Declares a new symbol in the current scope."""
        if name in self.__symbols:
            raise SemanticError(f"Ang baryabol na '{name}' ay naideklara na sa sakop na ito.", pos)

        dt = type_name if isinstance(type_name, DataType) else DataType.from_name(str(type_name))
        sym = Symbol(name, dt, pos)
        self.__symbols[name] = sym
        return sym

    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        """Looks up a Symbol by name in the current and enclosing scopes."""
        if name in self.__symbols:
            return self.__symbols[name]
        if self.__enclosing:
            return self.__enclosing.lookup_symbol(name)
        return None

    def lookup(self, name: str) -> Optional[str]:
        """Looks up the type name of a symbol for backward compatibility."""
        sym = self.lookup_symbol(name)
        return sym.type_name if sym else None

    def contains_locally(self, name: str) -> bool:
        """Checks if a symbol is declared in the local scope."""
        return name in self.__symbols
