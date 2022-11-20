# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Class for managing the XL-Connection and common read/write operations."""

from typing import Optional, Callable, Text, List
from contextlib import contextmanager
import os

import xlwings as xw

from NBDM.to_Excel import xl_data


# -----------------------------------------------------------------------------


class ReadRowsError(Exception):
    def __init__(self, row_start, row_end):
        self.msg = (
            f"Error: row_start should be less than row_end. Got {row_start}, {row_end}"
        )
        super().__init__(self.msg)


class NoActiveExcelRunningError(Exception):
    def __init__(self):
        self.msg = (
            "\n\tError: No active instance of Excel running?"
            "\n\tPlease open Excel and try again."
        )
        super().__init__(self.msg)


class ReadMultipleColumnsError(Exception):
    def __init__(self, _c1, _c2):
        self.msg = (
            f'\n\tError: Cannot use "read_multiple_columns()" with _col_start={_c1}'
            f'and _col_end={_c2}. Please use "read_single_column()" instead.'
        )
        super().__init__(self.msg)


class WriteValueError(Exception):
    def __init__(self, _value, _range, _worksheet, _e):
        self.msg = (
            "\n\n\tSomething went wrong trying to write the value: '{}' to the cell: '{}' on worksheet: '{}'. Please "
            "make sure that a valid PHPP file is open, and both the worksheet and workbook are unprotected.\n\n{}".format(
                _value, _range, _worksheet, _e
            )
        )
        super().__init__(self.msg)


# -----------------------------------------------------------------------------


class XLConnection:
    def __init__(self, _output: Optional[Callable] = None) -> None:
        """Facade class for Excel Interop

        Arguments:
        ----------
            * _output: Optional[Callable]: The output functions to use. Input None for silent.
        """

        self._output = _output

    def output(self, _input: Text) -> None:
        """Used to set the output method. Default is None (silent).

        Arguments:
        ----------
            * _input (typing.Text): The string to output.

        Returns:
        --------
            * None
        """
        try:
            self._output(str(_input))  # type: ignore
        except:
            # If _input=None, ignore...
            pass

    @property
    def wb(self) -> xw.main.Book:
        try:
            return xw.books.active
        except:
            raise NoActiveExcelRunningError

    @contextmanager
    def in_silent_mode(self):
        """Context Manager which turns off screen-refresh and auto-calc in the
        Excel App in order to help speed up read/write. Turns back on screen-refresh
        and auto-calc in the Excel App when done or on any error.
        """
        try:
            self.wb.app.screen_updating = False
            self.wb.app.display_alerts = False
            self.wb.app.calculation = "manual"
            yield
        finally:
            self.wb.app.screen_updating = True
            self.wb.app.display_alerts = True
            self.wb.app.calculation = "automatic"
            self.wb.app.calculate()

    def connection_is_open(self) -> bool:
        if not self.wb:
            return False
        return True

    def unprotect_all_sheets(self) -> None:
        """Walk through all the sheets and unprotect them all."""
        for sheet in self.wb.sheets:
            if os.name != "nt":
                sheet.api.unprotect()
            else:
                sheet.api.Unprotect()

    def create_new_worksheet(self, _sheet_name: str) -> None:
        """Try and add a new Worksheet to the Workbook."""
        try:
            self.wb.sheets.add(_sheet_name)
            print(f"Adding '{_sheet_name}' to Workbook")
        except ValueError:
            print(f"Worksheet '{_sheet_name}' already in Workbook.")

        self.get_sheet_by_name(_sheet_name).clear()

    def get_sheet_by_name(self, _sheet_name: str) -> xw.main.Sheet:
        """Returns an Excel Sheet with the specified name, or KeyError if not found.

        Arguments:
        ----------
            * _sheet_name: (str): The excel sheet name to locate.

        Returns:
        --------
            * (xw.main.Sheet): The excel sheet found.
        """
        return self.wb.sheets[_sheet_name]

    def write_xl_item(self, _xl_item: xl_data.XlItem) -> None:
        """Writes a single XLItem to the worksheet

        Arguments:
        ---------
            * _xl_item: (XLItem) The XLItem with a sheet_name, range and value to write.
        """

        try:
            self.output(
                f"{_xl_item.sheet_name}:{_xl_item.xl_range}={_xl_item.write_value}"
            )
            xl_sheet = self.get_sheet_by_name(_xl_item.sheet_name)
            xl_range = xl_sheet.range(_xl_item.xl_range)
            xl_range.value = _xl_item.write_value

            if isinstance(_xl_item.write_value, List):
                # -- If its a list, color the entire width (all columns)
                for i in range(len(_xl_item.write_value)):
                    _xl_range = xl_range.offset(column_offset=i)
                    _xl_range.color = _xl_item.range_color
                    _xl_range.font.color = _xl_item.font_color
            else:
                xl_range.color = _xl_item.range_color
                xl_range.font.color = _xl_item.font_color

        except Exception as e:
            raise WriteValueError(
                _xl_item.write_value, _xl_item.xl_range, _xl_item.sheet_name, e
            )
