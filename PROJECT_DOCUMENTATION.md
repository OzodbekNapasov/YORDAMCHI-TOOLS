# 🚀 Unified Document & Contract Platform (Proyekt Hujjati va Yo'riqnoma)
**Tizim Versiyasi:** `v2.0.0` (Birlashtirilgan Yagona Platforma)  
**Muallif / Admin Telegram ID:** `8135594558`  
**Deploy Platformasi:** Vercel (Serverless Python WSGI) / PythonAnywhere  

---

## 📌 1. LOYIHA HAQIDA UMUMIY MA'LUMOT (OVERVIEW)

Ushbu yagona platforma 2 ta katta loyihani bitta bot va bitta tizimga birlashtirdi:

1. **Kontrakt Yangilovchi Modul:**
   - Bank debitorkasi (`.xlsx`) va Asosiy Baza (`.xlsx`) fayllarini taqqoslab, to'lovlarni avtomatik yangilaydi.
   - Excel faylidagi formulalarga umuman tegmasdan saqlaydi.
   - Guruhlar bo'yicha HD screenshotlar va yakuniy **XULOSA rasm-jadvalini** avtomatik yaratadi.

2. **Hujjat Generator Moduli (`Docbot`):**
   - Shablonlar (`.docx`) asosida rasmiy ma'lumotnomalar (masalan: `🎓 1-kursga qabul ma'lumotnomasi`) va hujjatlarni savol-javob (FSM) orqali to'ldiradi.
   - Gotenberg + pypdfium2 yordamida asl logotip, pechat va imzolarni 100% saqlab, **300 DPI o'ta tiniq PNG rasm** hamda `.docx` hujjat shaklida yuboradi.

3. **Instagram to Telegram & YouTube Shorts AutoPoster Moduli:**
   - Instagram profilidagi (`@shahrisabz_t_t_uz`) barcha postlar, reels va rasmlarni xronologik tartibda (eng eskisidan yangisiga) skanerlaydi.
   - SQLite navbat tizimi (`atlas.db` -> `insta_posts_queue`) orqali Telegram kanal/botga HD sifatda (1080p/720p), tozalangan matn va jonli `[ ❤️ Like ]` / `[ 🔗 Instagramda ko'rish ]` tugmalari bilan yetkazadi.
   - **YouTube Shorts Integratsiyasi (Google Data API v3):** Instagram Reels videolarini moslashtirilgan sarlavha va `#Shorts` teglari bilan YouTube kanalga avtomatik joylaydi.
   - **Moslashuvchan Rek Vaqtlari Jadvali:** Admin bot orqali YouTube Shorts uchun kunlik eng qulay organik tarqalish ("Rek") vaqtlarini (masalan: `09:00`, `13:00`, `19:30`) o'zi erkin qo'shishi (`+`) yoki o'chirishi (`-`) mumkin.

4. **Yagona Admin Xavfsizligi (Single Admin Whitelist):**
   - Platforma 100% faqat tayinlangan Bosh Buxgalter Telegram ID si (`8135594558`) orqali ishlaydi.
   - Begona foydalanuvchilar kirganda menyu tugmalarini yo'qotadi (`ReplyKeyboardRemove`).

---

## 🛠️ 2. TEXNOLOGIK STEK VA KUTUBXONALAR (TECH STACK)

- **Dasturlash tili:** Python 3.10+
- **Telegram Bot Framework:** `pyTelegramBotAPI` (`telebot`)
- **Web Server / Webhook:** `Flask` (WSGI Micro-framework)
- **Excel Bilan Ishlash:** `openpyxl`
- **Hujjat To'ldirish (.docx):** `python-docx`
- **HD Rasm & PDF Konversiyasi:** `Pillow` (`PIL`), `pypdfium2`, `requests` (Gotenberg API)
- **Fuzzy Name Matching (Ismlarni Topish):** `fuzzywuzzy` + `python-Levenshtein`
- **Shriftlar:** Times New Roman Bold TTF (`fonts/TimesNewRomanBold.ttf`), `FreeSans.ttf`

---

## 📁 3. LOYIHA FAYLLAR TUZILMASI (PROJECT STRUCTURE)

```
kontrakt-bot/
├── bot.py                       # Birlashgan asosiy bot (Kontrakt + Docbot FSM logic)
├── docbot_config.py             # Docbot shablonlari va sozlamalari
├── requirements.txt             # Barcha kerakli Python kutubxonalari
├── vercel.json                  # Vercel serverless deploy konfiguratsiyasi
├── services/
│   ├── docx_filler.py           # .docx shablonni to'ldirish kodi (asl holicha)
│   ├── image_builder.py         # 300 DPI tiniq rasm konvertori (asl holicha)
│   ├── pdf_maker.py             # PDF & Pechat o'rnatish kodi (asl holicha)
│   └── pdf_builder.py           # ReportLab PDF yaratish kodi
├── templates/
│   ├── malumotnoma.docx         # 1-kurs qabul ma'lumotnomasi shablon fayli
│   ├── stamps/                  # Pechat va imzo rasmlari
│   └── fonts/                   # Shablon shriftlari
├── fonts/
│   ├── TimesNewRomanBold.ttf    # HD screenshotlar uchun asosiy Bold shrift
│   └── AppBoldFont.ttf         # Zaxira shrift
└── PROJECT_DOCUMENTATION.md     # Loyiha hujjatlari va yo'riqnomasi
```

---

## ⚙️ 4. YANGI HUJJAT SHABLONLARINI QO'SHISH

Agarda kelajakda yana yangi `.docx` shablon qo'shmoqchi bo'lsangiz:
1. Tayyor `.docx` faylingizni `templates/` papkasiga tashlaysiz (o'zgaruvchi joylarni `{{FIO}}`, `{{SANA}}` deb belgilaysiz).
2. `docbot_config.py` faylidagi `TEMPLATES` ro'yxatiga yangi shablon va uning savollarini qo'shasiz:

```python
TEMPLATES.append({
    "id": "yangi_hujjat",
    "name": "📄 Yangi ma'lumotnoma",
    "file": find_template_file("yangi_hujjat.docx"),
    "filename": "yangi_hujjat.docx",
    "steps": [
        {"field": "FIO", "question": "👤 F.I.O ni kiriting:", "buttons": None},
        {"field": "SANA", "question": "📅 Sanani kiriting:", "buttons": [[today_str]]}
    ]
})
```

---

✅ **Loyiha 100% yagona bot va yagona platformaga birlashtirildi va Vercel-da ishga tushirildi.**
