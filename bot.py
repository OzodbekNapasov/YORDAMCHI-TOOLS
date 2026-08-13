import telebot
from telebot import apihelper
import openpyxl
from datetime import datetime, timedelta
import os
import time
import tempfile
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN") or "8937819411:AAHrCwLyr_Ob3bM0ypwNFYP-SKb1weL97fs"

# PythonAnywhere bepul tarifida Telegram API proksi orqali ishlaydi
if os.path.exists('/var/www') or 'PYTHONANYWHERE_DOMAIN' in os.environ or 'PYTHONANYWHERE_SITE' in os.environ or 'pythonanywhere' in os.environ.get('HOME', ''):
    os.environ['http_proxy'] = 'http://proxy.server:3128'
    os.environ['https_proxy'] = 'http://proxy.server:3128'
    apihelper.proxy = {'http': 'http://proxy.server:3128', 'https': 'http://proxy.server:3128'}

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
user_data = {}

class TelegramProgress:
    """Uzoq davom etadigan jarayonlar uchun universal progress/loading bar tizimi"""
    def __init__(self, bot, chat_id, initial_status="⏳ Jarayon boshlandi..."):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = None
        self.current_percent = 0
        self.current_status = initial_status
        self.last_update_time = 0
        self.min_interval = 0.6  # Telegram edit limitlarini hisobga olish
        self._send_initial()

    def _render_bar(self, percent):
        blocks = int(round(percent / 10))
        filled = "🟩" * blocks
        empty = "⬜" * (10 - blocks)
        return f"{filled}{empty} {percent}%"

    def _send_initial(self):
        text = f"{self.current_status}\n{self._render_bar(0)}"
        try:
            msg = self.bot.send_message(self.chat_id, text, parse_mode="Markdown")
            self.message_id = msg.message_id
            self.last_update_time = time.time()
        except Exception:
            try:
                msg = self.bot.send_message(self.chat_id, text)
                self.message_id = msg.message_id
                self.last_update_time = time.time()
            except Exception:
                pass

    def update(self, status, percent, force=False):
        self.current_status = status
        self.current_percent = min(max(int(percent), 0), 100)
        now = time.time()

        if not force and (now - self.last_update_time < self.min_interval):
            return

        text = f"{self.current_status}\n{self._render_bar(self.current_percent)}"
        if self.message_id:
            try:
                self.bot.edit_message_text(text, self.chat_id, self.message_id, parse_mode="Markdown")
                self.last_update_time = now
            except Exception:
                try:
                    self.bot.edit_message_text(text, self.chat_id, self.message_id)
                    self.last_update_time = now
                except Exception:
                    pass

    def success(self, status="✅ Tayyor!"):
        self.update(status, 100, force=True)

    def error(self, err_msg="❌ Jarayonni bajarishda xatolik yuz berdi.\nQayta urinib ko‘ring."):
        if self.message_id:
            try:
                self.bot.edit_message_text(f"{err_msg}", self.chat_id, self.message_id)
            except Exception:
                pass

    def cancel(self, cancel_msg="⛔ Jarayon bekor qilindi."):
        if self.message_id:
            try:
                self.bot.edit_message_text(f"{cancel_msg}", self.chat_id, self.message_id)
            except Exception:
                pass

def get_main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("📝 Kontraktni yangilash")
    btn2 = telebot.types.KeyboardButton("📸 Guruh screenshotlarini olish")
    markup.add(btn1, btn2)
    return markup

def escape_md(text):
    """Telegram Markdown v1 uchun maxsus belgilarni zararsizlantirish"""
    if not text:
        return ""
    text = str(text)
    for char in ['_', '*', '`', '[']:
        text = text.replace(char, f"\\{char}")
    return text

def ismlarni_standartlash(ism):
    if not ism: return ""
    ism = str(ism).strip().lower()
    ism = ism.replace("`", "").replace("ʻ", "").replace("‘", "").replace("’", "").replace("'", "")
    ism = ism.replace("о‘", "o").replace("o‘", "o").replace("o'", "o").replace("о'", "o")
    ism = ism.replace("g‘", "g").replace("g'", "g").replace("г‘", "g")
    ism = ism.replace("ch", "c").replace("sh", "s")
    ism = ism.replace("x", "h").replace("ya", "a").replace("yu", "u")
    return "".join(ism.split())

