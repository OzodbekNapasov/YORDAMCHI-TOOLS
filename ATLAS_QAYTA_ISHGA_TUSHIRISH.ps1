# ============================================================
#  ATLAS_QAYTA_ISHGA_TUSHIRISH.ps1
#  ATLAS ning barcha nusxalarini to'xtatib, bittasini toza ishga tushiradi.
#
#  Nima uchun: bir nechta nusxa ishlab tursa, Telegram bot bitta token bilan
#  bir vaqtda ulanishga urinadi va 409 Conflict beradi. Jadval esa Supabase
#  orqali himoyalangan, lekin ortiqcha nusxalar keraksiz yuk beradi.
#
#  Ishlatish (oddiy PowerShell, admin shart emas):
#     .\ATLAS_QAYTA_ISHGA_TUSHIRISH.ps1
# ============================================================

$ErrorActionPreference = "SilentlyContinue"
$proj = "C:\Users\user\Desktop\kontrakt bot"

Write-Host "ATLAS qayta ishga tushirilmoqda..." -ForegroundColor Cyan
Write-Host ""

# --- 1. ATLAS nusxalarini topish ---
# Boshqa loyihalarning bot.py fayllariga TEGILMAYDI: bu kompyuterda
# D:\My BOTS va D:\MyTestX dan ham python jarayonlari ishlaydi.
$atlas = @()
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ForEach-Object {
    $p = $_
    $cmd = if ($null -eq $p.CommandLine) { "" } else { $p.CommandLine }
    $cwd = ""
    try {
        $cwd = (Get-Process -Id $p.ProcessId).Path
    } catch { }

    $isAtlas = $false
    if ($cmd -like "*$proj*") { $isAtlas = $true }
    # "python bot.py" - yo'lsiz ishga tushirilgan bo'lishi mumkin.
    # Boshqa loyihalar .venv ishlatadi yoki boshqa fayl nomiga ega.
    elseif ($cmd -match '(^|\s)"?python(\.exe)?"?\s+"?bot\.py"?\s*$' -and $cmd -notlike "*.venv*") {
        $isAtlas = $true
    }

    if ($isAtlas) {
        $atlas += [PSCustomObject]@{ PID = $p.ProcessId; Cmd = $cmd }
    }
}

if ($atlas.Count -eq 0) {
    Write-Host "Ishlab turgan ATLAS nusxasi yo'q." -ForegroundColor Yellow
} else {
    Write-Host "Topildi: $($atlas.Count) ta nusxa" -ForegroundColor Yellow
    foreach ($a in $atlas) {
        Write-Host ("   PID {0}  {1}" -f $a.PID, $a.Cmd.Substring(0, [Math]::Min(54, $a.Cmd.Length)))
    }
    Write-Host ""
    Write-Host "To'xtatilmoqda..." -ForegroundColor Yellow
    foreach ($a in $atlas) {
        Stop-Process -Id $a.PID -Force
    }
    Start-Sleep -Seconds 3
}

# --- 2. Bittasini ishga tushirish ---
Write-Host ""
Write-Host "Yangi nusxa ishga tushirilmoqda..." -ForegroundColor Cyan
Start-Process -FilePath "wscript.exe" `
    -ArgumentList "`"$proj\AUTORUN_ATLAS_FONDA.vbs`"" `
    -WindowStyle Hidden
Start-Sleep -Seconds 12

# --- 3. Tekshirish ---
$now = @()
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ForEach-Object {
    $cmd = if ($null -eq $_.CommandLine) { "" } else { $_.CommandLine }
    if ($cmd -like "*$proj*") { $now += $_.ProcessId }
}

Write-Host ""
if ($now.Count -eq 1) {
    Write-Host "TAYYOR. ATLAS ishlamoqda (PID $($now[0]))." -ForegroundColor Green
} elseif ($now.Count -eq 0) {
    Write-Host "XATO: ishga tushmadi." -ForegroundColor Red
    Write-Host "Qo'lda sinab ko'ring:  python bot.py" -ForegroundColor Red
} else {
    Write-Host "OGOHLANTIRISH: $($now.Count) ta nusxa ishlamoqda -> $now" -ForegroundColor Yellow
    Write-Host "Skriptni qayta ishga tushiring." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Tekshirish uchun:  python platform_healthcheck.py" -ForegroundColor Gray
