' ============================================================
'  AUTORUN_BRIDGE_FONDA.vbs
'  ATLAS PC Bridge agentini fonda (oynasiz) ishga tushiradi.
'  Vercel paneldagi tugmalar shu agent orqali bajariladi.
' ============================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Skript turgan papkani ish papkasi qilib olish
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDir

' 0 = oyna ko'rsatilmaydi, False = tugashini kutmaydi
WshShell.Run "python run_pc_bridge.py", 0, False
