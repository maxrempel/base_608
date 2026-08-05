Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw """ & "C:\cloud_base\scripts\mdindex_sync.py" & """", 0, False
