## 1. Root-Cause Assessment

1. **Safety watcher false Git-loss pages**  
   The watcher judges "uncommitted deletion" solely from working-tree state (`git ls-files --deleted`) but does not verify that the missing file actually exists in the current HEAD commit (`git cat-file -e HEAD:<path>`). The judge then produces a Telegram alarm even though Git history retains all content. Annotating `git ls-tree` output does not prevent escalation because the judge logic evaluates the *danger* before the annotation is consulted.

2. **Expense digest cadence**  
   The `.timer` unit runs at 00:00,06:00,12:00,18:00 Pacific. The Python script (`ds_ledger.py`) and its README mention "four times daily". The urgent low-balance and spend-threshold alerts are implemented via independent polling inside the script (every 15 minutes) and are not tied to the timer cadence. The Healthchecks liveness ping is also decoupled (runs inside the AWS polling loop).

3. **Clipfisher classification**  
   The bot delivers user-requested results, not infrastructure alarms. It currently appears in the default alert aggregation (`tg_alerts.py` trouble view), causing noise – but its messages are not actionable errors. Removing it from the default view without altering its delivery is the correct denoise.

## 2. Minimal Patch Design

### 2a. Safety watcher false Git-loss guard

In `safety_watcher.py`, after computing the set of deleted working-tree files (from `git ls-files --deleted`) but **before** running the judge that fires Telegram, insert:

```python
# Guard: suppress escalation if every declared "missing" file exists in HEAD.
if deletion_only and all(git.exists_in_head(path) for path in del_paths):
    logger.info("Suppress false loss alarm: all deleted files are committed in HEAD.")
    return   # or skip the escalation path
```

`git.exists_in_head(path)` is a helper that runs `git cat-file -e HEAD:<path>` (returns True if object exists). The guard must check `deletion_only` – that the alarm’s stated danger is exclusively file deletion (not force‑push, repo deletion, etc.). The existing `DangerProfile` enum or a similar boolean in the alarm object should contain that flag; if not, add it.

### 2b. Expense digest cadence

- **`.timer` file**: change `OnCalendar=*-*-* 00:00,06:00,12:00:00` to `OnCalendar=*-*-* 09:00:00`.
- **`ds_ledger.py`**: update docstring / comment that says "four times daily" to "once daily at 09:00 Pacific".
- **`README_tomemex.md`**: replace "four times daily Telegram" with "once daily at 09:00 Pacific".
- **AWS polling loop**: remains at 15‑minute interval (four times an hour) – no change needed.
- **Healthchecks**: no change; it sends a ping on each AWS poll.

### 2c. Clipfisher classification

In `tg_alerts.py` (the trouble view), modify the `if` or filter that collects messages for display to:

```python
if not bot_name.startswith("clipfisher") or config.INCLUDE_CLIPFISHER:
    messages.add(bot_output)
```

Default `INCLUDE_CLIPFISHER = False`. This keeps the bot delivering transcripts exactly as before, but excludes them from the aggregated trouble view unless explicitly enabled.

## 3. Concrete Test Cases

### 3a. Safety watcher guard

| Test | Setup | Expected outcome |
|------|-------|------------------|
| Deleted file in HEAD | `git rm` a committed file, run watcher | No Telegram alarm; log line appears |
| Deleted file not in HEAD | `git rm` a file never committed | Telegram alarm fires |
| Deleted file + force push indicator | Set danger flag `force_push=True`, include deleted committed file | Guard skips (because `deletion_only` is false), alarm fires |
| File present but dirty working tree | File deleted but also modified in HEAD? Not possible – assume file exists in HEAD | Guard passes, no alarm |
| Multiple deleted, all in HEAD | Two committed files deleted | No alarm |
| One deleted in HEAD, one not | Mixed set | Alarm fires (only the truly unrecoverable one is valid, but alarm still sent – acceptable) |

### 3b. Expense digest cadence

