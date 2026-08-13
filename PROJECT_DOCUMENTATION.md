# 🚀 Kontrakt Yangilovchi va Guruhlar Telegram Boti (Proyekt Hujjati va Yo'riqnoma)
**Tizim Versiyasi:** `v1.6.1`  
**Muallif / Admin Telegram ID:** `8135594558`  
**Deploy Platformasi:** Vercel (Serverless Python WSGI) / PythonAnywhere  

---

## 📌 1. LOYIHA HAQIDA UMUMIY MA'LUMOT (OVERVIEW)

Ushbu bot oliygoh yoki ta'lim muassasasining buxgalteriya bo'limi uchun maxsus yaratilgan bo'lib, quyidagi 3 ta asosiy vazifani to'liq avtomatlashtiradi:

1. **Kontrakt to'lovlarini avtomatik yangilash:** Bankdan keladigan kunlik **Debitorka (`.xlsx`)** fayli va muassasaning **Asosiy Baza (`.xlsx`)** faylini taqqoslab, to'lov qilgan talabalarning hisobini avtomatik yangilaydi.
2. **Formulalarni 100% saqlab qolish:** Excel faylidagi barcha yig'indi (`SUM`), mantiqiy (`IF`) va `VLOOKUP` formulalariga zarar yetkazmasdan, faqat to'lov summasi katakchalarini yangilaydi.
3. **HD Screenshot va Xulasa Hisobotlar:** 
   - Har bir guruh bo'yicha Times New Roman Bold shriftida chiroyli High-Definition (3x Ultra HD) rasm-jadvallarni generatsiya qiladi.
   - Kontrakt yangilanishi yakunida barcha guruh rahbarlari, talabalar soni va qarzdorliklar jamlanmasini aks ettiruvchi **XULOSA rasm-jadvalini** avtomatik yuboradi.
4. **Yagona Admin Xavfsizligi (Single Admin Whitelist):** Bot faqatgina tayinlangan Bosh Buxgalter Telegram ID si (`8135594558`) orqali ishlaydi. Begona foydalanuvchilardan menyu tugmalarini yashiradi (`ReplyKeyboardRemove`).

---

## 🛠️ 2. TEXNOLOGIK STEK VA KUTUBXONALAR (TECH STACK)

- **Dasturlash tili:** Python 3.10+
- **Telegram Bot Framework:** `pyTelegramBotAPI` (`telebot`)
- **Web Server / Webhook:** `Flask` (WSGI Micro-framework)
- **Excel Bilan Ishlash:** `openpyxl`
- **Rasm Generatsiyasi (HD Screenshot):** `Pillow` (`PIL`)
- **Fuzzy Name Matching (Ismlarni Topish):** `fuzzywuzzy` + `python-Levenshtein`
- **Shriftlar:** Times New Roman Bold TTF (`fonts/TimesNewRomanBold.ttf`)

---

## 🧠 3. BOTNING ISHLASH PRINSIPI VA ALGORITMLARI (HOW IT WORKS)

