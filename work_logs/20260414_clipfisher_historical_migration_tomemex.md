# ClipFisher Historical Migration Report
# Author: Opus 4.6, Pine, Claude Code, 2026-04-14
# Status: Preservation-only. No DAX service activation.

## What ClipFisher is

A small Python video-clip service that ran on Sol with two live slots
plus Cloudflare tunnels in front of them. Max characterizes it as
mostly historical; the codebase is stable and no longer actively
developed. Related subproject: `amp` / `amptest1` / `amptest2` (same
author, Sizzler-family, fronted by its own tunnels).

## Current runtime state (as of 2026-04-14)

Sol is dead (drive pulled out, now read-only at Pine as `/mnt/sol` via
WSL). Every ClipFisher and amp service listed below is therefore
**not running** anywhere. The Cloudflare tunnels behind the public
hostnames are dead too. Nothing to break further.

## Service inventory (retrieved from Sol)

All unit files are preserved in
`C:\claude_base\sol_scripts_retrieved\clipfisher\`:

App services:
- clipfisher-live.service    -- port 8085, runs clipfisher_v25.py
- clipfisher-test.service    -- port 8084, runs clipfisher_v25.py
- amptest1.service           -- port 8087, amp_api_v08.py
- amptest2.service           -- port 8088, amptest_api_v06.py

Cloudflare tunnels (tokens embedded in unit files):
- clipfisher-tunnel.service        -- main
- clipfisher-blue-tunnel.service   -- blue slot
- clipfisher-green-tunnel.service  -- green slot
- clipfisher-tunnel-1.service      -- test slot (public hostname)
- clipfisher-tunnel-2.service      -- live slot (public hostname)
- amp-tunnel.service               -- amp.dnaresonance.com
- amptest1-tunnel.service          -- a1.dnaresonance.com
- amptest2-tunnel.service          -- a2.dnaresonance.com

## Code inventory

Lives in Nextcloud and is already synced to Pine, Lakarian, and
(when it was alive) Sol. Size: 96 KB on Sol, 88 KB on Lakarian.

Path on Pine: `C:\Users\maxre\Nextcloud\202603q1_clipfisher\`
Path on Lakarian: `/home/yunohost.app/nextcloud/data/mremp/files/202603q1_clipfisher/`

Files:
- clipfisher_v25.py          -- current production version
- clipfisher_v24.py          -- prior version, kept for rollback
- clipfisher_deploy.py       -- deploy helper
- clipfisher_batch_import.py -- batch import tool
- deploy_state.json          -- deploy tracking
- tunnel1_token.txt          -- tunnel credentials (plaintext)
- tunnel2_token.txt          -- tunnel credentials (plaintext)
- versions/                  -- older version snapshots

Amp code: `/home/maxre/Nextcloud/202603_sizzle/amp/` on Sol
(part of the Sizzler project tree, which Max says is already migrated).

## What was done in this pass

1. Service unit files copied from Sol's `/etc/systemd/system/` into the
   git repo at `sol_scripts_retrieved/clipfisher/`. This preserves the
   exact systemd contract (ports, env vars, tunnel tokens, binary paths)
   for future re-deployment if needed.
2. Verified code is already in Lakarian's Nextcloud datastore — no risk
   of data loss from Sol going permanently offline.
3. This report written.
4. NO services were deployed or started on DAX. Per Max, ClipFisher is
   historical; leaving it dormant is acceptable.
5. Memex was not touched.

## How to revive (if ever wanted)

Minimum steps to bring ClipFisher back on DAX:

1. Ensure `202603q1_clipfisher/` is synced onto DAX (either via
   Syncthing from Lakarian like the Memex pusher sources, or one-shot
   rsync).
2. Adjust the 2 unit files (`clipfisher-live.service`,
   `clipfisher-test.service`):
   - change `User=maxre` to `User=bitnami`
   - change `WorkingDirectory=/home/maxre/Nextcloud/...` to wherever the
     code lands on DAX
3. Install + start the 2 app services and the relevant tunnel services.
   The tunnel tokens in the unit files are still valid; no Cloudflare
   dashboard work needed to re-route.
4. Same pattern for amp services if those are wanted too.

Not doing this now because Max explicitly flagged it as historical and
the priority was not breaking Memex.

## Git restore point

This commit is the canonical preservation point for ClipFisher:
- Repo: https://github.com/maxrempel/claude_base
- Contains: this report + all 12 service unit files under
  `sol_scripts_retrieved/clipfisher/`.

Combined with the Nextcloud copy of the Python code on Lakarian, every
ClipFisher artifact is recoverable even if the Sol drive is dropped.
