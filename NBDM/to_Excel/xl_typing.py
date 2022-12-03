# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""XL-App Protocol Classes."""

from typing import Optional, Callable, Tuple

from NBDM.to_Excel import xl_data


class xl_API_Protocol:
    def __init__(self):
        self.unprotect: Callable
        self.Unprotect: Callable


class xl_app_Protocol:
    def __init__(self):
        self.screen_updating: bool
        self.display_alerts: bool
        self.calculation: str
        self.calculate: Callable


class xl_Range_Protocol:
    def __init__(self):
        self.value: xl_data.xl_writable
        self.color: Optional[Tuple[int, ...]]
        self.font: ...

    def offset(
        self, row_offset: int = 0, column_offset: int = 0
    ) -> "xl_Range_Protocol":
        ...


class xl_Sheet_Protocol:
    def __init__(self):
        self.api: xl_API_Protocol
        self.clear: Callable

    def range(self, cell1, cell2=None) -> xl_Range_Protocol:
        ...


class xl_Sheets_Protocol:
    def __init__(self):
        ...

    def __getitem__(self, _key) -> xl_Sheet_Protocol:
        ...

    def add(
        self,
        name: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> xl_Sheet_Protocol:
        ...


class xl_Book_Protocol:
    def __init__(self):
        self.app: xl_app_Protocol
        self.sheets: xl_Sheets_Protocol


class xl_Books_Protocol:
    def __init__(self):
        self.active: xl_Book_Protocol


class xl_Framework_Protocol:
    def __init__(self):
        self.books: xl_Books_Protocol
