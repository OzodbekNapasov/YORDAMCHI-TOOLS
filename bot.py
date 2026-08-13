import telebot
from telebot import apihelper
import openpyxl
from datetime import datetime, timedelta
import os
import time
import tempfile
import html
import re
import json
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN") or "8937819411:AAHrCwLyr_Ob3bM0ypwNFYP-SKb1weL97fs"
BOT_VERSION = "1.5.0"

def is_user_allowed(message):
    """Faqat ruxsat berilgan yagona foydalanuvchi ishlata olishini ta'minlash"""
    user_id = message.from_user.id
    username = (message.from_user.username or "").strip().lower()

    # Environment variable orqali ALLOWED_USERS belgilangan bo'lsa
    env_users = os.environ.get("ALLOWED_USERS", "").strip()
    if env_users:
        allowed_list = [i.strip().lower() for i in env_users.split(",") if i.strip()]
        if str(user_id) in allowed_list or (username and f"@{username}" in allowed_list) or (username and username in allowed_list):
            return True
        return False

    # Faylda saqlangan adminlar ro'yxati
    admins_file = os.path.join(tempfile.gettempdir(), "allowed_admins.json")
    admins = []
    if os.path.exists(admins_file):
        try:
            with open(admins_file, "r") as f:
                admins = json.load(f)
        except Exception:
            admins = []

    if not admins:
        # Birinchi bo'lib muloqot qilgan foydalanuvchi avtomatik admin bo'ladi
        admins.append(user_id)
        try:
            with open(admins_file, "w") as f:
                json.dump(admins, f)
        except Exception:
            pass
        return True

    return user_id in admins

def send_access_denied(chat_id, user_id):
    msg = f"⛔ <b>RUXSAT BERILMAGAN!</b>\n\n" \
          f"Kechirasiz, ushbu bot faqat ruxsat berilgan yagona foydalanuvchi (buxgalter) uchun mo'ljallangan.\n\n" \
          f"🔑 Sizning Telegram ID: <code>{user_id}</code>\n" \
          f"<i>Ushbu ID ni bot egalariga taqdim etib ruxsat berilishi mumkin.</i>"
    bot.send_message(chat_id, msg, parse_mode="HTML")

def save_user_chat_id(chat_id):
    """Foydalanuvchi chat ID sini saqlash"""
    try:
        chats_file = os.path.join(tempfile.gettempdir(), "user_chats.json")
        chats = set()
        if os.path.exists(chats_file):
            with open(chats_file, "r") as f:
                chats = set(json.load(f))
        chats.add(chat_id)
        with open(chats_file, "w") as f:
            json.dump(list(chats), f)
    except Exception:
        pass

def check_and_notify_updates():
    """Yangi versiya chiqqanda foydalanuvchilarga avtomatik yangilanish xabarini yuborish"""
    try:
        ver_file = os.path.join(tempfile.gettempdir(), "last_notified_version.txt")
        last_ver = ""
        if os.path.exists(ver_file):
            with open(ver_file, "r") as f:
                last_ver = f.read().strip()

        if last_ver != BOT_VERSION:
            chats_file = os.path.join(tempfile.gettempdir(), "user_chats.json")
            if os.path.exists(chats_file):
                with open(chats_file, "r") as f:
                    chats = json.load(f)
                
                update_msg = f"🔔 <b>TIZIMDA YANGI YANGILANISH! (v{BOT_VERSION})</b>\n\n" \
                             f"✨ <b>Yangi o'zgarishlar va imkoniyatlar:</b>\n" \
                             f"• 📊 <b>Avtomatik XULOSA hisobot rasm:</b> Kontrakt yangilanishi yakunida barcha guruh rahbarlari, guruhlar, talabalar soni va umumiy qarzdorlik jamlanmasi rasmi o'zi yuboriladi!\n" \
                             f"• 📏 <b>Familiyalar kengligi oshirildi:</b> Eng uzun ismlar ham jadvalga 100% to'liq va shinam sig'ib tushadi.\n\n" \
                             f"<i>Platformadan bemalol foydalanishingiz mumkin! 🚀</i>"

                for cid in chats:
                    try:
                        bot.send_message(cid, update_msg, parse_mode="HTML", reply_markup=get_main_keyboard())
                    except Exception:
                        pass

            with open(ver_file, "w") as f:
                f.write(BOT_VERSION)
    except Exception as e:
        print(f"NOTIFY ERR: {e}")

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
            msg = self.bot.send_message(self.chat_id, text, parse_mode="HTML")
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
                self.bot.edit_message_text(text, self.chat_id, self.message_id, parse_mode="HTML")
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

def get_main_keyboard(suggested_date=None):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if suggested_date:
        btn_date = telebot.types.KeyboardButton(suggested_date)
        markup.add(btn_date)
    btn1 = telebot.types.KeyboardButton("📝 Kontraktni yangilash")
    btn2 = telebot.types.KeyboardButton("📸 Guruh screenshotlarini olish")
    markup.add(btn1, btn2)
    return markup

def escape_html_text(text):
    """HTML rejimida maxsus belgilarni xavfsiz qilish"""
    if not text:
        return ""
    return html.escape(str(text))

