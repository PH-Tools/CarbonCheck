from abc import ABC, abstractmethod


class PDFSectionType(ABC):
    """Abstract base class for all PDF Section classes."""

    def __init__(self) -> None:
        self._lines = []

    @abstractmethod
    def add_line(self, _line: str) -> None:
        ...

    @abstractmethod
    def process_section_text(self) -> None:
        ...
