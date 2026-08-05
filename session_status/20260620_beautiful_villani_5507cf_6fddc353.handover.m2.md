# Scribe handover - milestone 2 (~154K tokens)
# session: 20260620_beautiful_villani_5507cf_6fddc353
# cwd: C:\claude_base\.claude\worktrees\beautiful-villani-5507cf
# written: 2026-06-20 11:52:56 by deepseek-v4-pro

# HANDOVER - cross-machine Claude Code comms (fleetcomm)

## GOAL (Max's words)

Max wanted a way for Claude Code sessions on Pine to talk to Claude Code sessions on Centauri - "occasional, but I need a communication channel, similar to teams." He explicitly chose the durable Cloudflare option over Nextcloud sync.

The session built that channel, proved it works both directions, and ended with Max saying **"ok, talk to mike in dc session on centauri"** - meaning the immediate next action is to use fleetcomm to send a message to Mike (the Claude session on Centauri).

## DECISIONS MADE + WHY

1. **Build, don't reuse the wall.** The existing `claude-wall` Cloudflare worker already reached both machines, but auto-deletes messages after 30 minutes - wrong for occasional async use. Rather than modify the live wall (risk), built a separate worker.

2. **Cloudflare KV-backed worker (`fleetcomm`).** Chosen over Nextcloud sync (Max: "surely B, A is flaky, unreliable, slow"). KV is eventually-consistent but durable (~30 days TTL), globally reachable, and uses existing Cloudflare credentials.

3. **Weak shared key for posting.** Anyone with the key can post (reads are unauthenticated by design - low stakes). Deliberately not secrets-safe; messages are plain text on a public-ish endpoint.

4. **Machine auto-tagging.** CLI stamps `Pine` or `Centauri` via environment variable so messages show origin.

5. **Cursor-based "read new only".** Stored in a local JSON file so each read shows only messages since last read, with `--all` fallback.

6. **No auto-hear hook built.** Max didn't ask for it, and it adds a network call every prompt turn. Left as optional upgrade.

7. **Claude sessions auto-discover fleetcomm.** Centauri's `~/.claude/CLAUDE.md` is a symlink to the **same synced `global_CLAUDE.md`** Pine uses (via Nextcloud). global2.md already contains the fleetcomm pointer - synced down to Centauri. So fresh sessions on either machine know it exists without pasting.

## CURRENT STATE

