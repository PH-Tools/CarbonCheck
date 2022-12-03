import pytest

from NBDM.to_Excel import xl_app, xl_data
from NBDM.to_Excel import xl_typing


# -- Mock XL Framework --------------------------------------------------------


class Mock_XL_Framework(xl_typing.xl_Framework_Protocol):
    def __init__(self):
        self.books = xl_typing.xl_Books_Protocol()
        self.books.active.sheets.storage = {
            "Sheet1": xl_typing.xl_Sheet_Protocol(),
            "Sheet2": xl_typing.xl_Sheet_Protocol(),
        }


# -----------------------------------------------------------------------------


def test_xl_app_default():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)
    assert app


# -----------------------------------------------------------------------------
# Workbook


def test_xl_app_get_WorkBook_success():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)
    assert app.wb


def test_xl_app_get_WorkBook_fail():
    mock_xw = Mock_XL_Framework()

    mock_xw.books = None  # type: ignore #<---------

    app = xl_app.XLConnection(xl_framework=mock_xw)

    with pytest.raises(xl_app.NoActiveExcelRunningError):
        assert app.wb


# -----------------------------------------------------------------------------
# App / Sheet Operations


def test_xl_app_silent_mode():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)
    assert app.wb.app.screen_updating == True
    assert app.wb.app.display_alerts == True
    assert app.wb.app.calculation == "automatic"

    with app.in_silent_mode():
        assert app.wb.app.screen_updating == False
        assert app.wb.app.display_alerts == False
        assert app.wb.app.calculation == "manual"

    assert app.wb.app.screen_updating == True
    assert app.wb.app.display_alerts == True
    assert app.wb.app.calculation == "automatic"


def test_xl_app_unprotect_all_sheets():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)

    for sheet in app.wb.sheets:
        assert sheet.protected == True

    app.unprotect_all_sheets()

    for sheet in app.wb.sheets:
        assert sheet.protected == False


def test_xl_app_create_new_worksheet():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)

    new_sheet_name = "A Test Worksheet"
    assert new_sheet_name not in app.wb.sheets

    app.create_new_worksheet(new_sheet_name)
    assert new_sheet_name in app.wb.sheets


def test_xl_app_create_new_worksheet_already_in_raises_ValueError():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)

    new_sheet_name = "A Test Worksheet"
    assert new_sheet_name not in app.wb.sheets
    assert len(app.wb.sheets) == 2

    app.create_new_worksheet(new_sheet_name)
    app.create_new_worksheet(new_sheet_name)  # Add again
    app.create_new_worksheet(new_sheet_name)  # Add again
    assert new_sheet_name in app.wb.sheets
    assert len(app.wb.sheets) == 3  # only added the sheet once


def test_xl_app_get_sheet_by_name():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)

    assert app.get_sheet_by_name("Sheet1") is not None

    with pytest.raises(KeyError):
        app.get_sheet_by_name("Not a Name")


# -----------------------------------------------------------------------------
# Writing


def test_xl_app_write_simple_value():
    mock_xw = Mock_XL_Framework()
    app = xl_app.XLConnection(xl_framework=mock_xw)

    xl_item = xl_data.XlItem("Sheet1", "A1", 1)
    app.write_xl_item(xl_item)
