# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Project Data"""

from typing import Any, List, Optional


class WufiPDF_BuildingAddress:
    def __init__(self):
        self.name: str = "-"
        self.building_number: str = "-"
        self.street: str = "-"
        self.locality: str = "-"
        self.state: str = "-"
        self.postal_code: str = "-"
        self.country: str = "-"

    def __setattr__(self, __name: str, __value: Any) -> None:
        if "name" in __name:
            self.__dict__["name"] = __value
        else:
            self.__dict__[__name] = __value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({[f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')]})"


class WufiPDF_ProjectData:
    __pdf_heading_string__ = "Project data"
    get_tables = True

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self.client = WufiPDF_BuildingAddress()
        self.building = WufiPDF_BuildingAddress()
        self.owner = WufiPDF_BuildingAddress()
        self.responsible = WufiPDF_BuildingAddress()

    def section(self, _key: str) -> Optional[str]:
        """Return the section object (client, building, owner, responsible) for the given key."""
        return getattr(self, _key.lower(), None)

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """Clean and organize all of the PDF data found."""
        for table in self._tables:
            section = None

            for row in table:
                # -- Change to the right section
                if section_marker := self.section(row[0]):
                    section = section_marker
                else:
                    # -- Add the data to the section
                    attr_name, attr_value = row
                    if section and attr_name and attr_value:
                        setattr(
                            section,
                            attr_name.lower().replace(" ", "_").strip(),
                            attr_value,
                        )
