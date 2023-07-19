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
    from CC_GUI.cc_app_config import (
        find_log_file_path,
        remove_old_log_files,
        find_resources_path,
    )
except Exception as e:
    raise Exception("Error importing App library?", e)

if __name__ == "__main__":
    # -- When using cx_Freeze to create the .exe file, it will set
    # -- stdout to 'None' which causes all sorts of trouble. So wrap
    # -- the execution here in a file object to redirect the stdout
    # -- so we can avoid any errors or failures.
    log_file_path = find_log_file_path()
    remove_old_log_files(log_file_path)
    resources_path = find_resources_path()
    error_log_path = log_file_path / "stdout.log"
    with open(error_log_path, "w") as f:
        sys.stdout = f
        # -- Run the App
        try:
            app = CCApp(output_format, log_file_path, resources_path, sys.argv)
            app.view.show()
            sys.exit(app.exec())
        except Exception as e:
            raise Exception("Error running App?", e)
