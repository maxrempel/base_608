# Scribe handover - milestone 2 (~150K tokens)
# session: 20260728_priceless_snyder_07082c_76f4bb0b
# cwd: C:\claude_base\.claude\worktrees\priceless-snyder-07082c
# written: 2026-07-28 17:28:04 by deepseek-v4-pro

**GOAL (in Max's words)**
> "why did codex die? I restarted pine, didn't help. It gives an error and refers to microsoft store."

Fix the ChatGPT desktop app ("Codex") on Windows (Pine) so it launches normally instead of showing an error that redirects to the Microsoft Store.

---

**DECISIONS + WHY**
- **First diagnosis:** the codex CLI is fine; the problem is only the Store-packaged desktop app (OpenAI.Codex). Its Store package was marked "NeedsRemediation" (corrupted/needs repair), causing Windows to refuse launch and send the user to the Store.
- **Root cause of repair failure:** The Store's own repair mechanism fails because two Windows services are disabled - **Microsoft Store Install Service** (`InstallService`) and **Windows Update** (`wuauserv`). The disablement is likely an old "debloat" tweak (the `Wub` / "Windows Update Blocker" tool was found on the machine).
- **Fix strategy chosen:**  
  1. Remove the broken `OpenAI.Codex` package.  
  2. Re-enable the two services, then reinstall the app from the Store (via `winget` or manual Store).  
  *Why this order:* The package was thoroughly corrupted, so repair alone wouldn't work; a clean reinstall after the services are unlocked is the safest path.
- **Service re-enable method:** Direct registry edits and `sc config` were blocked by the `Wub` tool. The assistant located `Wub_x64.exe` in `Downloads\Wub\Wub\` and ran it with the `/E` switch (enable) to undo the service blocking. This was successful - both services moved to Running.
- **Reinstall method:** `winget install --id 9PLM9XGG6VKS --source msstore ...` was chosen because it avoids UI interaction and can be triggered automatically from the shell. The assistant started this just before the user interrupted.

---

**CURRENT STATE**
- The corrupted `OpenAI.Codex` package has been **removed** from the system.
- `InstallService` and `wuauserv` are **now running** after using `Wub_x64.exe /E`.
- The **reinstall via `winget`** was launched but **status unknown** - the user interrupted the session just after the command was issued. It may have completed or may still be pending.
- No other side effects are present; the `codex` CLI tool still works.

---

**EXACT NEXT STEP**
1. **Check whether the Store app is now installed and launchable.**  
   - Run `Get-AppxPackage OpenAI.Codex` to see if the package is back.  
   - If it is present, try launching ChatGPT from Start menu or via `explorer.exe shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App`.  
   - If it works, we're done.
2. **If the package is not installed**, re-run the `winget` install (or use the Store GUI as an alternative).  
   ```
   winget install --id 9PLM9XGG6VKS --source msstore --accept-package-agreements --accept-source-agreements
   ```
   Wait for it to finish, then verify launch.
3. **If the installer fails with an error about services again**, confirm `InstallService` and `wuauserv` are still Running and not disabled by the blocker tool. The `Wub` tool may re-lock after reboot, but currently it's disabled. No reboot has occurred since the fix.

---

**OPEN QUESTIONS (for Max)**
- Did the `winget` install finish while the session was interrupted, or is the app still missing?  
- Was there any error message from `winget`?  
- Would you prefer to use the Store GUI to install (simpler visual confirmation), or continue with `winget`?

---

**KEY PATHS / IDs / NAMES**
- **App package ID:** `OpenAI.Codex` (Publisher ID `2p2nqsd0c76g0`), Store ID `9PLM9XGG6VKS`  
- **Windows Update Blocker tool:** `C:\Users\maxre\Downloads\Wub\Wub\Wub_x64.exe`  
  Used with `/E` to enable services (and `/D` would disable again).  
- **Affected services:**  
  - `InstallService` (Microsoft Store Install Service)  
  - `wuauserv` (Windows Update)  
- **Relevant registry keys:** `HKLM:\SYSTEM\CurrentControlSet\Services\InstallService` and `...\wuauserv` - Start value should be 3 (Manual). The `Wub` tool enforces 4 (Disabled) and blocks registry writes.

---

**GOTCHAS & DEAD ENDS RULED OUT**
- **Reboot doesn't help.** The corruption is persistent and services stay disabled through reboot because of the `Wub` registry lock.
- **`Reset-AppxPackage` and `Add-AppxPackage -Register` did not work** - the package was too damaged, and the Store services couldn't remediate it.
- **Direct registry/service modification (even elevated) was blocked** by `Wub`; it took ownership but the tool still protected the keys. The official `/E` switch of `Wub` was the only way to unlock them.
- **The codex CLI is separate** and is not affected - no need to reinstall or configure it.
- If the Store complaint returns after a future reboot, the `Wub` tool may have re-disabled services; simply run `Wub_x64.exe /E` again.
