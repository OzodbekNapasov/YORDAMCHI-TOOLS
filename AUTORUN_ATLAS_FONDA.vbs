' ============================================================
'  AUTORUN_ATLAS_FONDA.vbs
'  ATLAS platformasini to'liq fonda (oynasiz) ishga tushiradi.
'
'  bot.py quyidagilarning HAMMASINI yoqadi:
'    - Insta/YouTube jadvali (09:00, 12:00, 15:00, 18:30, 21:00)
'    - PC Bridge agenti (Vercel paneldagi tugmalar uchun)
'    - Telegram bot
'    - Mahalliy veb server
'
'  Startup papkasiga shu faylning YORLIG'INI tashlang:
'    Win+R  ->  shell:startup
'
'  Eslatma: AUTORUN_BRIDGE_FONDA.vbs faqat bridge'ni yoqadi (jadvalsiz).
'  Ikkalasini birga ishlatmang - bot.py bridge'ni o'zi boshqaradi.
' ============================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDir

' 0 = oyna ko'rsatilmaydi, False = tugashini kutmaydi
WshShell.Run "cmd.exe /c cd /d """ & scriptDir & """ && python bot.py", 0, False