def cyrillic_to_latin(text):
    """Kirill alifbosidagi ismlarni Lotin alifbosiga o'tkazish"""
    if not text: return ""
    text = str(text)
    trans = {
        'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'j','з':'z','и':'i',
        'й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t',
        'у':'u','ф':'f','х':'h','ц':'c','ч':'ch','ш':'sh','щ':'sh','ъ':'','ы':'y','ь':'',
        'э':'e','ю':'yu','я':'ya','ў':'o','ғ':'g','қ':'q','ҳ':'h',
        'А':'a','Б':'b','В':'v','Г':'g','Д':'d','Е':'e','Ё':'yo','Ж':'j','З':'z','И':'i',
        'Й':'y','К':'k','Л':'l','М':'m','Н':'n','О':'o','П':'p','Р':'r','С':'s','Т':'t',
        'У':'u','Ф':'f','Х':'h','Ц':'c','Ч':'ch','Ш':'sh','Щ':'sh','Ъ':'','Ы':'y','Ь':'',
        'Э':'e','Ю':'yu','Я':'ya','Ў':'o','Ғ':'g','Қ':'q','Ҳ':'h'
    }
    for k, v in trans.items():
        text = text.replace(k, v)
    return text

def ismlarni_standartlash(ism):
    """Ismlarni taqqoslash uchun tozalash va standartlash"""
    if not ism: return ""
    ism = cyrillic_to_latin(ism).strip().lower()
    ism = ism.replace("`", "").replace("ʻ", "").replace("‘", "").replace("’", "").replace("'", "")
    ism = ism.replace("о‘", "o").replace("o‘", "o").replace("o'", "o").replace("о'", "o")
    ism = ism.replace("g‘", "g").replace("g'", "g").replace("г‘", "g")
    ism = ism.replace("ch", "c").replace("sh", "s").replace("x", "h").replace("ya", "a").replace("yu", "u")
    return "".join(c for c in ism if c.isalpha() or c.isspace())

def send_safe_message(chat_id, text, reply_markup=None):
    """HTML rejimida xabarni HTML taglarini buzmasdan aqlli bo'lib yuborish"""
    if reply_markup is None:
        reply_markup = get_main_keyboard()

    if len(text) <= 3800:
        try:
            bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=reply_markup)
            return
        except Exception:
            try:
                bot.send_message(chat_id, text, reply_markup=reply_markup)
                return
            except Exception:
                pass

    blocks = text.split("<blockquote>")
    current_chunk = blocks[0]

    for block in blocks[1:]:
        formatted_block = "<blockquote>" + block
        if len(current_chunk) + len(formatted_block) > 3700:
            try:
                bot.send_message(chat_id, current_chunk.strip(), parse_mode="HTML", reply_markup=reply_markup)
            except Exception:
                bot.send_message(chat_id, current_chunk.strip(), reply_markup=reply_markup)
            current_chunk = formatted_block
        else:
            current_chunk += formatted_block

    if current_chunk.strip():
        try:
            bot.send_message(chat_id, current_chunk.strip(), parse_mode="HTML", reply_markup=reply_markup)
        except Exception:
            bot.send_message(chat_id, current_chunk.strip(), reply_markup=reply_markup)

def fmt_num(val):
    if val is None or val == "" or val == "-":
        return "-"
    try:
        fval = float(val)
        if fval == 0:
            return "0"
        return f"{int(round(fval)):,}".replace(",", " ")
    except Exception:
        return str(val)