def send_safe_message(chat_id, text):
    """Markdown xatosi bo'lsa tekis matnda yuborish (Crash oldini oladi)"""
    try:
        if len(text) <= 4000:
            bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())
        else:
            for i in range(0, len(text), 3900):
                bot.send_message(chat_id, text[i:i+3900], parse_mode="Markdown", reply_markup=get_main_keyboard())
    except Exception:
        for i in range(0, len(text), 3900):
            bot.send_message(chat_id, text[i:i+3900], reply_markup=get_main_keyboard())

def fmt_num(val):
    if val is None or val == "" or val == "-":
        return "-"
    try:
        fval = float(val)
        if fval == 0:
            return "-"
        return f"{int(round(fval)):,}".replace(",", " ")
    except Exception:
        return str(val)

def get_font_path(bold=True):
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf' if bold else '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
        r'C:\Windows\Fonts\tahomabd.ttf' if bold else r'C:\Windows\Fonts\tahoma.ttf',
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
        r'C:\Windows\Fonts\calibrib.ttf' if bold else r'C:\Windows\Fonts\calibri.ttf',
    ]
    for path in font_paths:
        if os.path.exists(path):
            return path
    return None

def get_font(size, bold=False, italic=False):
    font_file = get_font_path(bold=bold)
    if font_file:
        try:
            return ImageFont.truetype(font_file, size)
        except Exception:
            pass
    return ImageFont.load_default()

