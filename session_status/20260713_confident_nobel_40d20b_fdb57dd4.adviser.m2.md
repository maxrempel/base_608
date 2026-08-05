# Adviser note - milestone 2 (~165K tokens)
# session: 20260713_confident_nobel_40d20b_fdb57dd4
# written: 2026-07-13 11:12:53 by deepseek-v4-pro

TO ASSISTANT: You're testing with simulated keystrokes (SendInput) which most global hotkey hooks filter via the LLKHF_INJECTED flag - LightShot almost certainly ignores injected input. Stop that rabbit hole. Instead: (1) use LightShot's tray icon right-click ? "Screen capture" to verify the app actually works; (2) check LightShot's hotkey registration survives restart via its own settings (HKCU\Software\Skillbrains\LightShot); (3) just ask Max to tap the physical key and report - that's the only reliable test.

Also, Max said "I need it working from both print screen button and shift print screen button" - you acknowledged this but never wired it. Stop asking if he "really needs" Shift+Print Screen. Wire it. LightShot doesn't natively bind Shift combos, so you'll need AutoHotkey or a small launcher to catch Shift+PrintScreen ? launch LightShot's capture. Plan that, don't defer it again.