- **Worker deployed:** `https://fleetcomm.max-rempel2.workers.dev` (Cloudflare KV namespace `4639fd2da50044a09ec5bb42ecc97247`), ~30-day message TTL, key `fleetcomm_claymem2026`
- **CLI tool** at canonical path on **both** machines: `C:/claude_base/tools/fleetcomm/fleetcomm.py`
  - Pine: git repo at `C:/claude_base` (master, pushed)
  - Centauri: git repo at `C:/claude_base` (can't git-pull - no GitHub creds non-interactively; files were manually copied to canonical path)
  - Stray `C:\fleetcomm` copy on Centauri was deleted
- **Round-trip proven:** Pine posted ? Centauri read it; Centauri posted ("Centauri session online, hearing you") ? Pine read it. Both directions confirmed.
- **Credentials:** Cloudflare API token `ZUyIUYjo_6w53JHSBfGmw1Tei9XgBBNsnpKTMR2b` (Workers-scoped), account `e4dc2224d6baa721873dca77dc6f057d`
- **global2 entry** has the fleetcomm pointer with correct canonical path
- **Method doc:** `C:/claude_base/tools/fleetcomm/fleetcomm_method_v01_tomemex.md`
- **Human-viewable board:** just open `https://fleetcomm.max-rempel2.workers.dev` in a browser
- **git:** committed to claude_base master, pushed

## EXACT NEXT STEP

**Send a message to Mike on Centauri using fleetcomm.** The user just told me: "talk to mike in dc session on centauri."

Do this:
```
FLEETCOMM_MACHINE=Pine python C:/claude_base/tools/fleetcomm/fleetcomm.py post "Hey Mike - Pine here. Max wants us linked up. What are you working on?" --session villani
```

Then read back to check for responses:
```
python C:/claude_base/tools/fleetcomm/fleetcomm.py read
```

(Replace `--session villani` with whatever session label makes sense - that's the label from this worktree: `beautiful-villani-5507cf`.)

If no immediate response, remember ~60s KV propagation lag - wait and `read --all` if needed.

## OPEN QUESTIONS STILL AWAITING USER

- **"Talk to mike in dc session"** - What is Mike working on? What should the actual message content be, beyond a hello? Max didn't specify.
- **Auto-hear hook** - not built. Max said "you decide" for approach; it was explicitly left as optional. If sessions need automatic inbox checking each turn, it needs wiring.
- **Centauri git-pull** - Centauri can't non-interactively pull claude_base (no GitHub creds). Any future updates to fleetcomm or other repo files need manual copy or SSH-based push. Not resolved, just worked around for now.
- **Path for Centauri sessions using fleetcomm** - global2 says `C:/claude_base/tools/fleetcomm/fleetcomm.py`. Centauri sessions use forward-slashes with `python` but it's Windows - Centauri's pasted session added a warning about this. Probably fine (Windows Python tolerates forward slashes), but untested in an automated turn.

## KEY PATHS, IDS, COMMANDS

| Thing | Path/Value |
|---|---|
| CLI (both machines) | `C:/claude_base/tools/fleetcomm/fleetcomm.py` |
| Worker URL | `https://fleetcomm.max-rempel2.workers.dev` |
| Human board view | `https://fleetcomm.max-rempel2.workers.dev` (bare URL in browser) |
| Auth key (post) | `fleetcomm_claymem2026` (set as env `FLEETCOMM_KEY`, hardcoded in CLI) |
| Cloudflare token | `ZUyIUYjo_6w53JHSBfGmw1Tei9XgBBNsnpKTMR2b` |
| CF account ID | `e4dc2224d6baa721873dca77dc6f057d` |
| Worker source | `C:/claude_base/tools/fleetcomm/worker/index.js` |
| Worker config | `C:/claude_base/tools/fleetcomm/worker/wrangler.toml` |
| Cursor file (local, gitignored) | `tools/fleetcomm/.fleetcomm_cursor.json` |
| Method doc | `C:/claude_base/tools/fleetcomm/fleetcomm_method_v01_tomemex.md` |
| Synced global rules (both machines) | `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md` |
| Centauri Nextcloud path | `D:\nextcloud\claude_md_synced\global2.md` |
| Centauri SSH | `ssh -i ~/.ssh/sol_key maxre@192.168.1.176` |
| Wrangler version | 4.103 (available on Pine via `npx`) |
| Post command | `python C:/claude_base/tools/fleetcomm/fleetcomm.py post "msg" --session <label>` |
| Read new command | `python C:/claude_base/tools/fleetcomm/fleetcomm.py read` |
| Read all command | `python C:/claude_base/tools/fleetcomm/fleetcomm.py read --all` |
| Machine env var | `FLEETCOMM_MACHINE=Pine` or `Centauri` (auto-detected via hostname, fallback to env) |

## GOTCHAS + DEAD ENDS

1. **Wall auto-deletes at 30 min** - ruled out for async use; confirmed before building fleetcomm.
2. **Centauri can't git-pull** - non-interactive GitHub auth fails. If fleetcomm files are updated, they must be pushed to master, then either manually copied to Centauri or ssh'd over. Not a blocker now but a gotcha for future changes.
3. **Cloudflare token is Workers-scoped only** - confirmed early: has Workers + KV, no D1 admin. That's sufficient for this worker.
4. **Centauri path forward-slashes** - Windows Python tolerates them, but Centauri's Claude session flagged this. The global2 entry uses `/` - not a bug, just a note.
5. **KV propagation lag ~60s** - eventual consistency. A freshly posted message may not appear immediately on a `read` from the other machine. Use `--all` and a short wait if `read` returns nothing.
6. **No auth on reads** - by design. Don't put secrets, API keys, or passwords in fleetcomm messages.
7. **The wall (`claude-wall`) and fleetcomm are completely separate workers** - zero risk of cross-contamination. The wall is still live and unchanged for other sessions.
8. **403 on first CLI test** - Cloudflare blocked urllib's default User-Agent. Fixed by adding a standard `User-Agent` header in the CLI.
