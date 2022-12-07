# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Class for managing the XL-Connection and common read/write operations."""

from typing import Optional, Callable, Text, List, Any
from contextlib import contextmanager
import os

from NBDM.Excel import xl_data
from NBDM.Excel.xl_typing import (
    xl_Framework_Protocol,
    xl_Book_Protocol,
    xl_Sheet_Protocol,
)

# -----------------------------------------------------------------------------
# -- Exceptions


class ReadRowsError(Exception):
    def __init__(self, row_start, row_end):
        self.msg = (
            f"Error: row_start should be less than "
            f"row_end. Got {row_start}, {row_end}"
        )
        super().__init__(self.msg)


class NoActiveExcelRunningError(Exception):
    def __init__(self):
        self.msg = (
            "\n\tError: No active instance of Excel running?"
            "\n\tPlease open"
            "Excel and try again."
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
            f"\n\n\tSomething went wrong trying to write the value: '{_value}' to the "
            f"cell: '{_range}' on worksheet: '{_worksheet}'. Please make sure that a "
            f"valid Excel file is open, and both the worksheet and workbook are "
            f"unprotected.\n\n{_e}"
        )
        super().__init__(self.msg)


# -----------------------------------------------------------------------------
def silent_print(_input: Any) -> None:
    """Default 'output' for XLConnection."""
    return


class XLConnection:
    def __init__(
        self, xl_framework, output: Callable[[Any], None] = silent_print
    ) -> None:
        """Facade class for Excel Interop.

        Arguments:
        ----------
            * xl (xl_Framework_Protocol): The Excel framework to use to interact with XL.
            * _output (Callable[[Any], None]): The output function to use.
                Default is silent (no output), or provide 'print' for standard-out, etc.
        """
        # -- Note: can not type-hint xl_framework in the Class argument line
        # -- cus' Python-3.7 doesn't have Protocols yet. It does see to work
        # -- when type-hinting the actual attribute though.
        self.xl: xl_Framework_Protocol = xl_framework
        self._output = output

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
    def wb(self) -> xl_Book_Protocol:
        """Return the active XL Workbook, or raise NoActiveExcelRunningError."""
        try:
            return self.xl.books.active
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
            self.output(f"Adding '{_sheet_name}' to Workbook")
        except ValueError:
            self.output(f"Worksheet '{_sheet_name}' already in Workbook.")

        self.get_sheet_by_name(_sheet_name).clear()

    def get_sheet_by_name(self, _sheet_name: str) -> xl_Sheet_Protocol:
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
        except AttributeError as e:
            raise AttributeError(e)
        except Exception as e:
            raise WriteValueError(
                _xl_item.write_value, _xl_item.xl_range, _xl_item.sheet_name, e
            )
