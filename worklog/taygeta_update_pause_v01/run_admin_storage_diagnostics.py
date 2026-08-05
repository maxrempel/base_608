import runpy
import traceback
from pathlib import Path


log = Path(__file__).with_name("admin_storage_diagnostics_launcher.txt")
try:
    runpy.run_path(
        str(Path(__file__).with_name("admin_storage_diagnostics.py")),
        run_name="__main__",
    )
    log.write_text("completed\n", encoding="utf-8")
except BaseException:
    log.write_text(traceback.format_exc(), encoding="utf-8")
    raise