### 3.1. Ismlarni 100% Aniqlikda Taqqoslash (Fuzzy Matching + Transliteration)
Bank debitorkasida talaba ismi kirillcha (`ШАМСИЕВА ФОТИМА`), pasport bo'yicha (`Shamsiyeva Fotima`) yoki shartnoma raqamlari bilan (`00111TOSHPULATOVA`) yozilgan bo'lishi mumkin.
- `cyrillic_to_latin()` yordamida kirillcha harflar lotinchaga o'giriladi.
- `ismlarni_standartlash()` yordamida tutruq belgilari (`'`, `‘`, `` ` ``), `o'`, `g'`, `ch`, `sh` kabi belgilar va raqamlar tozalanadi.
- `fuzzywuzzy` algoritmlari (`token_set_ratio`, `partial_ratio`, `token_sort_ratio`) ning eng yuqorisi olinib, **70% dan yuqori ball** toplagan talaba bazadan 100% aniqlikda topiladi va to'lovi qo'shiladi.

### 3.2. Sanani Avtomatik Aniqlash
- Bot Asosiy Baza Excel faylining ichidagi `"Yangilangan sanasi:"` katagini yoki fayl nomidagi sanani avtomatik skanerlaydi.
- Oxirgi yangilangan sanaga **+1 kun** qo'shib, Telegramda foydalanuvchiga quick button sifatizda taklif etadi (masalan: `01.08.2026`).

### 3.3. HD Rasm-Jadval Generatori (Pillow Canvas API)
- Rasm sifatini mukammal qilish uchun **3x Scale factor (`S = 3`)** ishlatiladi.
- Katakcha balandligi (`row_h = 42 * S`) qulay vertikal padding bilan berilgan.
- Ismlar ustuni kengligi (`col_w = 520 * S`) eng uzun familiyalar ham sig'ishi uchun kengaytirilgan.
- **Qarzdorlik ranglari:**
  - Qarz (`> 0`): Yumshoq qizil fon (`#FFC7CE`) + To'q qizil matn (`#9C0006`).
  - Ortiqcha to'lov / Toza (`<= 0`): Yumshoq yashil fon (`#C6EFCE`) + To'q yashil matn (`#006100`).

### 3.4. Guruh Rahbarlari Bo'yicha XULOSA Rasm Jadvali
- `process_kontrakt_update` funksiyasi `KONTRAKTLAR` varog'ining 1-18 qatorlaridagi Guruh rahbarlari va Guruh nomlarini o'qiydi.
- Yangilangan talabalar to'lovlari bo'yicha har bir guruhning talabalar soni va musbat qarzdorliklarini hisoblaydi.
- Olovrang sarlavhali (`#ED7D31`) hamda pastida **Qizil fondagi JAMI qatori** bo'lgan XULOSA rasm-jadvalini generatsiya qilib yuboradi.

---

## 🔒 4. XAVFSIZLIK VA KIRISH HUQUQLARI (SECURITY & PERMISSIONS)

- `PRIMARY_ADMIN_ID = 8135594558`: Loyiha kodida faqat bitta admin ID belgilangan.
- Begona foydalanuvchi yozganda:
  - Bot `telebot.types.ReplyKeyboardRemove()` yuborib, menyu tugmalarini yo'qotadi.
  - Samimiy rad etish xabarini chiqaradi.

---

## 📁 5. LOYIHA FAYLLAR TUZILMASI (PROJECT STRUCTURE)

```
kontrakt-bot/
├── bot.py                       # Botning asosiy kodi (Flask + telebot + Pillow logic)
├── requirements.txt             # Kerakli Python kutubxonalari
├── vercel.json                  # Vercel serverless deploy konfiguratsiyasi
├── fonts/
│   ├── TimesNewRomanBold.ttf    # HD screenshotlar uchun asosiy Bold shrift
│   └── AppBoldFont.ttf         # Zaxira shrift
└── PROJECT_DOCUMENTATION.md     # Loyiha hujjatlari va yo'riqnomasi
```

---

## 🚀 6. KELAJAKDA SHUNDAY BOTNI NOLDAN QURISH YO'RIQNOMASI

Agarda kelajakda boshqa loyiha yoki tashkilot uchun ham shunday bot qurmoqchi bo'lsangiz, quyidagi bosqichlarni bajarasiz:

### 1-Bosqich: Telegram Bot Yaratish
1. Telegramda `@BotFather` ga kiring.
2. `/newbot` buyrug'ini yuboring va botingizga nom hamda username bering.
3. Sizga berilgan `HTTP API TOKEN` ni nusxalab oling.

### 2-Bosqich: Muhitni Sozlash va Kutubxonalarni O'rnatish
Kompyuteringizda terminalda quyidagi buyruqni bering:
```bash
pip install pyTelegramBotAPI openpyxl pillow fuzzywuzzy python-Levenshtein Flask
```

### 3-Bosqich: Shriftlarni Joylash
Loyihangiz papkasida `fonts/` nomli papka ochib, uning ichiga `TimesNewRomanBold.ttf` faylini joylang. Barcha chiroyli jadvallar shu shrift orqali chiziladi.

### 4-Bosqich: Kodni Ishga Tushirish
`bot.py` faylida Telegram Tokeningizni va Telegram ID ingizni kiriting hamda dasturni ishga tushiring:
```bash
python bot.py
```

### 5-Bosqich: GitHub va Vercel ga Yuklash (Deploy)
1. Kodingizni GitHub omboriga push qiling (`git push origin main`).
2. [Vercel.com](https://vercel.com) saytiga kirib, GitHub omboringizni import qiling.
3. Environment Variable bo'limiga `BOT_TOKEN` ni kiriting va **Deploy** tugmasini bosing.
4. Vercel bergan URL manziliga `/set_webhook` buyrug'ini yuborib web-hookni faollashtiring (Masalan: `https://sizning-botingiz.vercel.app/set_webhook`).

---
✅ **Loyiha to'liq tayyor va har bir yangilanish Vercel-da avtomatik ishlaydi.**
