from abc import ABC, abstractmethod
from typing import Any, List


class OutputDevice(ABC):
    """
    Abstract interface for output handling (Strategy / Dependency Injection pattern).
    Allows decoupling the Interpreter from standard console printing.
    """
    @abstractmethod
    def write(self, value: Any) -> None:
        pass

    @abstractmethod
    def write_line(self, value: Any) -> None:
        pass


class ConsoleOutput(OutputDevice):
    """
    Standard output device that prints to the console.
    Formats booleans according to Peenoise grammar ('totoo'/'mali').
    """
    def write(self, value: Any) -> None:
        formatted = self.__format_value(value)
        print(formatted, end="")

    def write_line(self, value: Any) -> None:
        formatted = self.__format_value(value)
        print(formatted)

    def __format_value(self, value: Any) -> str:
        if isinstance(value, bool):
            return "totoo" if value else "mali"
        return str(value)


class BufferedOutput(OutputDevice):
    """
    In-memory output buffer, useful for testing and GUI integration.
    """
    def __init__(self):
        self.__buffer: List[str] = []

    def write(self, value: Any) -> None:
        formatted = "totoo" if (isinstance(value, bool) and value) else ("mali" if isinstance(value, bool) else str(value))
        self.__buffer.append(formatted)

    def write_line(self, value: Any) -> None:
        formatted = "totoo" if (isinstance(value, bool) and value) else ("mali" if isinstance(value, bool) else str(value))
        self.__buffer.append(formatted + "\n")

    def get_output(self) -> str:
        return "".join(self.__buffer)

    def clear(self) -> None:
        self.__buffer.clear()
