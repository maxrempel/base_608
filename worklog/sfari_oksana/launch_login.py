import sys
import traceback

sys.path.insert(0, r"C:\claude_base\tools\codex_access\scripts")
import bw_auto  # noqa: E402

LOGIN_SCRIPT = r"C:\claude_base\worklog\sfari_oksana\login_oksana.py"
RC_FILE = r"C:\claude_base\worklog\sfari_oksana\launcher_rc.txt"
ERR_FILE = r"C:\claude_base\worklog\sfari_oksana\launcher_error.txt"
START_FILE = r"C:\claude_base\worklog\sfari_oksana\launcher_started.txt"

with open(START_FILE, "w", encoding="utf-8") as f:
    f.write("launcher started\n")

try:
    rc = bw_auto.command_exec(
        "Oksana 20260805 base.sfari.org",
        ["pythonw", LOGIN_SCRIPT],
        "LOGIN_USERNAME",
        "LOGIN_PASSWORD",
        None,
    )
    with open(RC_FILE, "w", encoding="utf-8") as f:
        f.write("rc=" + str(rc) + "\n")
except Exception:
    with open(ERR_FILE, "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())
