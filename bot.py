import telebot
from telebot import apihelper
import openpyxl
from datetime import datetime, timedelta
import os
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify
import tempfile

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN") or "8937819411:AAHrCwLyr_Ob3bM0ypwNFYP-SKb1weL97fs"

# PythonAnywhere bepul tarifida Telegram API proksi orqali ishlaydi
if os.path.exists('/var/www') or 'PYTHONANYWHERE_DOMAIN' in os.environ or 'PYTHONANYWHERE_SITE' in os.environ or 'pythonanywhere' in os.environ.get('HOME', ''):
    os.environ['http_proxy'] = 'http://proxy.server:3128'
    os.environ['https_proxy'] = 'http://proxy.server:3128'
    apihelper.proxy = {'http': 'http://proxy.server:3128', 'https': 'http://proxy.server:3128'}

bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)
user_data = {}

def get_main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("📝 Kontraktni yangilash")
    btn2 = telebot.types.KeyboardButton("📸 Guruh screenshotlarini olish")
    markup.add(btn1, btn2)
    return markup

def escape_md(text):
    """Telegram Markdown uchun maxsus belgilarni zararsizlantirish"""
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

def draw_filter_arrow(draw, x, y, size=14):
    """Excel filtri tugmasi (strelka) rasmga chizish"""
    draw.rectangle([x, y, x + size, y + size], fill=(242, 242, 242), outline=(166, 166, 166))
    cx = x + size // 2
    cy = y + size // 2
    draw.polygon([(cx - 3, cy - 2), (cx + 3, cy - 2), (cx, cy + 2)], fill=(51, 51, 51))

def generate_group_table_image(group_name, date_str, rows_data, output_path, header_bg_color=(0, 112, 192), font_key='arial_bold'):
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
    
    margin = int(20 * S) # Outer hoshiya
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
    
    grid_col = (0, 0, 0) # PITCH BLACK GRIDLINES
    border_w = 3 # Crisp black borders
    
    ox = margin
    oy = margin
    
    # 1. Title Row (CENTERED across full table width)
    draw.rectangle([ox, oy, ox + table_w, oy + title_h], fill=(255, 255, 255), outline=grid_col, width=border_w)
    title_str = f'Yangilangan sanasi:   {date_str}'
    
    bbox = font_title.getbbox(title_str) if hasattr(font_title, 'getbbox') else (0,0,220*S,16*S)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    tx = ox + (table_w - tw) // 2
    ty = oy + (title_h - th) // 2 - int(2 * S)
    draw.text((tx, ty), title_str, fill=(0, 0, 0), font=font_title)
    
    # 2. Header Row (NO FILTER ARROWS, fully centered)
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

    # 3. Data Rows (ALL BOLD TEXT)
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
    return "✅ Bot PythonAnywhere bulutida 24/7 faol!", 200

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

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    import sys
    chat_id = message.chat.id
    print(f"START: chat_id={chat_id}", file=sys.stderr, flush=True)
    user_data[chat_id] = {}
    try:
        bot.send_message(chat_id, "Salom! Aqlli kontrakt va guruhlar platformasi faol. 🚀\n\n"
                                  "Kerakli bo'limni tanlang:", reply_markup=get_main_keyboard())
        print(f"START: xabar yuborildi {chat_id}", file=sys.stderr, flush=True)
    except Exception as e:
        import traceback
        print(f"START ERR: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)

@bot.message_handler(func=lambda message: message.text == "📝 Kontraktni yangilash")
def start_kontrakt_yangilash(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"holat": "sana_kutish"}
    bot.reply_to(message, "To'lovlarni **qaysi sanadan boshlab** hisoblayin?\n"
                          "Format: `27.06.2026` shaklida yozing:", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: message.text == "📸 Guruh screenshotlarini olish")
def start_guruh_screenshot(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"holat": "guruh_fayl_kutish"}
    bot.reply_to(message, "📸 **Guruhlar screenshotlarini olish uchun tayyorlangan Excel (.xlsx) faylingizni yuboring:**", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id].get("holat") == "sana_kutish")
