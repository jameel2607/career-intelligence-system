import sys
import os
import traceback

sys.path.append(os.getcwd())

try:
    from app import main
    print("Import successful!")
except Exception:
    with open("import_error.log", "w") as f:
        traceback.print_exc(file=f)
