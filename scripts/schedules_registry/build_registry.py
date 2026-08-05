"""
Self-building schedule registry. Created 2026-06-02 by Claude Opus 4.8 for Max.
Last edited 2026-07-29 by Codex (GPT-5.6 SOL).

ONE script, runs on Pine. Pulls every scheduled job from every machine via SSH
(no per-machine collector to deploy), merges hand-written purpose annotations,
and writes ../schedules_registry_tomemex.md (git-synced + Memex-searchable).

Re-run any time and the doc is current -- it can't go stale because nobody
hand-types the schedules. The only hand-edited part is annotations.json
(what each job is FOR / is it a backup). Unknown jobs show "(unannotated)"
so a gap is visible, never silently dropped.

No silent fallbacks: if a machine is unreachable, its section says
"UNREACHABLE (ssh failed)" loudly rather than omitting it.
"""
import json
import re
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "schedules_registry_tomemex.md"
ANNOT = HERE / "annotations.json"

SSH = "ssh"
SSH_OPTS = ["-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=12",
            "-o", "BatchMode=yes"]
KEYS = Path.home() / ".ssh"

# Remote machines: (label, ssh_target, key_file, note)
REMOTES = [
    ("Lak", "mrempadmin@lakarian-city.ynh.fr", KEYS / "lakarian_key.pem",
     "home server (RempelServer), always-on, hosts Nextcloud + restic R2 backup repo"),
    ("Dax", "bitnami@35.80.203.42", KEYS / "dax_lightsail_max_id_rsa.pem",
     "AWS Lightsail, runs Memex pipeline + noeticus + clipfisher"),
    ("Sol", "maxre@192.168.1.113", KEYS / "sol_key",
     "local Ubuntu server (192.168.1.113)"),
]

# Pine task is "mine" (vs app noise) if its action command matches any of these.
PINE_INCLUDE = re.compile(
    r"(python|\.bat|\.ps1|\bgit\b|claude_base|cloud_base|\\moma\\|Nextcloud|notion|backup|memex)",
    re.IGNORECASE,
)


def cron_english(expr):
    """Best-effort gloss of a 5-field cron expr. Returns '' if unsure."""
    parts = expr.split()
    if len(parts) != 5:
        return ""
    mi, ho, dom, mon, dow = parts
    if expr == "* * * * *":
        return "every minute"
    m = re.fullmatch(r"\*/(\d+)", mi)
    if m and ho == dom == mon == dow == "*":
        return f"every {m.group(1)} min"
    m = re.fullmatch(r"\*/(\d+)", ho)
    if m and mi.isdigit() and dom == mon == dow == "*":
        return f"every {m.group(1)} h (at :{int(mi):02d})"
    if mi.isdigit() and ho.isdigit() and dom == mon == "*" and dow == "*":
        return f"daily {int(ho):02d}:{int(mi):02d}"
    if mi.isdigit() and ho.isdigit() and dom.isdigit() and mon == "*" and dow == "*":
        return f"monthly day {dom} {int(ho):02d}:{int(mi):02d}"
    if mi.isdigit() and ho == "*" and dom == mon == dow == "*":
        return f"hourly (at :{int(mi):02d})"
    return ""


def get_remote_cron(target, key):
    try:
        r = subprocess.run(
            [SSH, "-i", str(key), *SSH_OPTS, target,
             "crontab -l 2>/dev/null"],
            capture_output=True, text=True, timeout=30,
        )
    except Exception as e:
        return None, f"ssh exception: {e}"
    if r.returncode != 0 and not r.stdout.strip():
        return None, f"ssh rc={r.returncode}: {r.stderr.strip()[:200]}"
    jobs = []
    for line in r.stdout.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"^((?:\S+\s+){5})(.*)$", s)
        if not m:
            continue
        sched = m.group(1).strip()
        cmd = m.group(2).strip()
        jobs.append((sched, cmd))
    return jobs, None


def get_remote_systemd_timers(target, key):
    """Return user-level systemd timers when the remote exposes a user bus."""
    try:
        listed = subprocess.run(
            [SSH, "-i", str(key), *SSH_OPTS, target,
             "systemctl --user list-timers --all --no-pager --no-legend --output=json"],
            capture_output=True, text=True, timeout=30,
        )
    except Exception as e:
        return [], f"systemd timer query exception: {e}"
    if listed.returncode != 0:
        return [], None
    try:
        rows = json.loads(listed.stdout) if listed.stdout.strip() else []
    except json.JSONDecodeError as e:
        return [], f"systemd timer JSON error: {e}"
    jobs = []
    for row in rows:
        timer = row.get("unit", "")
        service = row.get("activates", "")
        if not timer or not service:
            continue
        detail = subprocess.run(
            [SSH, "-i", str(key), *SSH_OPTS, target,
             "systemctl --user show "
             f"{timer} -p TimersCalendar -p NextElapseUSecRealtime -p LastTriggerUSec; "
             "systemctl --user show "
             f"{service} -p ExecStart"],
            capture_output=True, text=True, timeout=30,
        )
        props = {}
        for line in detail.stdout.splitlines():
            if "=" in line:
                key_name, value = line.split("=", 1)
                props[key_name] = value
        jobs.append({
            "timer": timer,
            "service": service,
            "calendar": props.get("TimersCalendar", ""),
            "next": props.get("NextElapseUSecRealtime", ""),
            "last": props.get("LastTriggerUSec", ""),
            "command": props.get("ExecStart", ""),
        })
    return jobs, None


