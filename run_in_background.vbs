Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c Price_Alert.bat"
oShell.Run strArgs, 0, false