def generate_group_table_image(group_name, date_str, rows_data, output_path, header_bg_color=(0, 112, 192)):
    """Excel jadvali ko'rinishida pixel-perfect HD screenshot hosil qilish"""
    S = 3 # 3x Ultra HD Resolution
    col_w = [int(w * S) for w in [85, 48, 310, 210, 150, 175]]
    
    headers = [
        'GURUHI',
        '№',
        'Familiiyasi Ismi va Sharfi',
        'Shu vaqtgacha bo\'lishi\nkerak bo\'lgan to\'lov',
        'Jami',
        'Shu vaqtgacha\nqarzi'
    ]
    
    table_w = sum(col_w)
    title_h = int(36 * S)
    header_h = int(54 * S)
    row_h = int(28 * S)
    summary_h = int(36 * S)
    
    num_rows = len(rows_data)
    table_h = title_h + header_h + (num_rows * row_h) + summary_h
    
    margin = int(20 * S)
    img_w = table_w + 2 * margin
    img_h = table_h + 2 * margin
    
    img = Image.new('RGB', (img_w, img_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_file = get_font_path(bold=True)
    if font_file:
        try:
            font_bold = ImageFont.truetype(font_file, int(14 * S))
            font_title = ImageFont.truetype(font_file, int(16 * S))
        except Exception:
            font_bold = ImageFont.load_default()
            font_title = ImageFont.load_default()
    else:
        font_bold = ImageFont.load_default()
        font_title = ImageFont.load_default()
    
    grid_col = (0, 0, 0)
    border_w = 3
    
    ox = margin
    oy = margin
    
    # 1. Title Row
    draw.rectangle([ox, oy, ox + table_w, oy + title_h], fill=(255, 255, 255), outline=grid_col, width=border_w)
    title_str = f'Yangilangan sanasi:   {date_str}'
    
    bbox = font_title.getbbox(title_str) if hasattr(font_title, 'getbbox') else (0,0,220*S,16*S)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    tx = ox + (table_w - tw) // 2
    ty = oy + (title_h - th) // 2 - int(2 * S)
    draw.text((tx, ty), title_str, fill=(0, 0, 0), font=font_title)
    
    # 2. Header Row
    curr_y = oy + title_h
    curr_x = ox
    for idx, (h_text, w) in enumerate(zip(headers, col_w)):
        draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + header_h], fill=header_bg_color, outline=grid_col, width=border_w)
        lines = h_text.split('\n')
        line_y = curr_y + (header_h - (len(lines) * int(18 * S))) // 2
        for line in lines:
            bbox = font_bold.getbbox(line) if hasattr(font_bold, 'getbbox') else (0,0,len(line)*8*S,14*S)
            tw = bbox[2] - bbox[0]
            tx = curr_x + (w - tw) // 2
            draw.text((tx, line_y), line, fill=(255, 255, 255), font=font_bold)
            line_y += int(18 * S)
            
        curr_x += w

    # 3. Data Rows
    curr_y += header_h
    tot_kerak = 0.0
    tot_jami = 0.0
    tot_qarzi = 0.0
    
    for row_idx, rdata in enumerate(rows_data):
        curr_x = ox
        no_val = str(rdata.get('no', row_idx + 1))
        fio_val = str(rdata.get('fio', ''))
        kerak_num = rdata.get('kerak', 0.0)
        jami_num = rdata.get('jami', 0.0)
        qarzi_num = rdata.get('qarzi', 0.0)
        
        tot_kerak += kerak_num
        tot_jami += jami_num
        tot_qarzi += qarzi_num
        
        cells_info = [
            (group_name, 'center', (255,255,255), (0,0,0)),
            (no_val, 'center', (255,255,255), (0,0,0)),
            (fio_val, 'left', (255,255,255), (0,0,0)),
            (fmt_num(kerak_num), 'right', (255,255,255), (0,0,0)),
            (fmt_num(jami_num), 'right', (255,255,255), (0,0,0)),
        ]
        
        if qarzi_num > 0:
            debt_bg = (252, 228, 214) # #FCE4D6
            debt_fg = (192, 0, 0)     # Red
        else:
            debt_bg = (226, 239, 218) # #E2EFDA
            debt_fg = (55, 86, 35)    # Green
            
        cells_info.append((fmt_num(qarzi_num), 'right', debt_bg, debt_fg))
        
        for (c_text, align, bg_col, fg_col), w in zip(cells_info, col_w):
            draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + row_h], fill=bg_col, outline=grid_col, width=border_w)
            bbox = font_bold.getbbox(c_text) if hasattr(font_bold, 'getbbox') else (0,0,len(c_text)*8*S,14*S)
            tw = bbox[2] - bbox[0]
            
            if align == 'center':
                tx = curr_x + (w - tw) // 2
            elif align == 'right':
                tx = curr_x + w - tw - int(14 * S)
            else:
                tx = curr_x + int(12 * S)
                
            ty = curr_y + (row_h - int(16 * S)) // 2
            draw.text((tx, ty), c_text, fill=fg_col, font=font_bold)
            curr_x += w
            
        curr_y += row_h

    # 4. Summary Row (JAMI)
    curr_x = ox
    jami_w = col_w[0] + col_w[1] + col_w[2]
    draw.rectangle([curr_x, curr_y, curr_x + jami_w, curr_y + summary_h], fill=header_bg_color, outline=grid_col, width=border_w)
    bbox = font_bold.getbbox('JAMI') if hasattr(font_bold, 'getbbox') else (0,0,32*S,14*S)
    tw = bbox[2] - bbox[0]
    draw.text((curr_x + (jami_w - tw) // 2, curr_y + int(9 * S)), 'JAMI', fill=(255, 255, 255), font=font_bold)
    curr_x += jami_w
    
    summary_cols = [
        (fmt_num(tot_kerak), col_w[3]),
        (fmt_num(tot_jami), col_w[4]),
        (fmt_num(tot_qarzi), col_w[5]),
    ]
    for c_text, w in summary_cols:
        draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + summary_h], fill=header_bg_color, outline=grid_col, width=border_w)
        bbox = font_bold.getbbox(c_text) if hasattr(font_bold, 'getbbox') else (0,0,len(c_text)*8*S,14*S)
        tw = bbox[2] - bbox[0]
        tx = curr_x + w - tw - int(14 * S)
        draw.text((tx, curr_y + int(9 * S)), c_text, fill=(255, 255, 255), font=font_bold)
        curr_x += w
        
    img.save(output_path, 'PNG', quality=100)
    return output_path

# Webhook Marshrutlari
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    import sys, json as _json, traceback as _tb
    try:
        raw = request.get_data().decode('utf-8')
        data = _json.loads(raw)
        msg = data.get('message') or {}
        print(f"WEBHOOK: chat={msg.get('chat',{}).get('id')} text={msg.get('text','')}", file=sys.stderr, flush=True)
        update = telebot.types.Update.de_json(raw)
        bot.process_new_updates([update])
        print("WEBHOOK: done", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"WEBHOOK ERR: {e}", file=sys.stderr, flush=True)
        _tb.print_exc(file=sys.stderr)
    return "!", 200

@app.route("/")
def webhook():
    return "✅ Bot PythonAnywhere/Vercel bulutida 24/7 faol!", 200

