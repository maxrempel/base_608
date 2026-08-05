' Launches the nightly Cloudflare workers + KV backup fully hidden
' (window style 0 = no window). Prevents the prohibited flashing terminal that
' the Interactive scheduled task would otherwise show every night. The .bat
' keeps doing its work (python script + git commit/push); only the console
' window is suppressed.
CreateObject("WScript.Shell").Run "C:\claude_base\scripts\backup_cf_workers.bat", 0, False
