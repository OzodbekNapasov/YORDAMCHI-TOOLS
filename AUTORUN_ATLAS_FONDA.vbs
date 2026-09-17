' ============================================================
'  AUTORUN_ATLAS_FONDA.vbs
'  ATLAS platformasini to'liq fonda (oynasiz) ishga tushiradi.
'
'  bot.py quyidagilarning HAMMASINI yoqadi:
'    - PC Bridge agenti (MTF konvertor, Vercel paneldagi tugmalar)
'    - Insta/YouTube jadvali (09:00, 12:00, 15:00, 18:30, 21:00)
'    - Telegram bot
'    - Mahalliy veb server (http://127.0.0.1:5005)
'
'  Avtomatik ishga tushirish: Win+R -> shell:startup -> shu faylni tashlang.
'  Nusxa ham, yorliq ham ishlaydi.
'
'  Eslatma: AUTORUN_BRIDGE_FONDA.vbs faqat bridge'ni yoqadi (jadvalsiz).
'  Ikkalasini birga ishlatmang - bot.py bridge'ni o'zi boshqaradi.
' ============================================================

Option Explicit

Dim WshShell, fso, projectDir, fallbackDir, pyExe, svc, procs, p, cmdLine

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' ---------- 1. Loyiha papkasini topish ----------
projectDir = fso.GetParentFolderName(WScript.ScriptFullName)
If Not fso.FileExists(fso.BuildPath(projectDir, "bot.py")) Then
    ' Bu nusxa (masalan Startup papkasida) - haqiqiy joydan qidiramiz
    fallbackDir = "C:\Users\user\Desktop\kontrakt bot"
    If fso.FileExists(fso.BuildPath(fallbackDir, "bot.py")) Then
        projectDir = fallbackDir
    Else
        MsgBox "ATLAS topilmadi: bot.py yo'q." & vbCrLf & vbCrLf & _
               "Qidirildi:" & vbCrLf & _
               fso.GetParentFolderName(WScript.ScriptFullName) & vbCrLf & _
               fallbackDir, 16, "ATLAS"
        WScript.Quit 1
    End If
End If

' ---------- 2. Python ni topish ----------
' Faqat "python" deb yozish yetarli emas: wscript muhitida PATH boshqacha
' bo'lishi mumkin va skript jimgina ishga tushmay qolardi. Shuning uchun
' aniq yo'llar sinaladi va hech biri topilmasa, ochiq xato ko'rsatiladi.
pyExe = ""

If fso.FileExists(fso.BuildPath(projectDir, ".venv\Scripts\python.exe")) Then
    pyExe = fso.BuildPath(projectDir, ".venv\Scripts\python.exe")
ElseIf fso.FileExists(fso.BuildPath(projectDir, "venv\Scripts\python.exe")) Then
    pyExe = fso.BuildPath(projectDir, "venv\Scripts\python.exe")
End If

If pyExe = "" Then
    Dim candidates, i, c
    candidates = Array( _
        WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%\Programs\Python\Python314\python.exe"), _
        WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%\Programs\Python\Python313\python.exe"), _
        WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%\Programs\Python\Python312\python.exe"), _
        WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%\Programs\Python\Python311\python.exe"), _
        "C:\Python314\python.exe", "C:\Python313\python.exe" _
    )
    For i = 0 To UBound(candidates)
        c = candidates(i)
        If pyExe = "" And fso.FileExists(c) Then pyExe = c
    Next
End If

If pyExe = "" Then
    MsgBox "Python topilmadi." & vbCrLf & vbCrLf & _
           "Python o'rnatilganini tekshiring yoki loyihada .venv yarating.", _
           16, "ATLAS"
    WScript.Quit 1
End If

' ---------- 3. Allaqachon ishlayaptimi? ----------
' Ikkita nusxa bir navbatga post chiqarmasligi uchun. Tekshiruv loyiha yo'li
' bo'yicha: bu kompyuterda boshqa loyihalarning bot.py fayllari ham ishlaydi.
On Error Resume Next
Set svc = GetObject("winmgmts:\\.\root\cimv2")
If Err.Number = 0 Then
    Set procs = svc.ExecQuery("SELECT CommandLine FROM Win32_Process WHERE Name='python.exe'")
    For Each p In procs
        If Not IsNull(p.CommandLine) Then
            If InStr(LCase(p.CommandLine), "bot.py") > 0 And _
               InStr(LCase(p.CommandLine), LCase(projectDir)) > 0 Then
                WScript.Quit 0
            End If
        End If
    Next
End If
Err.Clear
On Error GoTo 0

' ---------- 4. Ishga tushirish ----------
WshShell.CurrentDirectory = projectDir
cmdLine = """" & pyExe & """ """ & fso.BuildPath(projectDir, "bot.py") & """"
' 0 = oyna ko'rsatilmaydi, False = tugashini kutmaydi
WshShell.Run cmdLine, 0, False
