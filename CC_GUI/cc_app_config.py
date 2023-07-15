# -*- Python Version: 3.11 -*-

"""Configuration Utilities."""

import logging
import logging.config
import os
import pathlib
import sys
import traceback
from types import TracebackType
from typing import Optional, Any


def find_application_path() -> pathlib.Path:
    """Returns the path to the application root location.

    The 'application' will be located and run from different places, depending on the OS and
    whether it is run as an 'app' or run as a 'script'.
    If the application is run as a frozen bundle, the PyInstaller boot-loader
    extends the sys module by a flag 'frozen=True' and sets the __file__ path into variable '_MEIPASS'.

    For instance:

    As App (sys.frozen==True):
    ----
        MacOS:
        - sys.executable            = '/Users/em/Dropbox/bldgtyp/2209_Nash_Home/12_Scripts/dist/app'
        - os.path.abspath(__file__) = '/var/folders/vm/rkn0g153d2tph6hz8r00000gn/T/_MEIh08vPN/app.py'
        - sys._MEIPASS              = '/var/folders/vm/rkn0g153d2tph6hz8r00000gn/T/_MEI1fU4xe'

        Windows:
        - sys.executable            = '\\\\Mac\\Dropbox\\bldgtyp\\2209_Nash_Home\\12_Scripts\\dist\\app.exe'
        - os.path.abspath(__file__) = 'C:\\Users\\em\\AppData\\Local\\Temp\\_MEI34162\\app.py'
        - sys._MEIPASS              = 'C:\\Users\\em\\AppData\\Local\\Temp\\_MEI34162'

    As Script (ie: from inside VSCode or from the Terminal while testing)
    ------
        MacOS:
        - sys.executable            = '/Users/em/Dropbox/bldgtyp/2209_Nash_Home/12_Scripts/venv/bin/python'
        - os.path.abspath(__file__) = '/Users/em/Dropbox/bldgtyp/2209_Nash_Home/12_Scripts/app.py'
        - sys._MEIPASS              = None (does not exist)

        Windows:
        - sys.executable            = '\\\\mac\\Dropbox\\bldgtyp\\2209_Nash_Home\\12_Scripts\\venv\\Scripts\\python.exe'
        - os.path.abspath(__file__) = '\\\\mac\\Dropbox\\bldgtyp\\2209_Nash_Home\\12_Scripts\\app.py'
        - sys._MEIPASS              = None (does not exist)

    So, if its a script, use __file__, but if its an 'app', use sys.executable for the app location.
    """

    def _app_is_run_as_frozen_app() -> bool:
        """Return True if the app is run as a frozen app, False if not."""
        return getattr(sys, "frozen", False)

    # -- return the PARENT of the app's location as the application root
    if _app_is_run_as_frozen_app():
        return pathlib.Path(sys.executable).parent
    else:
        return pathlib.Path(os.path.abspath(__file__)).parent


def find_log_file_path() -> pathlib.Path:
    """Returns the path to the application log file location."""
    log_file_path = find_application_path() / "Logs"

    if not log_file_path.exists():
        os.makedirs(log_file_path)

    return log_file_path


def remove_old_log_files(_log_file_path: pathlib.Path) -> None:
    """Remove old log files from the log file path."""
    if _log_file_path.exists():
        for file in _log_file_path.glob("*.log"):
            file.unlink()


def find_resources_path() -> pathlib.Path:
    """Returns the path to the application log file location."""
    return find_application_path() / "resources"


def add_logging_level(levelName, levelNum, methodName=None):
    """Utility function to add a new logging level to the logging module."""
    # Adopted from https://stackoverflow.com/a/35804945/1691778
    # Adds a new logging method to the logging module
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError("{} already defined in logging module".format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError("{} already defined in logging module".format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError("{} already defined in logger class".format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def log_exception(
    exc_type: type[BaseException], value: BaseException, tb: Optional[TracebackType]
) -> Any:
    """Log an exception to the error_log.txt file.

    This is needed when using cx_Freeze to create an executable since it
    seems to set sys.stdout to None by default? That causes problems, so this
    is used as s fallback.
    """
    log_path = find_log_file_path()
    error_file = pathlib.Path(log_path, "ERROR.log")
    with open(error_file, "w") as f:
        traceback.print_exception(exc_type, value, tb, file=f)
