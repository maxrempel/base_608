
## [2026-07-02 07:52] ? de7bc1bf
- DID: Fixed accidental hibernate on numpad-5. Killed hibernate_ce.ahk (bound bare numpad-5 to SetSuspendState hibernate=1); archived to C:/Users/maxre/hibernate_disabled_20260701. Built sleep_numpadslash.ahk = numpad-/ -> real sleep, autostarts. Cleaned up misnamed sleep_hotkey.ps1 (was Delete->monitor-off). Also earlier: killed frozen TextInputHost (9073s CPU), root cause = 6 typer1 --paste instances flooding clipboard events.
- STATE: Sleep hotkey on numpad-/ is live (PID 47912). Hibernate binding gone. Typer1 clipboard issue reported to E125 who committed a fix in 74bfdf56.
- NEXT: If Max wants numpad-/ freed for math and moved to a modifier combo, edit sleep_numpadslash.ahk. If typer1 still bothersome, retire typer1 in favor of typer2 keystroke mode.
