Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c """ & WshShell.CurrentDirectory & "\venv\Scripts\python.exe"" """ & WshShell.CurrentDirectory & "\bot.py""", 0, False