def qabul_qilish_sanasi(message):
    chat_id = message.chat.id
    sana_matni = message.text.strip()
    try:
        cheklov_sanasi = datetime.strptime(sana_matni, "%d.%m.%Y")
        user_data[chat_id]["sana"] = cheklov_sanasi
        user_data[chat_id]["holat"] = "fayl_kutish"
        bot.send_message(chat_id, f"✅ Sana tasdiqlandi: **{sana_matni}**.\n\n"
                                  f"1. **Asosiy bazangizni** (.xlsx) yuboring.", reply_markup=get_main_keyboard())
    except ValueError:
        bot.reply_to(message, "❌ Noto'g'ri format. Nuqtalar bilan kiriting (Masalan: 27.06.2026):", reply_markup=get_main_keyboard())

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    holat = user_data.get(chat_id, {}).get("holat")

    if not holat:
        bot.reply_to(message, "Iltimos, avval menyudan tugmalardan birini tanlang:", reply_markup=get_main_keyboard())
        return

    # VAZIFA 2: GURUH SCREENSHOTLARINI OLISH
    if holat == "guruh_fayl_kutish":
        try:
            bot.reply_to(message, "🔄 Guruhlar screenshotlari tayyorlanmoqda, kuting...")
            
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            temp_excel = os.path.join(tempfile.gettempdir(), f"temp_guruh_{chat_id}.xlsx")
            with open(temp_excel, 'wb') as f:
                f.write(downloaded_file)

            wb = openpyxl.load_workbook(temp_excel, data_only=True)
            sheet = wb.active

            header_row = 22
            date_str = datetime.now().strftime("%d.%m.%Y")

            # Qator va sarlavhalarni aniqlash
            for r in range(1, 30):
                val_a = str(sheet.cell(row=r, column=1).value or "").lower()
                val_c = str(sheet.cell(row=r, column=3).value or "").lower()
                if "guruh" in val_a or "familiy" in val_c:
                    header_row = r
                    break
                # Yangilangan sanasini olish
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
                bot.send_message(chat_id, "❌ Excel faylidan guruhlar ma'lumotlari topilmadi.", reply_markup=get_main_keyboard())
                user_data[chat_id] = {}
                return

            # Har bir guruh uchun screenshot yaratish va yuborish
            guruh_nomlari = sorted(guruhlar.keys())
            for g_name in guruh_nomlari:
                rows_data = guruhlar[g_name]
                img_path = os.path.join(tempfile.gettempdir(), f"screenshot_{chat_id}_{g_name}.png")
                
                generate_group_table_image(g_name, date_str, rows_data, img_path)
                
                with open(img_path, 'rb') as photo_f:
                    bot.send_photo(chat_id, photo=photo_f, caption=f"📊 **Guruh: {g_name}**", parse_mode="Markdown")
                
                if os.path.exists(img_path): os.remove(img_path)

            bot.send_message(chat_id, f"✅ **Barcha {len(guruh_nomlari)} ta guruh screenshotlari muvaffaqiyatli yuborildi!**", reply_markup=get_main_keyboard())
            user_data[chat_id] = {}

        except Exception as e:
            bot.send_message(chat_id, f"❌ Xatolik yuz berdi: {str(e)}", reply_markup=get_main_keyboard())
            user_data[chat_id] = {}
        return

    # VAZIFA 1: KONTRAKTNI YANGILASH (Eski oqim)
    if "sana" not in user_data[chat_id]:
        bot.reply_to(message, "❌ Iltimos, avval sana kiriting!", reply_markup=get_main_keyboard())
        return

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        baza_nomi = os.path.join(tempfile.gettempdir(), f"baza_{chat_id}.xlsx")
        deb_nomi = os.path.join(tempfile.gettempdir(), f"deb_{chat_id}.xlsx")
        natija_nomi = os.path.join(tempfile.gettempdir(), f"Tayyor_Yangilangan_{chat_id}.xlsx")

        if "baza_yuklandi" not in user_data[chat_id]:
            with open(baza_nomi, 'wb') as f:
                f.write(downloaded_file)
            user_data[chat_id]["baza_yuklandi"] = True
            user_data[chat_id]["baza_path"] = baza_nomi
            bot.reply_to(message, "✅ Asosiy baza yuklandi.\n\n"
                                  "2. Endi bankdan kelgan **Debitorka** faylini yuboring.", reply_markup=get_main_keyboard())
            return
        
        elif "deb_yuklandi" not in user_data[chat_id]:
            with open(deb_nomi, 'wb') as f:
                f.write(downloaded_file)
            user_data[chat_id]["deb_yuklandi"] = True
            
            baza_path = user_data[chat_id]["baza_path"]
            cheklov_sanasi = user_data[chat_id]["sana"]
            
            bot.reply_to(message, "🔄 Hisob-kitob va matnli hisobot tayyorlanmoqda. Kuting...", reply_markup=get_main_keyboard())

            wb_baza_write = openpyxl.load_workbook(baza_path, data_only=False)
            wb_baza_read = openpyxl.load_workbook(baza_path, data_only=True)
            wb_deb = openpyxl.load_workbook(deb_nomi, data_only=True)

            varoq_nomi = 'KONTRAKTLAR' if 'KONTRAKTLAR' in wb_baza_write.sheetnames else wb_baza_write.sheetnames[0]
            sheet_write = wb_baza_write[varoq_nomi]
            sheet_read = wb_baza_read[varoq_nomi]
            sheet_deb = wb_deb['bank'] if 'bank' in wb_deb.sheetnames else wb_deb.active

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
            
            for row in range(2, sheet_deb.max_row + 1):
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
                            f"👤 **{safe_orig_name}**\n"
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

            wb_baza_write.save(natija_nomi)
            wb_baza_write.close()
            wb_baza_read.close()
            wb_deb.close()

            oxirgi_sana_str = oxirgi_to_lov_sanasi.strftime('%d.%m.%Y') if oxirgi_to_lov_sanasi else cheklov_sanasi.strftime('%d.%m.%Y')
            keyingi_sana_dt = (oxirgi_to_lov_sanasi or cheklov_sanasi) + timedelta(days=1)
            keyingi_sana_str = keyingi_sana_dt.strftime('%d.%m.%Y')

            hisobot_matni = f"📊 **KONTRAKT YANGILANISH HISOBOTI**\n"
            hisobot_matni += f"📅 Filtr sanasi: {cheklov_sanasi.strftime('%d.%m.%Y')} dan {oxirgi_sana_str} gacha\n"
            hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n"
            hisobot_matni += f"💰 **Jami tushgan pul:** `{jami_tushgan_pul:,.0f} so'm`\n"
            hisobot_matni += f"👥 **Muvaffaqiyatli yangilandi:** {len(yangilangan_talabalar_set)} kishi\n"
            hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if yangilanish_tarixi:
                hisobot_matni += f"✅ **Yangilangan talabalar ({len(yangilanish_tarixi)} ta):**\n\n"
                for t in yangilanish_tarixi:
                    hisobot_matni += t + "\n\n"
            else:
                hisobot_matni += "❌ Yangi to'lovlar topilmadi.\n\n"

            if topilmaganlar:
                hisobot_matni += f"❓ **Umuman topilmagan ismlar ({len(topilmaganlar)} ta):**\n"
                for top in topilmaganlar:
                    hisobot_matni += top + "\n"
                hisobot_matni += "\n"

            hisobot_matni += f"━━━━━━━━━━━━━━━━━━━━\n"
            hisobot_matni += f"💡 **Keyingi safar adashmasligingiz uchun eslatma:**\n"
            hisobot_matni += f"Navbatdagi debitorkani yuklaganingizda botga boshlanish sanasi sifatida `{keyingi_sana_str}` sanasini kiriting."

            with open(natija_nomi, 'rb') as f_send:
                bot.send_document(chat_id, f_send, caption="📄 Formulalari buzilmagan tayyor Excel faylingiz.", reply_markup=get_main_keyboard())
            
            send_safe_message(chat_id, hisobot_matni)

            if os.path.exists(baza_path): os.remove(baza_path)
            if os.path.exists(deb_nomi): os.remove(deb_nomi)
            if os.path.exists(natija_nomi): os.remove(natija_nomi)
            user_data[chat_id] = {}

    except Exception as e:
        bot.send_message(chat_id, f"❌ Xatolik yuz berdi: {str(e)}", reply_markup=get_main_keyboard())
        user_data[chat_id] = {}

# Webhookni Render yoki PythonAnywhere ishga tushganda bog'laydi
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://Alcatrazbek.pythonanywhere.com/" + TOKEN) 
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
