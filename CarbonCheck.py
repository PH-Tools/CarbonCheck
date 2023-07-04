# -*- Python Version: 3.10 -*-

"""Run to see GUI."""

import logging
import sys

try:
    from NBDM.model import output_format
except Exception as e:
    raise Exception("Error importing NBDM library?", e)

try:
    from CC_GUI.cc_app import CCApp
    from CC_GUI.cc_app_config import find_log_file_path, find_stylesheet_path
except Exception as e:
    raise Exception("Error importing App library?", e)

if __name__ == "__main__":
    # -- When using cx_Freeze to create the .exe file, it will set
    # -- stdout to 'None' which causes all sorts of trouble. So wrap
    # -- the execution here in a file object to redirect the stdout
    # -- so we can avoid any errors or failures.
    log_file_path = find_log_file_path()
    error_log_path = log_file_path / "stdout.log"
    stylesheet_path = find_stylesheet_path()
    with open(error_log_path, "w") as f:
        sys.stdout = f

        # -- Run the App
        app = CCApp(output_format, stylesheet_path, log_file_path, sys.argv)
        app.view.show()
        sys.exit(app.exec())
