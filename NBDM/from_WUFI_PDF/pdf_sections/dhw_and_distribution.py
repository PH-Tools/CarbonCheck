class DHWandDistribution:
    __pdf_heading_string__ = "DHW AND DISTRIBUTION"

    def __init__(self) -> None:
        self._lines = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def process_section_text(self) -> None:
        pass
