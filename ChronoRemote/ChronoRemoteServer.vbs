Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "C:\ChronoRemote\ChronoRemoteSocket.bat" & Chr(34), 0
WshShell.Run chr(34) & "C:\ChronoRemote\ChronoRemoteFlask.bat" & Chr(34), 0
Set WshShell = Nothing
