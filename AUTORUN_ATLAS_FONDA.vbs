' ============================================================
'  AUTORUN_ATLAS_FONDA.vbs
'  ATLAS platformasini to'liq fonda (oynasiz) ishga tushiradi.
'
'  bot.py quyidagilarning HAMMASINI yoqadi:
'    - Insta/YouTube jadvali (09:00, 12:00, 15:00, 18:30, 21:00)
'    - PC Bridge agenti (Vercel paneldagi tugmalar, MTF konvertor)
'    - Telegram bot
'    - Mahalliy veb server
'
'  Avtomatik ishga tushirish uchun:
'    Win+R -> shell:startup -> shu faylni (yoki yorlig'ini) tashlang.
'
'  Fayl Startup papkasiga NUSXA qilib qo'yilsa ham ishlaydi: yonida bot.py
'  topilmasa, quyidagi ma'lum yo'ldan qidiradi.
'
'  Eslatma: AUTORUN_BRIDGE_FONDA.vbs faqat bridge'ni yoqadi (jadvalsiz).
'  Ikkalasini birga ishlatmang - bot.py bridge'ni o'zi boshqaradi.
' ============================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

projectDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Yonida bot.py yo'qmi? Demak bu nusxa (masalan Startup papkasida) —
' loyihaning haqiqiy joyidan qidiramiz.
If Not fso.FileExists(fso.BuildPath(projectDir, "bot.py")) Then
    fallbackDir = "C:\Users\user\Desktop\kontrakt bot"
    If fso.FileExists(fso.BuildPath(fallbackDir, "bot.py")) Then
        projectDir = fallbackDir
    Else
        MsgBox "ATLAS topilmadi: bot.py yo'q." & vbCrLf & _
               "Qidirilgan joylar:" & vbCrLf & _
               fso.GetParentFolderName(WScript.ScriptFullName) & vbCrLf & _
               fallbackDir, 16, "ATLAS"
        WScript.Quit 1
    End If
End If

' Allaqachon ishlab turgan bo'lsa, ikkinchisini ochmaymiz
Set svc = GetObject("winmgmts:\\.\root\cimv2")
Set procs = svc.ExecQuery("SELECT CommandLine FROM Win32_Process WHERE Name='python.exe'")
For Each p In procs
    If Not IsNull(p.CommandLine) Then
        If InStr(LCase(p.CommandLine), "bot.py") > 0 And _
           InStr(LCase(p.CommandLine), LCase(projectDir)) > 0 Then
            WScript.Quit 0
        End If
    End If
Next

WshShell.CurrentDirectory = projectDir
' 0 = oyna ko'rsatilmaydi, False = tugashini kutmaydi
WshShell.Run "cmd.exe /c cd /d """ & projectDir & """ && python bot.py", 0, False