| Test | What to check | Method |
|------|---------------|--------|
| Timer activates only at 09:00 | `systemctl list-timers` | After applying `.timer` change, wait for next trigger. Also inspect `.timer` unit `OnCalendar` value. |
| Script runs at 09:00 | Log `Time: 09:00` in journal | Trigger manually with `systemctl start ds_ledger.service` and check log |
| Low-balance alarm still fires | Set dummy low balance, ensure Telegram is sent outside 09:00 | Manually trigger the Python script’s polling function |
| AWS polling runs independently | Watch job log for 15‑minute intervals | Let the service run for an hour |
| README mentions old cadence | Grep for "four times" in README | After patch, grep should find only "once daily" or none |

### 3c. Clipfisher classification

| Test | Setup | Expected outcome |
|------|-------|------------------|
| Default config (no explicit flag) | Bot sends transcript; trouble view aggregates | Transcript delivered; not shown in trouble view |
| Explicit flag `INCLUDE_CLIPFISHER = True` | Same | Transcript delivered and shown in trouble view |
| Bot goes offline | Bot crashes | Alert still sent via other monitors? This is not about delivery, just view. The monitor bot itself is part of delivery – if it fails, that is an infrastructure alarm. Leave that unchanged. |

## 4. Deployment and Rollback Checklist

### 4a. Safety watcher guard
- **Deploy**: Commit patch to `safety_watcher.py`. Deploy as part of next normal release. No config change.
- **Rollback**: Git revert that commit. No data loss.
- **Verify**: Watch Telegram for 24 hours for any false suppression. If real danger is suppressed (e.g., because `git cat-file -e` returns True even after a force push that rewrote history?), the guard only protects when `deletion_only` is true and all files are in HEAD. If a force push happens, `deletion_only` will be false, so guard will not suppress. Rollback only if a real alarm is incorrectly blocked.

### 4b. Expense digest cadence
- **Deploy**:  
  1. Edit `.timer` file, run `systemctl daemon-reload && systemctl restart ds_ledger.timer`.  
  2. Update Python docstring and README.  
- **Rollback**:  
  1. Restore old `.timer` (git checkout).  
  2. `systemctl daemon-reload && systemctl restart ds_ledger.timer`  
  3. Revert doc/README changes.  
- **Sanity**: After deploy, list timers (`systemctl list-timers`) to confirm next trigger is 09:00 Pacific.

### 4c. Clipfisher classification
- **Deploy**: Change default value of `INCLUDE_CLIPFISHER` in config file or environment. Restart Telegram alert aggregator.
- **Rollback**: Set `INCLUDE_CLIPFISHER = True` (old behaviour) and restart.
- **No impact** on delivery – bot continues without interruption.

## 5. Safety Concerns That Should Block Implementation

- **Safety watcher guard**  
  The guard assumes `git cat-file -e HEAD:<path>` is a reliable indicator of recoverability. It is – for a normal repository. However, if the repository is a shallow clone, `cat-file` may fail even though the object exists in a wider fetch. This is unlikely for a production AWS‑backed repo. Consider adding a shallow‑clone check or treating error from `cat-file` as "not sure" and falling back to alarm. For now, low risk.  
  Another edge: a file could be deleted from working tree *and* removed from HEAD via a previous commit (not in this commit). `git cat-file -e HEAD:<path>` would then be False, alarm fires correctly. No block.

- **Expense digest cadence**  
  If the timer service is masked or overridden by another system control, the change could silently fail to activate. The checklist step to list timers mitigates this. No safety block.

- **Clipfisher classification**  
  No safety block. Changing the view does not affect delivery. However, ensure that the monitoring of the clipfisher bot itself (e.g., healthcheck) remains in the trouble view – that is an infrastructure alarm. The current design only filters messages that the bot *sends*, not its own health. If the bot fails to send, that will be caught elsewhere (e.g., Healthchecks). No block.

**None of the three changes present a blocking safety concern.** The guard in (1) has a minor edge case, but it is acceptable given the reproducibility of false alarms. All changes can be rolled back within one minute.