def get_font(size, bold=True):
    bundled_tnr = os.path.join(os.path.dirname(__file__), 'fonts', 'TimesNewRomanBold.ttf')
    if os.path.exists(bundled_tnr):
        try:
            return ImageFont.truetype(bundled_tnr, size)
        except Exception:
            pass

    bundled_font = os.path.join(os.path.dirname(__file__), 'fonts', 'AppBoldFont.ttf')
    if os.path.exists(bundled_font):
        try:
            return ImageFont.truetype(bundled_font, size)
        except Exception:
            pass

    font_paths = [
        '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf' if bold else '/usr/share/fonts/truetype/freefont/FreeSerif.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        r'C:\Windows\Fonts\timesbd.ttf' if bold else r'C:\Windows\Fonts\times.ttf',
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()

def generate_group_table_image(group_name, date_str, rows_data, output_path, header_bg_color=(0, 112, 192)):
    """Times New Roman shriftida pixel-perfect HD screenshot hosil qilish (v1.4.0)"""
    S = 3 # 3x Ultra HD Resolution
    col_w = [int(w * S) for w in [110, 60, 520, 310, 230, 250]]
    
    headers = [
        'GURUHI',
        '№',
        'Familiiyasi Ismi va Sharfi',
        'Shu vaqtgacha bo\'lishi\nkerak bo\'lgan to\'lov',
        'Jami',
        'Shu vaqtgacha\nqarzi'
    ]
    
    table_w = sum(col_w)
    title_h = int(55 * S)
    header_h = int(75 * S)
    row_h = int(42 * S)
    summary_h = int(50 * S)
    
    num_rows = len(rows_data)
    table_h = title_h + header_h + (num_rows * row_h) + summary_h
    
    margin = int(24 * S)
    img_w = table_w + 2 * margin
    img_h = table_h + 2 * margin
    
    img = Image.new('RGB', (img_w, img_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_cell = get_font(int(24 * S), bold=True)
    font_title = get_font(int(30 * S), bold=True)
    font_header = get_font(int(24 * S), bold=True)
    font_summary = get_font(int(25 * S), bold=True)
    
    grid_col = (0, 0, 0)
    border_w = int(3 * S // 2)
    
    ox, oy = margin, margin
    
    # 1. Title Row
    draw.rectangle([ox, oy, ox + table_w, oy + title_h], fill=(255, 255, 255), outline=grid_col, width=border_w)
    title_str = f'Yangilangan sanasi:   {date_str}'
    bbox = font_title.getbbox(title_str)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((ox + (table_w - tw) // 2, oy + (title_h - th) // 2 - bbox[1]), title_str, fill=(0, 0, 0), font=font_title)
    
    # 2. Header Row
    curr_y = oy + title_h
    curr_x = ox
    for idx, (h_text, w) in enumerate(zip(headers, col_w)):
        draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + header_h], fill=header_bg_color, outline=grid_col, width=border_w)
        lines = h_text.split('\n')
        total_lines_h = len(lines) * int(28 * S)
        line_y = curr_y + (header_h - total_lines_h) // 2
        for line in lines:
            bbox = font_header.getbbox(line)
            tw = bbox[2] - bbox[0]
            tx = curr_x + (w - tw) // 2
            draw.text((tx, line_y - bbox[1]), line, fill=(255, 255, 255), font=font_header)
            line_y += int(28 * S)
        curr_x += w

    # 3. Data Rows
    curr_y += header_h
    tot_kerak, tot_jami, tot_qarzi_musbat = 0.0, 0.0, 0.0
    
    for row_idx, rdata in enumerate(rows_data):
        curr_x = ox
        no_val = str(rdata.get('no', row_idx + 1))
        fio_val = str(rdata.get('fio', ''))
        kerak_num = rdata.get('kerak', 0.0)
        jami_num = rdata.get('jami', 0.0)
        qarzi_num = rdata.get('qarzi', 0.0)
        
        tot_kerak += kerak_num
        tot_jami += jami_num
        if qarzi_num > 0:
            tot_qarzi_musbat += qarzi_num
        
        cells_info = [
            (group_name, 'center', (255,255,255), (0,0,0)),
            (no_val, 'center', (255,255,255), (0,0,0)),
            (fio_val, 'left', (255,255,255), (0,0,0)),
            (fmt_num(kerak_num), 'right', (255,255,255), (0,0,0)),
            (fmt_num(jami_num), 'right', (255,255,255), (0,0,0)),
        ]
        
        if qarzi_num > 0:
            debt_bg = (255, 199, 206)
            debt_fg = (156, 0, 6)
        else:
            debt_bg = (198, 239, 206)
            debt_fg = (0, 97, 0)
            
        cells_info.append((fmt_num(qarzi_num), 'right', debt_bg, debt_fg))
        
        for (c_text, align, bg_col, fg_col), w in zip(cells_info, col_w):
            draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + row_h], fill=bg_col, outline=grid_col, width=border_w)
            bbox = font_cell.getbbox(c_text)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
            if align == 'center':
                tx = curr_x + (w - tw) // 2
            elif align == 'right':
                tx = curr_x + w - tw - int(16 * S)
            else:
                tx = curr_x + int(16 * S)
                
            ty = curr_y + (row_h - th) // 2 - bbox[1]
            draw.text((tx, ty), c_text, fill=fg_col, font=font_cell)
            curr_x += w
            
        curr_y += row_h

    # 4. Summary Row (JAMI)
    curr_x = ox
    jami_w = col_w[0] + col_w[1] + col_w[2]
    draw.rectangle([curr_x, curr_y, curr_x + jami_w, curr_y + summary_h], fill=header_bg_color, outline=grid_col, width=border_w)
    bbox = font_summary.getbbox('JAMI')
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((curr_x + (jami_w - tw) // 2, curr_y + (summary_h - th) // 2 - bbox[1]), 'JAMI', fill=(255, 255, 255), font=font_summary)
    curr_x += jami_w
    
    summary_cols = [
        (fmt_num(tot_kerak), col_w[3]),
        (fmt_num(tot_jami), col_w[4]),
        (fmt_num(tot_qarzi_musbat), col_w[5]),
    ]
    for c_text, w in summary_cols:
        draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + summary_h], fill=header_bg_color, outline=grid_col, width=border_w)
        bbox = font_summary.getbbox(c_text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = curr_x + w - tw - int(16 * S)
        ty = curr_y + (summary_h - th) // 2 - bbox[1]
        draw.text((tx, ty), c_text, fill=(255, 255, 255), font=font_summary)
        curr_x += w
        
    img.save(output_path, 'PNG', quality=100)
    return output_path

def generate_xulosa_table_image(xulosa_rows, output_path):
    """Guruh rahbarlari va umumiy jamlanma XULOSA rasm jadvalini yaratish"""
    S = 3 # 3x Ultra HD Resolution
    col_w = [int(w * S) for w in [280, 160, 180, 240]]
    headers = ['Guruh rahbari', 'Guruh', 'Talabalar soni', 'Qarzdorligi']
    
    table_w = sum(col_w)
    header_h = int(65 * S)
    row_h = int(42 * S)
    summary_h = int(50 * S)
    
    num_rows = len(xulosa_rows)
    table_h = header_h + (num_rows * row_h) + summary_h
    
    margin = int(24 * S)
    img_w = table_w + 2 * margin
    img_h = table_h + 2 * margin
    
    img = Image.new('RGB', (img_w, img_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_cell = get_font(int(21 * S), bold=True)
    font_header = get_font(int(22 * S), bold=True)
    font_summary = get_font(int(23 * S), bold=True)
    
    grid_col = (0, 0, 0)
    border_w = int(3 * S // 2)
    ox, oy = margin, margin
    
    # 1. Header Row (To'q olovrang fon: #ED7D31)
    header_bg_color = (237, 125, 49)
    curr_x = ox
    curr_y = oy
    for idx, (h_text, w) in enumerate(zip(headers, col_w)):
        draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + header_h], fill=header_bg_color, outline=grid_col, width=border_w)
        bbox = font_header.getbbox(h_text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = curr_x + (w - tw) // 2
        ty = curr_y + (header_h - th) // 2 - bbox[1]
        draw.text((tx, ty), h_text, fill=(255, 255, 255), font=font_header)
        curr_x += w

    # 2. Data Rows
    curr_y += header_h
    tot_talabalar = 0
    tot_qarzdorlik = 0.0
    
    for rdata in xulosa_rows:
        curr_x = ox
        rahbar = str(rdata.get('rahbar', ''))
        guruh = str(rdata.get('guruh', ''))
        soni = int(rdata.get('soni', 0))
        qarz = float(rdata.get('qarz', 0.0))
        
        tot_talabalar += soni
        tot_qarzdorlik += qarz
        
        qarz_bg = (198, 239, 206) if qarz <= 0 else (255, 255, 255)
        
        cells_info = [
            (rahbar, 'center', (255,255,255), (0,0,0)),
            (guruh, 'center', (255,255,255), (0,0,0)),
            (str(soni), 'center', (255,255,255), (0,0,0)),
            (fmt_num(qarz), 'right', qarz_bg, (0,0,0)),
        ]
        
        for (c_text, align, bg_col, fg_col), w in zip(cells_info, col_w):
            draw.rectangle([curr_x, curr_y, curr_x + w, curr_y + row_h], fill=bg_col, outline=grid_col, width=border_w)
            bbox = font_cell.getbbox(c_text)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
            if align == 'center':
                tx = curr_x + (w - tw) // 2
            elif align == 'right':
                tx = curr_x + w - tw - int(16 * S)
            else:
                tx = curr_x + int(16 * S)
                
            ty = curr_y + (row_h - th) // 2 - bbox[1]
            draw.text((tx, ty), c_text, fill=fg_col, font=font_cell)
            curr_x += w
            
        curr_y += row_h

    # 3. Bottom Summary Row (JAMI - Qizil fon)
    curr_x = ox
    jami_w = col_w[0] + col_w[1]
    summary_bg_color = (255, 0, 0)
    
    draw.rectangle([curr_x, curr_y, curr_x + jami_w, curr_y + summary_h], fill=summary_bg_color, outline=grid_col, width=border_w)
    bbox = font_summary.getbbox('Jami')
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((curr_x + (jami_w - tw) // 2, curr_y + (summary_h - th) // 2 - bbox[1]), 'Jami', fill=(0, 0, 0), font=font_summary)
    curr_x += jami_w
    
    w_soni = col_w[2]
    draw.rectangle([curr_x, curr_y, curr_x + w_soni, curr_y + summary_h], fill=summary_bg_color, outline=grid_col, width=border_w)
    bbox = font_summary.getbbox(str(tot_talabalar))
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((curr_x + (w_soni - tw) // 2, curr_y + (summary_h - th) // 2 - bbox[1]), str(tot_talabalar), fill=(0, 0, 0), font=font_summary)
    curr_x += w_soni
    
    w_qarz = col_w[3]
    qarz_str = fmt_num(tot_qarzdorlik)
    draw.rectangle([curr_x, curr_y, curr_x + w_qarz, curr_y + summary_h], fill=summary_bg_color, outline=grid_col, width=border_w)
    bbox = font_summary.getbbox(qarz_str)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = curr_x + w_qarz - tw - int(16 * S)
    ty = curr_y + (summary_h - th) // 2 - bbox[1]
    draw.text((tx, ty), qarz_str, fill=(0, 0, 0), font=font_summary)
    
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
        cid = msg.get('chat',{}).get('id')
        if cid:
            save_user_chat_id(cid)
            
        print(f"WEBHOOK: chat={cid} text={msg.get('text','')}", file=sys.stderr, flush=True)
        update = telebot.types.Update.de_json(raw)
        bot.process_new_updates([update])
        
        check_and_notify_updates()
        
        print("WEBHOOK: done", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"WEBHOOK ERR: {e}", file=sys.stderr, flush=True)
        _tb.print_exc(file=sys.stderr)
    return "!", 200

@app.route("/")
def webhook():
    check_and_notify_updates()
    return f"✅ Bot PythonAnywhere/Vercel bulutida 24/7 faol! (v{BOT_VERSION})", 200

@app.route("/set_webhook", methods=['GET'])
def set_webhook_route():
    host_url = request.host_url.rstrip('/')
    webhook_url = f"{host_url}/{TOKEN}"
    try:
        bot.remove_webhook()
        success = bot.set_webhook(url=webhook_url)
        if success:
            check_and_notify_updates()
            return f"<h3>✅ Webhook muvaffaqiyatli o'rnatildi!</h3><p>URL: <b>{webhook_url}</b></p><p>Versiya: <b>v{BOT_VERSION}</b></p><p>Endi Telegram botingizga /start yuborib tekshirishingiz mumkin.</p>", 200
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
            "version": BOT_VERSION,
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
    if not is_user_allowed(message):
        send_access_denied(chat_id, message.from_user.id)
        return
    save_user_chat_id(chat_id)
    user_data[chat_id] = {}
    send_safe_message(chat_id, f"🚀 <b>Salom! Aqlli kontrakt va guruhlar platformasi faol.</b>\n"
                               f"📌 <b>Tizim versiyasi:</b> <code>v{BOT_VERSION}</code>\n"
                               f"🔑 <b>Foydalanuvchi ID:</b> <code>{message.from_user.id}</code> (Ruxsat berilgan)\n\n"
                               f"Kerakli bo'limni tanlang:")

@bot.message_handler(func=lambda message: message.text == "📝 Kontraktni yangilash")
def start_kontrakt_yangilash(message):
    chat_id = message.chat.id
    if not is_user_allowed(message):
        send_access_denied(chat_id, message.from_user.id)
        return
    save_user_chat_id(chat_id)
    user_data[chat_id] = {"holat": "baza_kutish"}
    send_safe_message(chat_id, "📑 <b>1-BOSQICH: ASOSIY BAZANI YUKLASH</b>\n\n"
                               "Iltimos, kontraktlar kiritilgan asosiy <b>.xlsx</b> faylingizni yuboring:")

@bot.message_handler(func=lambda message: message.text == "📸 Guruh screenshotlarini olish")
def start_guruh_screenshot(message):
    chat_id = message.chat.id
    if not is_user_allowed(message):
        send_access_denied(chat_id, message.from_user.id)
        return
    save_user_chat_id(chat_id)
    user_data[chat_id] = {"holat": "guruh_fayl_kutish"}
    send_safe_message(chat_id, "📸 <b>GURUH SCREENSHOTLARINI OLISH</b>\n\n"
                               "Guruhlar screenshotlarini olish uchun tayyorlangan Excel (<b>.xlsx</b>) faylingizni yuboring:")

# Matnli xabarlar handler
@bot.message_handler(func=lambda message: message.content_type == 'text' and not message.text.startswith('/'))
def handle_text_messages(message):
    chat_id = message.chat.id
    if not is_user_allowed(message):
        send_access_denied(chat_id, message.from_user.id)
        return
    save_user_chat_id(chat_id)
    holat = user_data.get(chat_id, {}).get("holat")

    if holat == "sana_kutish":
        sana_matni = message.text.strip()
        sana_matni = sana_matni.replace("📅", "").strip()

        try:
            cheklov_sanasi = datetime.strptime(sana_matni, "%d.%m.%Y")
            user_data[chat_id]["sana"] = cheklov_sanasi
            
            baza_path = user_data[chat_id].get("baza_path")
            deb_path = user_data[chat_id].get("deb_path")

            if not baza_path or not os.path.exists(baza_path) or not deb_path or not os.path.exists(deb_path):
                send_safe_message(chat_id, "❌ Yuklangan fayllar topilmadi. Qayta urinib ko'ring.")
                user_data[chat_id] = {}
                return

            process_kontrakt_update(chat_id, baza_path, deb_path, cheklov_sanasi)
            user_data[chat_id] = {}

        except ValueError:
            suggested = user_data.get(chat_id, {}).get("taklif_sana_str")
            markup = get_main_keyboard(suggested)
            send_safe_message(chat_id, "❌ Noto'g'ri sana formati. Nuqtalar bilan kiriting (Masalan: <code>27.06.2026</code>):", reply_markup=markup)

# Fayl yuklanganda ishlovchi handler
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    if not is_user_allowed(message):
        send_access_denied(chat_id, message.from_user.id)
        return
    save_user_chat_id(chat_id)
    holat = user_data.get(chat_id, {}).get("holat")

    if not holat:
        send_safe_message(chat_id, "Iltimos, avval menyudan kerakli tugmani tanlang:")
        return

    # GURUH SCREENSHOTLARINI OLISH
    if holat == "guruh_fayl_kutish":
        process_group_screenshots(chat_id, message)
        return

    # KONTRAKTNI YANGILASH: 1-BOSQICH
    if holat == "baza_kutish":
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            baza_nomi = os.path.join(tempfile.gettempdir(), f"baza_{chat_id}.xlsx")
            with open(baza_nomi, 'wb') as f:
                f.write(downloaded_file)

            taklif_sana_dt = None
            try:
                wb_check = openpyxl.load_workbook(baza_nomi, data_only=True)
                sheet_check = wb_check.active
                for r in range(1, 30):
                    for c in range(1, 10):
                        val = str(sheet_check.cell(row=r, column=c).value or "")
                        if 'yangilangan sanasi' in val.lower():
                            cell_val = sheet_check.cell(row=r, column=c+1).value or sheet_check.cell(row=r, column=c+2).value
                            if cell_val:
                                if isinstance(cell_val, datetime):
                                    taklif_sana_dt = cell_val + timedelta(days=1)
                                elif isinstance(cell_val, str):
                                    try:
                                        dt = datetime.strptime(cell_val.strip(), "%d.%m.%Y")
                                        taklif_sana_dt = dt + timedelta(days=1)
                                    except ValueError:
                                        pass
                wb_check.close()
            except Exception:
                pass

            if not taklif_sana_dt and message.document.file_name:
                match = re.search(r'(\d{2}\.\d{2}\.\d{4})', message.document.file_name)
                if match:
                    try:
                        dt = datetime.strptime(match.group(1), "%d.%m.%Y")
                        taklif_sana_dt = dt + timedelta(days=1)
                    except ValueError:
                        pass

            taklif_sana_str = taklif_sana_dt.strftime("%d.%m.%Y") if taklif_sana_dt else None

            user_data[chat_id]["baza_path"] = baza_nomi
            user_data[chat_id]["taklif_sana_str"] = taklif_sana_str
            user_data[chat_id]["holat"] = "deb_kutish"

            send_safe_message(chat_id, "✅ <b>Asosiy baza qabul qilindi!</b>\n\n"
                                       "📥 <b>2-BOSQICH: BANK DEBITORKASINI YUKLASH</b>\n\n"
                                       "Endi bankdan kelgan yangi <b>Debitorka (.xlsx)</b> faylini yuboring:")
        except Exception as e:
            send_safe_message(chat_id, f"❌ Faylni yuklashda xatolik: <code>{escape_html_text(str(e))}</code>")
            user_data[chat_id] = {}
        return

    # KONTRAKTNI YANGILASH: 2-BOSQICH
    if holat == "deb_kutish":
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            deb_nomi = os.path.join(tempfile.gettempdir(), f"deb_{chat_id}.xlsx")
            with open(deb_nomi, 'wb') as f:
                f.write(downloaded_file)

            user_data[chat_id]["deb_path"] = deb_nomi
            user_data[chat_id]["holat"] = "sana_kutish"

            taklif_sana_str = user_data[chat_id].get("taklif_sana_str")
            
            msg_text = "✅ <b>Bank debitorkasi qabul qilindi!</b>\n\n" \
                       "📅 <b>3-BOSQICH: BOSHLANISH SANASI</b>\n\n"
            
            if taklif_sana_str:
                msg_text += f"💡 Bazangizdagi oxirgi sana bo'yicha tavsiya etilgan boshlanish sanasi: <code>{taklif_sana_str}</code>\n\n"
            
            msg_text += "To'lovlarni <b>qaysi sanadan boshlab</b> hisoblayin?\n"
            if taklif_sana_str:
                msg_text += f"<i>(Pastdagi <code>{taklif_sana_str}</code> tugmasini bosing yoki o'zingiz sana kiriting):</i>"
            else:
                msg_text += "Format: <code>27.06.2026</code> shaklida yozing:"

            markup = get_main_keyboard(suggested_date=taklif_sana_str)
            send_safe_message(chat_id, msg_text, reply_markup=markup)

        except Exception as e:
            send_safe_message(chat_id, f"❌ Faylni yuklashda xatolik: <code>{escape_html_text(str(e))}</code>")
            user_data[chat_id] = {}
        return

def process_kontrakt_update(chat_id, baza_path, deb_nomi, cheklov_sanasi):
    """Kontraktlarni yangilash, hisobot va XULOSA rasm tayyorlash"""
    progress = TelegramProgress(bot, chat_id, "⏳ Jarayon boshlandi...")

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
        kerak_ustun = 4
        tolov_ustun = 5
        guruh_ustun = 1
        boshlanish_row = 23

        for r in range(1, 30):
            for c in range(1, 15):
                val = str(sheet_read.cell(row=r, column=c).value or "").lower()
                if 'guruh' in val and 'rahbar' not in val and 'soni' not in val:
                    guruh_ustun = c
                if any(x in val for x in ['familiya', 'f.i.sh', 'ism', 'sharfi']):
                    ism_ustun = c
                    boshlanish_row = r + 1
                if 'bo\'lishi' in val or 'kerak' in val:
                    kerak_ustun = c
                if any(x in val for x in ['jami', 'to\'lagan summasi', 'to\'lov']):
                    tolov_ustun = c

        baza_talabalari = []
        for row in range(boshlanish_row, sheet_read.max_row + 1):
            fio = sheet_read.cell(row=row, column=ism_ustun).value
            if fio and str(fio).strip() and not str(fio).lower().startswith(('familiya', 'f.i.sh', 'итого', 'jami', 'guruh')):
                guruh_val = sheet_read.cell(row=row, column=guruh_ustun).value
                guruh_str = str(guruh_val).strip() if guruh_val else "Noma'lum"
                if guruh_str.endswith('.0'): guruh_str = guruh_str[:-2]

                eski_val = sheet_read.cell(row=row, column=tolov_ustun).value
                kerak_val = sheet_read.cell(row=row, column=kerak_ustun).value
                try: eski_sum = float(eski_val) if eski_val else 0.0
                except (ValueError, TypeError): eski_sum = 0.0

                try: kerak_sum = float(kerak_val) if kerak_val else 0.0
                except (ValueError, TypeError): kerak_sum = 0.0

                baza_talabalari.append({
                    "row": row,
                    "original_name": str(fio).strip(),
                    "clean_name": ismlarni_standartlash(fio),
                    "guruh": guruh_str,
                    "kerak_summa": kerak_sum,
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
                    s_set = fuzz.token_set_ratio(deb_fio_clean, talaba["clean_name"])
                    s_partial = fuzz.partial_ratio(talaba["clean_name"], deb_fio_clean)
                    s_sort = fuzz.token_sort_ratio(deb_fio_clean, talaba["clean_name"])
                    ball = max(s_set, s_partial, s_sort)

                    if ball > eng_yuqori_ball:
                        eng_yuqori_ball = ball
                        eng_yaxshi_moslik = talaba

                if eng_yaxshi_moslik and eng_yuqori_ball >= 70:
                    target_row = eng_yaxshi_moslik["row"]
                    
                    eski_summa = eng_yaxshi_moslik["joriy_summa"]
                    jami_yangi = eski_summa + yangi_summa
                    
                    sheet_write.cell(row=target_row, column=tolov_ustun).value = jami_yangi
                    eng_yaxshi_moslik["joriy_summa"] = jami_yangi
                    
                    jami_tushgan_pul += yangi_summa
                    yangilangan_talabalar_set.add(eng_yaxshi_moslik['original_name'])

                    safe_orig_name = escape_html_text(eng_yaxshi_moslik['original_name'])
                    safe_guruh = escape_html_text(eng_yaxshi_moslik['guruh'])
                    safe_deb_fio = escape_html_text(deb_fio_str or h_str)
                    safe_sana = to_lov_sanasi.strftime('%d.%m.%Y')
                    
                    yangilanish_tarixi.append(
                        f"<blockquote>👤 <b>{safe_orig_name}</b>\n"
                        f"├ 🏦 Debitorkada: <code>{safe_deb_fio}</code>\n"
                        f"├ 🏫 Guruh: <code>{safe_guruh}</code>\n"
                        f"├ 📅 Toʻlov sanasi: <code>{safe_sana}</code>\n"
                        f"├ ➕ Tushgan pul: <code>{yangi_summa:,.0f} so'm</code>\n"
                        f"└ 📊 Jami toʻladi: <code>{jami_yangi:,.0f} so'm</code></blockquote>"
                    )
                else:
                    if h_str and deb_fio_str and h_str != deb_fio_str and deb_fio_str != "?":
                        disp_name = f"{deb_fio_str} | {h_str}"
                    elif h_str:
                        disp_name = h_str
                    else:
                        disp_name = deb_fio_str or "Noma'lum"

                    safe_disp_name = escape_html_text(disp_name)
                    safe_sana = to_lov_sanasi.strftime('%d.%m.%Y')
                    topilmaganlar.append(f"<blockquote>❓ <code>{safe_disp_name}</code> — <code>{yangi_summa:,.0f} so'm</code> (Sana: {safe_sana})</blockquote>")

        progress.update("⚙️ Natija tayyorlanmoqda...", 85)

        oxirgi_sana_str = oxirgi_to_lov_sanasi.strftime('%d.%m.%Y') if oxirgi_to_lov_sanasi else cheklov_sanasi.strftime('%d.%m.%Y')
        for r in range(1, 30):
            for c in range(1, 10):
                val = str(sheet_write.cell(row=r, column=c).value or "")
                if 'yangilangan sanasi' in val.lower():
                    target_c = c + 1
                    if not sheet_write.cell(row=r, column=target_c).value:
                        target_c = c + 2
                    sheet_write.cell(row=r, column=target_c).value = oxirgi_sana_str

        # Guruhlar bo'yicha umumiy XULOSA ma'lumotlarini bazadan avtomatik shakllantirish
        xulosa_rows = []
        for r in range(1, 20):
            rahbar = sheet_read.cell(row=r, column=3).value
            guruh = sheet_read.cell(row=r, column=4).value
            if rahbar and guruh and str(rahbar).strip() and str(guruh).strip():
                if str(rahbar).lower().startswith(('jami', 'итого', 'guruh rahbari')): continue
                g_str = str(guruh).strip()
                if g_str.endswith('.0'): g_str = g_str[:-2]

                g_students = [t for t in baza_talabalari if t['guruh'] == g_str]
                soni = len(g_students)
                qarz_sum = sum(max(0.0, t['kerak_summa'] - t['joriy_summa']) for t in g_students)

                xulosa_rows.append({
                    'rahbar': str(rahbar).strip(),
                    'guruh': g_str,
                    'soni': soni if soni > 0 else int(sheet_read.cell(row=r, column=5).value or 0),
                    'qarz': qarz_sum
                })

        natija_nomi = os.path.join(tempfile.gettempdir(), f"{oxirgi_sana_str}_GACHA_KONTRAKTLAR.xlsx")
        wb_baza_write.save(natija_nomi)
        wb_baza_write.close()
        wb_baza_read.close()
        wb_deb.close()

        progress.update("🔍 Yakuniy tekshiruv...", 95)

        keyingi_sana_dt = (oxirgi_to_lov_sanasi or cheklov_sanasi) + timedelta(days=1)
        keyingi_sana_str = keyingi_sana_dt.strftime('%d.%m.%Y')

        hisobot_matni = f"📊 <b>KONTRAKT YANGILANISH HISOBOTI</b>\n"
        hisobot_matni += f"📅 Filtr sanasi: {cheklov_sanasi.strftime('%d.%m.%Y')} dan {oxirgi_sana_str} gacha\n"
        hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n"
        hisobot_matni += f"💰 <b>Jami tushgan pul:</b> <code>{jami_tushgan_pul:,.0f} so'm</code>\n"
        hisobot_matni += f"👥 <b>Muvaffaqiyatli yangilandi:</b> {len(yangilangan_talabalar_set)} kishi\n"
        hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if yangilanish_tarixi:
            hisobot_matni += f"✅ <b>Yangilangan talabalar ({len(yangilanish_tarixi)} ta):</b>\n\n"
            for t in yangilanish_tarixi:
                hisobot_matni += t + "\n\n"
        else:
            hisobot_matni += "❌ Yangi to'lovlar topilmadi.\n\n"

        if topilmaganlar:
            hisobot_matni += f"❓ <b>Umuman topilmagan ismlar ({len(topilmaganlar)} ta):</b>\n"
            for top in topilmaganlar:
                hisobot_matni += top + "\n"
            hisobot_matni += "\n"

        hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n"
        hisobot_matni += f"💡 <b>Keyingi safar adashmasligingiz uchun eslatma:</b>\n"
        hisobot_matni += f"Navbatdagi debitorkani yuklaganingizda botga boshlanish sanasi sifatida <code>{keyingi_sana_str}</code> sanasini kiriting."

        with open(natija_nomi, 'rb') as f_send:
            bot.send_document(chat_id, f_send, caption=f"📄 Formulalari buzilmagan tayyor Excel faylingiz: <code>{os.path.basename(natija_nomi)}</code>", parse_mode="HTML", reply_markup=get_main_keyboard())
        
        send_safe_message(chat_id, hisobot_matni)

        # ENG OXIRIDA GURUHLAR BO'YICHA XULOSA RASM JADVALINI YUBORISH
        if xulosa_rows:
            xulosa_img = os.path.join(tempfile.gettempdir(), f"xulosa_{chat_id}.png")
            generate_xulosa_table_image(xulosa_rows, xulosa_img)
            with open(xulosa_img, 'rb') as xf:
                bot.send_photo(chat_id, photo=xf, caption=f"📊 <b>Guruh rahbarlari bo'yicha umumiy XULOSA hisoboti (v{BOT_VERSION})</b>", parse_mode="HTML")
            if os.path.exists(xulosa_img): os.remove(xulosa_img)

        progress.success("✅ Tayyor!")

        if os.path.exists(baza_path): os.remove(baza_path)
        if os.path.exists(deb_nomi): os.remove(deb_nomi)
        if os.path.exists(natija_nomi): os.remove(natija_nomi)

    except Exception as e:
        progress.error(f"❌ Jarayonni bajarishda xatolik yuz berdi:\n<code>{escape_html_text(str(e))}</code>")
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
                bot.send_photo(chat_id, photo=photo_f, caption=f"📊 <b>Guruh: {escape_html_text(g_name)}</b>", parse_mode="HTML")
            
            if os.path.exists(img_path): os.remove(img_path)

        progress.update("🔍 Yakuniy tekshiruv...", 95)
        send_safe_message(chat_id, f"✅ <b>Barcha {len(guruh_nomlari)} ta guruh screenshotlari muvaffaqiyatli yuborildi!</b>")
        progress.success("✅ Tayyor!")
        user_data[chat_id] = {}

    except Exception as e:
        progress.error(f"❌ Xatolik yuz berdi:\n<code>{escape_html_text(str(e))}</code>")
        if os.path.exists(temp_excel): os.remove(temp_excel)
        user_data[chat_id] = {}

if __name__ == "__main__":
    bot.remove_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))