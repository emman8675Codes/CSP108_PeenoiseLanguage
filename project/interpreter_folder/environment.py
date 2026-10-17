from typing import Optional, Dict, Any
from lexer_folder.token import Token
from interpreter_folder.runtime_error import RuntimeError_


class Environment:
    """
    Represents the runtime environment and memory scope for variables.
    Supports nested scopes and scope chaining.
    """
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.__values: Dict[str, Any] = {}
        self.__enclosing = enclosing

    @property
    def values(self) -> Dict[str, Any]:
        """Returns the internal dictionary for reading or backward compatibility."""
        return self.__values

    @property
    def enclosing(self) -> Optional["Environment"]:
        return self.__enclosing

    def define(self, name: str, value: Any) -> None:
        """Declares or defines a variable in the current local scope."""
        self.__values[name] = value

    def assign(self, name_token: Token, value: Any) -> None:
        """Assigns a new value to an existing variable in the scope chain."""
        name = name_token.lexeme
        if name in self.__values:
            self.__values[name] = value
            return
        if self.__enclosing is not None:
            self.__enclosing.assign(name_token, value)
            return
        raise RuntimeError_(f"Hindi nahanap ang baryabol na '{name}'.", name_token.position)

    def get(self, name_token: Token) -> Any:
        """Retrieves the value of a variable from the current or parent scope."""
        name = name_token.lexeme
        if name in self.__values:
            return self.__values[name]
        if self.__enclosing is not None:
            return self.__enclosing.get(name_token)
        raise RuntimeError_(f"Hindi pa naitatala ang halaga ng '{name}'.", name_token.position)

    def contains(self, name: str) -> bool:
        """Checks if a variable exists in the local or enclosing scopes."""
        if name in self.__values:
            return True
        if self.__enclosing is not None:
            return self.__enclosing.contains(name)
        return False
