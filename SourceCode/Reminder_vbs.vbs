Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "C:\Program Files\ChronoAlert\Reminder_batfile.bat" & Chr(34), 0
Set WshShell = Nothing