def get_pine_jobs():
    ps = (
        "$out=@(); "
        "Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\\Microsoft\\*' } | ForEach-Object { "
        "  $t=$_; $info=Get-ScheduledTaskInfo -TaskName $t.TaskName -TaskPath $t.TaskPath -ErrorAction SilentlyContinue; "
        "  $act=($t.Actions | ForEach-Object { (\"{0} {1}\" -f $_.Execute,$_.Arguments).Trim() }) -join ' ; '; "
        "  $trg=($t.Triggers | ForEach-Object { $_.CimClass.CimClassName }) -join ','; "
        "  $out += [pscustomobject]@{ name=$t.TaskName; state=[string]$t.State; action=$act; trigger=$trg; next=[string]$info.NextRunTime } "
        "}; $out | ConvertTo-Json -Depth 4"
    )
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, timeout=120)
        data = json.loads(r.stdout) if r.stdout.strip() else []
    except Exception as e:
        return None, f"powershell exception: {e}"
    if isinstance(data, dict):
        data = [data]
    jobs = []
    for d in data:
        act = (d.get("action") or "").strip()
        name = d.get("name") or ""
        if not PINE_INCLUDE.search(act + " " + name):
            continue
        jobs.append({
            "name": name, "state": d.get("state", ""),
            "action": act, "trigger": d.get("trigger", ""),
            "next": d.get("next", ""),
        })
    return jobs, None


def load_annotations():
    if ANNOT.exists():
        return json.loads(ANNOT.read_text(encoding="utf-8"))
    return {}


def annot_for(annotations, key):
    for k, v in annotations.items():
        if k and k in key:
            return v
    return "(unannotated)"


def main():
    annotations = load_annotations()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    L = []
    L.append("# Schedules registry - all crons & scheduled tasks")
    L.append("")
    L.append(f"AUTO-GENERATED {now} by scripts/schedules_registry/build_registry.py.")
    L.append("Do NOT hand-edit job rows -- they are pulled live from each machine via SSH.")
    L.append("To describe a job, add/edit its purpose in scripts/schedules_registry/annotations.json")
    L.append("(matched as a substring of the job command). Re-run the script to refresh.")
    L.append("")
    L.append("Legend: schedules shown as raw cron (min hour dom mon dow) with an English gloss where clear.")
    L.append("")

    # Pine
    L.append("## Pine (this laptop) - Windows Task Scheduler")
    L.append("")
    pine, err = get_pine_jobs()
    if err:
        L.append(f"**UNREACHABLE / ERROR:** {err}")
    elif not pine:
        L.append("_(no user scheduled tasks matched)_")
    else:
        for j in pine:
            purpose = annot_for(annotations, j["name"] + " " + j["action"])
            L.append(f"- **{j['name']}** -- {purpose}")
            L.append(f"  - runs: `{j['action']}`")
            extra = []
            if j["next"]:
                extra.append(f"next: {j['next']}")
            if j["state"]:
                extra.append(f"state: {j['state']}")
            if extra:
                L.append("  - " + ", ".join(extra))
    L.append("")

    # Remotes
    for label, target, key, note in REMOTES:
        L.append(f"## {label} - {note}")
        L.append(f"_{target}_")
        L.append("")
        if not key.exists():
            L.append(f"**UNREACHABLE:** ssh key missing ({key})")
            L.append("")
            continue
        jobs, err = get_remote_cron(target, key)
        if err:
            L.append(f"**UNREACHABLE (ssh failed):** {err}")
        elif not jobs:
            L.append("_(empty crontab)_")
        else:
            for sched, cmd in jobs:
                purpose = annot_for(annotations, cmd)
                gloss = cron_english(sched)
                gtxt = f"  ({gloss})" if gloss else ""
                L.append(f"- `{sched}`{gtxt} -- {purpose}")
                L.append(f"  - `{cmd}`")
        timers, timer_err = get_remote_systemd_timers(target, key)
        if timer_err:
            L.append(f"- **systemd timer scan warning:** {timer_err}")
        for timer in timers:
            purpose = annot_for(
                annotations,
                timer["timer"] + " " + timer["service"] + " " + timer["command"],
            )
            L.append(f"- **{timer['timer']}** (systemd user timer) -- {purpose}")
            if timer["calendar"]:
                L.append(f"  - schedule: `{timer['calendar']}`")
            if timer["next"]:
                L.append(f"  - next: {timer['next']}")
            L.append(f"  - activates: `{timer['service']}`")
            if timer["command"]:
                L.append(f"  - runs: `{timer['command']}`")
        L.append("")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
