# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""XL-App Protocol Behavior Classes."""

from typing import Optional, Dict, Tuple

from NBDM.to_Excel import xl_data


class xl_app_Protocol:
    def __init__(self):
        self.screen_updating: bool = True
        self.display_alerts: bool = True
        self.calculation: str = "automatic"

    def calculate(self) -> None:
        return None


class xl_Range_Protocol:
    def __init__(self):
        self.value: xl_data.xl_writable
        self.color: Optional[Tuple[int, ...]]
        self.font: ...

    def offset(self, row_offset: int = 0, column_offset: int = 0) -> "xl_Range_Protocol":
        return xl_Range_Protocol()


class xl_API_Protocol:
    def __init__(self, sheet):
        self.sheet: "xl_Sheet_Protocol" = sheet

    def unprotect(self):
        self.sheet.protected = False

    def Unprotect(self):
        self.sheet.protected = False


class xl_Sheet_Protocol:
    def __init__(self):
        self.api = xl_API_Protocol(self)
        self.protected = True

    def clear(self) -> None:
        return None

    def range(self, cell1, cell2=None) -> xl_Range_Protocol:
        return xl_Range_Protocol()


class xl_Sheets_Protocol:
    def __init__(self):
        self.storage: Dict[str, xl_Sheet_Protocol] = {}

    def __getitem__(self, _key) -> xl_Sheet_Protocol:
        return self.storage[_key]

    def add(
        self,
        name: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> xl_Sheet_Protocol:
        if name in self.storage.keys():
            raise ValueError
        else:
            new_sheet = xl_Sheet_Protocol()
            self.storage[str(name)] = new_sheet
            return new_sheet

    def __iter__(self):
        for _ in self.storage.values():
            yield _

    def __contains__(self, key):
        return key in self.storage

    def __len__(self):
        return len(self.storage)


class xl_Book_Protocol:
    def __init__(self):
        self.app = xl_app_Protocol()
        self.sheets = xl_Sheets_Protocol()


class xl_Books_Protocol:
    def __init__(self):
        self.active = xl_Book_Protocol()


class xl_Framework_Protocol:
    def __init__(self):
        self.books = xl_Books_Protocol()