@app.route("/set_webhook", methods=['GET'])
def set_webhook_route():
    host_url = request.host_url.rstrip('/')
    webhook_url = f"{host_url}/{TOKEN}"
    try:
        bot.remove_webhook()
        success = bot.set_webhook(url=webhook_url)
        if success:
            return f"<h3>✅ Webhook muvaffaqiyatli o'rnatildi!</h3><p>URL: <b>{webhook_url}</b></p><p>Endi Telegram botingizga /start yuborib tekshirishingiz mumkin.</p>", 200
        else:
            return "<h3>❌ Webhook o'rnatilmadi!</h3>", 500
    except Exception as e:
        return f"<h3>❌ Xatolik: {str(e)}</h3>", 500

@app.route("/delete_webhook", methods=['GET'])
def delete_webhook_route():
    try:
        success = bot.remove_webhook(drop_pending_updates=True)
        if success:
            return "<h3>✅ Webhook muvaffaqiyatli uzildi va o'chirildi!</h3>", 200
        else:
            return "<h3>❌ Webhook uzib bo'lmadi!</h3>", 500
    except Exception as e:
        return f"<h3>❌ Xatolik: {str(e)}</h3>", 500

@app.route("/webhook_info", methods=['GET'])
def webhook_info():
    try:
        info = bot.get_webhook_info()
        return jsonify({
            "url": info.url,
            "has_custom_certificate": info.has_custom_certificate,
            "pending_update_count": info.pending_update_count,
            "last_error_date": info.last_error_date,
            "last_error_message": info.last_error_message,
            "max_connections": info.max_connections,
            "ip_address": info.ip_address
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Telegram Bot Handlerlari
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "Salom! Aqlli kontrakt va guruhlar platformasi faol. 🚀\n\n"
                              "Kerakli bo'limni tanlang:", reply_markup=get_main_keyboard())

# 1-KETMA-KETLIK: Kontraktni yangilash jarayoni (Baza -> Debitorka -> Sana)
@bot.message_handler(func=lambda message: message.text == "📝 Kontraktni yangilash")
def start_kontrakt_yangilash(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"holat": "baza_kutish"}
    bot.send_message(chat_id, "📑 *1-BOSQICH: ASOSIY BAZANI YUKLASH*\n\n"
                              "Iltimos, kontraktlar kiritilgan asosiy *.xlsx* faylingizni yuboring:", 
                     parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: message.text == "📸 Guruh screenshotlarini olish")
def start_guruh_screenshot(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"holat": "guruh_fayl_kutish"}
    bot.send_message(chat_id, "📸 *GURUH SCREENSHOTLARINI OLISH*\n\n"
                              "Guruhlar screenshotlarini olish uchun tayyorlangan Excel (*.xlsx*) faylingizni yuboring:", 
                     parse_mode="Markdown", reply_markup=get_main_keyboard())

# Matnli xabarlar handler (Boshlanish sanasi va boshqalar)
@bot.message_handler(func=lambda message: message.content_type == 'text' and not message.text.startswith('/'))
def handle_text_messages(message):
    chat_id = message.chat.id
    holat = user_data.get(chat_id, {}).get("holat")

    if holat == "sana_kutish":
        sana_matni = message.text.strip()
        try:
            cheklov_sanasi = datetime.strptime(sana_matni, "%d.%m.%Y")
            user_data[chat_id]["sana"] = cheklov_sanasi
            
            # Sanadan so'ng hisob-kitob jarayonini boshlash
            baza_path = user_data[chat_id].get("baza_path")
            deb_path = user_data[chat_id].get("deb_path")

            if not baza_path or not os.path.exists(baza_path) or not deb_path or not os.path.exists(deb_path):
                bot.reply_to(message, "❌ Yuklangan fayllar topilmadi. Qayta urinib ko'ring.", reply_markup=get_main_keyboard())
                user_data[chat_id] = {}
                return

            process_kontrakt_update(chat_id, baza_path, deb_path, cheklov_sanasi)
            user_data[chat_id] = {}

        except ValueError:
            bot.reply_to(message, "❌ Noto'g'ri sana formati. Nuqtalar bilan kiriting (Masalan: `27.06.2026`):", parse_mode="Markdown", reply_markup=get_main_keyboard())

# Fayl yuklanganda ishlovchi handler
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    holat = user_data.get(chat_id, {}).get("holat")

    if not holat:
        bot.reply_to(message, "Iltimos, avval menyudan kerakli tugmani tanlang:", reply_markup=get_main_keyboard())
        return

    # GURUH SCREENSHOTLARINI OLISH
    if holat == "guruh_fayl_kutish":
        process_group_screenshots(chat_id, message)
        return

    # KONTRAKTNI YANGILASH: 1-BOSQICH (ASOSIY BAZA YUKLANDI)
    if holat == "baza_kutish":
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            baza_nomi = os.path.join(tempfile.gettempdir(), f"baza_{chat_id}.xlsx")
            with open(baza_nomi, 'wb') as f:
                f.write(downloaded_file)

            user_data[chat_id]["baza_path"] = baza_nomi
            user_data[chat_id]["holat"] = "deb_kutish"

            bot.send_message(chat_id, "✅ *Asosiy baza qabul qilindi!*\n\n"
                                      "📥 *2-BOSQICH: BANK DEBITORKASINI YUKLASH*\n\n"
                                      "Endi bankdan kelgan yangi *Debitorka (.xlsx)* faylini yuboring:", 
                             parse_mode="Markdown", reply_markup=get_main_keyboard())
        except Exception as e:
            bot.send_message(chat_id, f"❌ Faylni yuklashda xatolik: `{str(e)}`", parse_mode="Markdown", reply_markup=get_main_keyboard())
            user_data[chat_id] = {}
        return

    # KONTRAKTNI YANGILASH: 2-BOSQICH (DEBITORKA YUKLANDI)
    if holat == "deb_kutish":
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            deb_nomi = os.path.join(tempfile.gettempdir(), f"deb_{chat_id}.xlsx")
            with open(deb_nomi, 'wb') as f:
                f.write(downloaded_file)

            user_data[chat_id]["deb_path"] = deb_nomi
            user_data[chat_id]["holat"] = "sana_kutish"

            bot.send_message(chat_id, "✅ *Bank debitorkasi qabul qilindi!*\n\n"
                                      "📅 *3-BOSQICH: BOSHLANISH SANASI*\n\n"
                                      "To'lovlarni *qaysi sanadan boshlab* hisoblayin?\n"
                                      "Format: `27.06.2026` shaklida yozing:", 
                             parse_mode="Markdown", reply_markup=get_main_keyboard())
        except Exception as e:
            bot.send_message(chat_id, f"❌ Faylni yuklashda xatolik: `{str(e)}`", parse_mode="Markdown", reply_markup=get_main_keyboard())
            user_data[chat_id] = {}
        return

def process_kontrakt_update(chat_id, baza_path, deb_nomi, cheklov_sanasi):
    """Kontraktlarni yangilash va hisobot tayyorlash (Real Progress bilan)"""
    progress = TelegramProgress(bot, chat_id, "⏳ Jarayon boshlandi...")
    natija_nomi = os.path.join(tempfile.gettempdir(), f"Tayyor_Yangilangan_{chat_id}.xlsx")

    try:
        progress.update("📥 Ma'lumotlar olinmoqda...", 10)
        
        wb_baza_write = openpyxl.load_workbook(baza_path, data_only=False)
        wb_baza_read = openpyxl.load_workbook(baza_path, data_only=True)
        wb_deb = openpyxl.load_workbook(deb_nomi, data_only=True)

        varoq_nomi = 'KONTRAKTLAR' if 'KONTRAKTLAR' in wb_baza_write.sheetnames else wb_baza_write.sheetnames[0]
        sheet_write = wb_baza_write[varoq_nomi]
        sheet_read = wb_baza_read[varoq_nomi]
        sheet_deb = wb_deb['bank'] if 'bank' in wb_deb.sheetnames else wb_deb.active

        progress.update("🧠 Ma'lumotlar tahlil qilinmoqda...", 25)

        ism_ustun = 3
        tolov_ustun = 5
        boshlanish_row = 25

        for r in range(1, 30):
            for c in range(1, 15):
                val = str(sheet_read.cell(row=r, column=c).value or "").lower()
                if any(x in val for x in ['familiya', 'f.i.sh', 'ism', 'sharfi']):
                    ism_ustun = c
                    boshlanish_row = r + 1
                if any(x in val for x in ['jami', 'to\'lagan summasi', 'to\'lov']):
                    tolov_ustun = c

        guruh_ustun = ism_ustun - 1 if ism_ustun > 1 else 2

        baza_talabalari = []
        for row in range(boshlanish_row, sheet_read.max_row + 1):
            fio = sheet_read.cell(row=row, column=ism_ustun).value
            if fio and str(fio).strip() and not str(fio).lower().startswith(('familiya', 'f.i.sh', 'итого', 'jami', 'guruh')):
                guruh_val = sheet_read.cell(row=row, column=guruh_ustun).value
                guruh_str = str(guruh_val).strip() if guruh_val else "Noma'lum"
                if guruh_str.endswith('.0'): guruh_str = guruh_str[:-2]

                eski_val = sheet_read.cell(row=row, column=tolov_ustun).value
                try:
                    eski_sum = float(eski_val) if eski_val else 0.0
                except (ValueError, TypeError):
                    eski_sum = 0.0

                baza_talabalari.append({
                    "row": row,
                    "original_name": str(fio).strip(),
                    "clean_name": ismlarni_standartlash(fio),
                    "guruh": guruh_str,
                    "boshlangich_summa": eski_sum,
                    "joriy_summa": eski_sum
                })

        yangilanish_tarixi = []
        topilmaganlar = []
        jami_tushgan_pul = 0.0
        oxirgi_to_lov_sanasi = None
        yangilangan_talabalar_set = set()
        
        max_deb_rows = sheet_deb.max_row
        for row_idx, row in enumerate(range(2, max_deb_rows + 1), start=1):
            # Real progress dinamik yangilanishi (25% dan 75% gacha)
            current_pct = 25 + int((row_idx / max(max_deb_rows - 1, 1)) * 50)
            progress.update("🧠 Ma'lumotlar tahlil qilinmoqda...", current_pct)

            sana_val = sheet_deb.cell(row=row, column=1).value
            if not sana_val: continue

            try:
                if isinstance(sana_val, str):
                    if '.' in sana_val:
                        to_lov_sanasi = datetime.strptime(sana_val.strip(), "%d.%m.%y")
                    else:
                        to_lov_sanasi = datetime.strptime(sana_val.strip(), "%Y-%m-%d %H:%M:%S")
                elif isinstance(sana_val, datetime):
                    to_lov_sanasi = sana_val
                else:
                    continue
            except ValueError:
                continue

            if to_lov_sanasi >= cheklov_sanasi:
                summa_val = sheet_deb.cell(row=row, column=7).value
                h_val = sheet_deb.cell(row=row, column=8).value
                deb_fio = sheet_deb.cell(row=row, column=9).value

                deb_fio_str = str(deb_fio).strip() if deb_fio else ""
                h_str = str(h_val).strip() if h_val else ""

                if not deb_fio_str and not h_str: continue
                if not summa_val: continue

                try:
                    yangi_summa = float(summa_val)
                except (ValueError, TypeError):
                    continue

                if oxirgi_to_lov_sanasi is None or to_lov_sanasi > oxirgi_to_lov_sanasi:
                    oxirgi_to_lov_sanasi = to_lov_sanasi

                deb_fio_clean = ismlarni_standartlash(deb_fio_str or h_str)
                eng_yaxshi_moslik = None
                eng_yuqori_ball = 0

                for talaba in baza_talabalari:
                    ball = fuzz.token_sort_ratio(deb_fio_clean, talaba["clean_name"])
                    if ball > eng_yuqori_ball:
                        eng_yuqori_ball = ball
                        eng_yaxshi_moslik = talaba

                if eng_yaxshi_moslik and eng_yuqori_ball >= 75:
                    target_row = eng_yaxshi_moslik["row"]
                    
                    eski_summa = eng_yaxshi_moslik["joriy_summa"]
                    jami_yangi = eski_summa + yangi_summa
                    
                    sheet_write.cell(row=target_row, column=tolov_ustun).value = jami_yangi
                    eng_yaxshi_moslik["joriy_summa"] = jami_yangi
                    
                    jami_tushgan_pul += yangi_summa
                    yangilangan_talabalar_set.add(eng_yaxshi_moslik['original_name'])

                    safe_orig_name = escape_md(eng_yaxshi_moslik['original_name'])
                    safe_guruh = escape_md(eng_yaxshi_moslik['guruh'])
                    safe_deb_fio = escape_md(deb_fio_str or h_str)
                    safe_sana = to_lov_sanasi.strftime('%d.%m.%Y')
                    
                    yangilanish_tarixi.append(
                        f"👤 *{safe_orig_name}*\n"
                        f"├ 🏦 Debitorkada: `{safe_deb_fio}`\n"
                        f"├ 🏫 Guruh: `{safe_guruh}`\n"
                        f"├ 📅 Toʻlov sanasi: `{safe_sana}`\n"
                        f"├ ➕ Tushgan pul: `{yangi_summa:,.0f} so'm`\n"
                        f"└ 📊 Jami toʻladi: `{jami_yangi:,.0f} so'm`"
                    )
                else:
                    if h_str and deb_fio_str and h_str != deb_fio_str and deb_fio_str != "?":
                        disp_name = f"{deb_fio_str} | {h_str}"
                    elif h_str:
                        disp_name = h_str
                    else:
                        disp_name = deb_fio_str or "Noma'lum"

                    safe_disp_name = escape_md(disp_name)
                    safe_sana = to_lov_sanasi.strftime('%d.%m.%Y')
                    topilmaganlar.append(f"❓ `{safe_disp_name}` — `{yangi_summa:,.0f} so'm` (Sana: {safe_sana})")

        progress.update("⚙️ Natija tayyorlanmoqda...", 85)
        wb_baza_write.save(natija_nomi)
        wb_baza_write.close()
        wb_baza_read.close()
        wb_deb.close()

        progress.update("🔍 Yakuniy tekshiruv...", 95)

        oxirgi_sana_str = oxirgi_to_lov_sanasi.strftime('%d.%m.%Y') if oxirgi_to_lov_sanasi else cheklov_sanasi.strftime('%d.%m.%Y')
        keyingi_sana_dt = (oxirgi_to_lov_sanasi or cheklov_sanasi) + timedelta(days=1)
        keyingi_sana_str = keyingi_sana_dt.strftime('%d.%m.%Y')

        hisobot_matni = f"📊 *KONTRAKT YANGILANISH HISOBOTI*\n"
        hisobot_matni += f"📅 Filtr sanasi: {cheklov_sanasi.strftime('%d.%m.%Y')} dan {oxirgi_sana_str} gacha\n"
        hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n"
        hisobot_matni += f"💰 *Jami tushgan pul:* `{jami_tushgan_pul:,.0f} so'm`\n"
        hisobot_matni += f"👥 *Muvaffaqiyatli yangilandi:* {len(yangilangan_talabalar_set)} kishi\n"
        hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if yangilanish_tarixi:
            hisobot_matni += f"✅ *Yangilangan talabalar ({len(yangilanish_tarixi)} ta):*\n\n"
            for t in yangilanish_tarixi:
                hisobot_matni += t + "\n\n"
        else:
            hisobot_matni += "❌ Yangi to'lovlar topilmadi.\n\n"

        if topilmaganlar:
            hisobot_matni += f"❓ *Umuman topilmagan ismlar ({len(topilmaganlar)} ta):*\n"
            for top in topilmaganlar:
                hisobot_matni += top + "\n"
            hisobot_matni += "\n"

        hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n"
        hisobot_matni += f"💡 *Keyingi safar adashmasligingiz uchun eslatma:*\n"
        hisobot_matni += f"Navbatdagi debitorkani yuklaganingizda botga boshlanish sanasi sifatida `{keyingi_sana_str}` sanasini kiriting."

        with open(natija_nomi, 'rb') as f_send:
            bot.send_document(chat_id, f_send, caption="📄 Formulalari buzilmagan tayyor Excel faylingiz.", reply_markup=get_main_keyboard())
        
        send_safe_message(chat_id, hisobot_matni)
        progress.success("✅ Tayyor!")

        if os.path.exists(baza_path): os.remove(baza_path)
        if os.path.exists(deb_nomi): os.remove(deb_nomi)
        if os.path.exists(natija_nomi): os.remove(natija_nomi)

    except Exception as e:
        progress.error(f"❌ Jarayonni bajarishda xatolik yuz berdi:\n`{str(e)}`")
        if os.path.exists(baza_path): os.remove(baza_path)
        if os.path.exists(deb_nomi): os.remove(deb_nomi)
        if os.path.exists(natija_nomi): os.remove(natija_nomi)

def process_group_screenshots(chat_id, message):
    """Guruhlar screenshotlarini olish jarayoni (Real Progress bilan)"""
    progress = TelegramProgress(bot, chat_id, "⏳ Jarayon boshlandi...")
    temp_excel = os.path.join(tempfile.gettempdir(), f"temp_guruh_{chat_id}.xlsx")

    try:
        progress.update("📥 Ma'lumotlar olinmoqda...", 10)

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(temp_excel, 'wb') as f:
            f.write(downloaded_file)

        wb = openpyxl.load_workbook(temp_excel, data_only=True)
        sheet = wb.active

        progress.update("🧠 Guruhlar tahlil qilinmoqda...", 25)

        header_row = 22
        date_str = datetime.now().strftime("%d.%m.%Y")

        for r in range(1, 30):
            val_a = str(sheet.cell(row=r, column=1).value or "").lower()
            val_c = str(sheet.cell(row=r, column=3).value or "").lower()
            if "guruh" in val_a or "familiy" in val_c:
                header_row = r
                break
            for c in range(1, 10):
                cell_val = str(sheet.cell(row=r, column=c).value or "")
                if "yangilangan sanasi" in cell_val.lower():
                    next_cell = sheet.cell(row=r, column=c+1).value or sheet.cell(row=r, column=c+2).value
                    if next_cell:
                        if isinstance(next_cell, datetime):
                            date_str = next_cell.strftime("%d.%m.%Y")
                        else:
                            date_str = str(next_cell).strip()

        guruhlar = {}
        for r in range(header_row + 1, sheet.max_row + 1):
            guruh_val = sheet.cell(row=r, column=1).value
            fio_val = sheet.cell(row=r, column=3).value

            if not guruh_val or not fio_val: continue
            
            g_name = str(guruh_val).strip()
            if g_name.endswith('.0'): g_name = g_name[:-2]
            if g_name.lower().startswith(('jami', 'итого', 'guruh')): continue

            no_val = sheet.cell(row=r, column=2).value or len(guruhlar.get(g_name, [])) + 1
            kerak_val = sheet.cell(row=r, column=4).value or 0
            jami_val = sheet.cell(row=r, column=5).value or 0
            qarzi_val = sheet.cell(row=r, column=6).value or 0

            try: kerak_num = float(kerak_val)
            except: kerak_num = 0.0

            try: jami_num = float(jami_val)
            except: jami_num = 0.0

            try: qarzi_num = float(qarzi_val)
            except: qarzi_num = 0.0

            if g_name not in guruhlar:
                guruhlar[g_name] = []

            guruhlar[g_name].append({
                "no": no_val,
                "fio": str(fio_val).strip(),
                "kerak": kerak_num,
                "jami": jami_num,
                "qarzi": qarzi_num
            })

        wb.close()
        if os.path.exists(temp_excel): os.remove(temp_excel)

        if not guruhlar:
            progress.error("❌ Excel faylidan guruhlar ma'lumotlari topilmadi.")
            user_data[chat_id] = {}
            return

        guruh_nomlari = sorted(guruhlar.keys())
        total_g = len(guruh_nomlari)

        progress.update("⚙️ Natija tayyorlanmoqda...", 40)

        for idx, g_name in enumerate(guruh_nomlari, start=1):
            pct = 40 + int((idx / total_g) * 50)
            progress.update(f"⚙️ {g_name} guruhi tayyorlanmoqda...", pct)

            rows_data = guruhlar[g_name]
            img_path = os.path.join(tempfile.gettempdir(), f"screenshot_{chat_id}_{g_name}.png")
            
            generate_group_table_image(g_name, date_str, rows_data, img_path)
            
            with open(img_path, 'rb') as photo_f:
                bot.send_photo(chat_id, photo=photo_f, caption=f"📊 *Guruh: {g_name}*", parse_mode="Markdown")
            
            if os.path.exists(img_path): os.remove(img_path)

        progress.update("🔍 Yakuniy tekshiruv...", 95)
        bot.send_message(chat_id, f"✅ *Barcha {len(guruh_nomlari)} ta guruh screenshotlari muvaffaqiyatli yuborildi!*", parse_mode="Markdown", reply_markup=get_main_keyboard())
        progress.success("✅ Tayyor!")
        user_data[chat_id] = {}

    except Exception as e:
        progress.error(f"❌ Xatolik yuz berdi:\n`{str(e)}`")
        if os.path.exists(temp_excel): os.remove(temp_excel)
        user_data[chat_id] = {}

if __name__ == "__main__":
    bot.remove_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))