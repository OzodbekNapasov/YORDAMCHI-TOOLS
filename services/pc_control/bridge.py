# ============================================================
#  services/pc_control/bridge.py
#  ATLAS Cloud-to-Local Realtime PC Bridge (Vercel <-> Windows PC)
# ============================================================

import os
import sys
import time
import json
import uuid
import base64
import logging
import tempfile
import threading
import requests
from datetime import datetime
from pathlib import Path


from .system_tools import (
    get_system_status,
    take_screenshot,
    take_webcam_photo,
    execute_cmd_sync,
    get_running_apps,
    kill_process,
    power_control,
    empty_recycle_bin,
    clean_temp_files,
    set_brightness,
    set_volume,
    set_mute,
    media_control,
    show_desktop,
    search_user_files,
    pair_sunshine_pin,
    take_all_monitors_screenshots,
    wake_and_unlock_pc,
    is_system_compatible,
    print_file,
    read_file_content,
    download_or_install_software,
    write_file_content
)

logger = logging.getLogger(__name__)

_DAEMON_STARTED = False
_DAEMON_LOCK = threading.Lock()


def _get_supa_headers():
    """Supabase URL va API kalitlarini olish (atlas_db orqali yoki .env orqali)"""
    try:
        from services.atlas_db import _get_supabase_credentials
        supa_url, supa_key = _get_supabase_credentials()
    except Exception:
        # Fallback: to'g'ridan-to'g'ri o'qish
        supa_url = os.environ.get("SUPABASE_URL", "https://rsrrrkkpvfjyfnzikiiy.supabase.co")
        supa_key = (
            os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or
            os.environ.get("SUPABASE_KEY") or
            os.environ.get("SB_KEY") or
            ""
        )

    # .env faylidan o'qish (agar env variable bo'lmasa)
    if not supa_key or supa_key == "":
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_paths = [
            os.path.join(base_dir, ".env"),
            ".env"
        ]
        for ep in env_paths:
            if os.path.exists(ep):
                try:
                    with open(ep, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            if "=" not in line:
                                continue
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip()
                            if k == "SUPABASE_SERVICE_ROLE_KEY" and v:
                                supa_key = v
                            elif k == "SUPABASE_KEY" and v and not supa_key:
                                supa_key = v
                            elif k == "SUPABASE_URL" and v and not os.environ.get("SUPABASE_URL"):
                                supa_url = v
                except Exception:
                    pass
                if supa_key:
                    break

    headers = {
        "apikey": supa_key,
        "Authorization": f"Bearer {supa_key}",
        "Content-Type": "application/json"
    }
    return supa_url, supa_key, headers


def collect_local_pc_metrics():
    """Mahalliy Windows kompyuterining real vaqtdagi parametrlarini yig'ish"""
    try:
        import psutil
        from datetime import datetime, timedelta

        cpu_usage = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count(logical=True)
        ram = psutil.virtual_memory()

        disks = []
        for d in ["C:\\", "D:\\"]:
            if os.path.exists(d):
                try:
                    du = psutil.disk_usage(d)
                    disks.append({
                        "drive": d,
                        "percent": du.percent,
                        "free_gb": round(du.free / (1024 ** 3), 1),
                        "total_gb": round(du.total / (1024 ** 3), 1)
                    })
                except Exception:
                    pass

        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = str(timedelta(seconds=int((datetime.now() - boot_time).total_seconds())))

        battery = psutil.sensors_battery()
        battery_data = {
            "percent": battery.percent if battery else 100,
            "plugged": battery.power_plugged if battery else True,
            "has_battery": bool(battery)
        }

        # TOP 15 Apps
        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                pinfo = proc.info
                if pinfo['name'] and pinfo['memory_info']:
                    mem_mb = round(pinfo['memory_info'].rss / (1024 * 1024), 1)
                    if mem_mb > 20:
                        apps.append({'pid': pinfo['pid'], 'name': pinfo['name'], 'memory_mb': mem_mb})
            except Exception:
                pass
        apps = sorted(apps, key=lambda x: x['memory_mb'], reverse=True)[:15]

        return {
            "online": True,
            "last_seen": time.time(),
            "cpu_percent": cpu_usage,
            "cpu_cores": cpu_count,
            "ram_percent": ram.percent,
            "ram_used_gb": round(ram.used / (1024 ** 3), 2),
            "ram_total_gb": round(ram.total / (1024 ** 3), 2),
            "disks": disks,
            "uptime": uptime,
            "battery": battery_data,
            "hostname": os.getenv("COMPUTERNAME", "Windows-PC"),
            "apps": apps,
            "raw_text": get_system_status()
        }
    except Exception as e:
        return {
            "online": True,
            "last_seen": time.time(),
            "error": str(e),
            "hostname": os.getenv("COMPUTERNAME", "Windows-PC")
        }


def get_bridge_pc_status():
    """
    Platformadan chaqirilganda holatni qaytarish:
    - Agar mahalliy Windows bo'lsa: darhol o'lchab qaytaradi.
    - Agar Vercel bulutida bo'lsa: Supabase'dagi jonli heartbeat'ni o'qib beradi.
    """
    # 1. Agar lokal Windows bo'lsa
    if is_system_compatible():
        metrics = collect_local_pc_metrics()
        # Bir vaqtda Supabase'ni ham yangilab qo'yamiz
        threading.Thread(target=_push_heartbeat_sync, args=(metrics,), daemon=True).start()
        return metrics

    # 2. Vercel Cloud bo'lsa — Supabase'dan o'qish
    supa_url, supa_key, headers = _get_supa_headers()
    if not supa_key:
        return {"online": False, "error": "Supabase kaliti topilmadi"}

    try:
        r = requests.get(
            f"{supa_url}/rest/v1/atlas_settings?key=eq.pc_live_state&select=*",
            headers=headers,
            timeout=3.5
        )
        if r.status_code == 200 and r.json():
            row = r.json()[0]
            val = json.loads(row.get("value", "{}"))
            last_seen = val.get("last_seen", 0)
            is_online = (time.time() - last_seen) < 15  # 15 soniya ichida yangilangan bo'lsa Online
            val["online"] = is_online
            if not is_online:
                val["offline_reason"] = "Kompyuteringizdagi Telegram bot yoki lokal agent yoniq emas."
            return val
    except Exception as e:
        logger.error(f"Error fetching pc_live_state: {e}")

    return {
        "online": False,
        "offline_reason": "Kompyuter bilan aloqa yo'q. Iltimos kompyuteringizda botni ishga tushiring (python bot.py)",
        "cpu_percent": 0,
        "ram_percent": 0,
        "disks": [],
        "uptime": "--:--:--",
        "hostname": "Windows-PC (Kutilmoqda)"
    }


def _push_heartbeat_sync(metrics):
    supa_url, supa_key, headers = _get_supa_headers()
    if not supa_key:
        return
    try:
        payload = {
            "key": "pc_live_state",
            "value": json.dumps(metrics),
            "category": "pc_control",
            "description": "PC Live State Realtime Heartbeat"
        }
        h = dict(headers)
        h["Prefer"] = "resolution=merge-duplicates"
        requests.post(f"{supa_url}/rest/v1/atlas_settings", headers=h, json=payload, timeout=3.5)
    except Exception:
        pass


def dispatch_bridge_command(action: str, payload: dict = None, timeout: float = 12.0) -> dict:
    """
    Platformadan kelgan buyruqni bajarish:
    - Agar lokal Windows bo'lsa: darhol shu yerda bajaradi.
    - Agar Vercel bulutida bo'lsa: Supabase orqali lokal kompyuter agentiga yuborib, natijani kutadi.
    """
    payload = payload or {}

    # 1. Mahalliy Windows bo'lsa — to'g'ridan-to'g'ri bajarish
    if is_system_compatible():
        return _execute_command_locally(action, payload)

    # 2. Vercel Cloud bo'lsa — Supabase Bridge orqali yuborish
    supa_url, supa_key, headers = _get_supa_headers()
    if not supa_key:
        return {"success": False, "error": "Supabase kaliti mavjud emas."}

    req_id = str(uuid.uuid4())
    cmd_record = {
        "actor": "web_admin",
        "module": "pc_bridge",
        "action": action,
        "status": "pending",
        "details_json": {
            "req_id": req_id,
            "payload": payload,
            "created_at": time.time()
        }
    }

    try:
        h_post = dict(headers)
        h_post["Prefer"] = "return=representation"
        r = requests.post(f"{supa_url}/rest/v1/atlas_audit_logs", headers=h_post, json=cmd_record, timeout=4)
        if r.status_code not in [200, 201]:
            return {"success": False, "error": f"Supabase bridge buyrug'ini yozishda xatolik: {r.text}"}

        created_item = r.json()[0]
        cmd_id = created_item["id"]

        # Kutish sikli (Polling loop)
        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(0.3)
            r_check = requests.get(
                f"{supa_url}/rest/v1/atlas_audit_logs?id=eq.{cmd_id}&select=status,details_json",
                headers=headers,
                timeout=3
            )
            if r_check.status_code == 200 and r_check.json():
                item = r_check.json()[0]
                status = item.get("status")
                if status == "completed":
                    details = item.get("details_json") or {}
                    result = details.get("result") or {}
                    return result
                elif status == "error":
                    details = item.get("details_json") or {}
                    return {"success": False, "error": details.get("error", "Bajarishda xatolik yuz berdi.")}

        return {
            "success": False,
            "error": "Kompyuterdan javob kelmadi (Timeout). Iltimos, kompyuteringizda bot yoniqligini tekshiring (python bot.py)."
        }
    except Exception as e:
        return {"success": False, "error": f"Bridge aloqa xatosi: {str(e)}"}


def _execute_command_locally(action: str, payload: dict) -> dict:
    """Lokal Windows kompyuterida buyruqni bevosita bajarish"""
    action = (action or "").strip().lower()
    logger.info(f"[_execute_command_locally] action='{action}'")
    try:
        if action == "screenshot":

            mon_param = payload.get("monitor")
            all_monitors = take_all_monitors_screenshots()
            primary_image = all_monitors[0]["image"] if all_monitors else ""

            if mon_param and str(mon_param).isdigit():
                idx = int(mon_param)
                if 1 <= idx <= len(all_monitors):
                    primary_image = all_monitors[idx - 1]["image"]
            elif mon_param == "all":
                temp_path = os.path.join(tempfile.gettempdir(), f"bridge_shot_all_{int(time.time())}.png")
                take_screenshot(temp_path, monitor_index="all")
                if os.path.exists(temp_path):
                    with open(temp_path, "rb") as f:
                        b64_str = base64.b64encode(f.read()).decode("utf-8")
                    try: os.remove(temp_path)
                    except Exception: pass
                    primary_image = f"data:image/png;base64,{b64_str}"

            return {
                "success": True,
                "image": primary_image,
                "monitors": all_monitors,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

        elif action == "webcam":
            temp_path = os.path.join(tempfile.gettempdir(), f"bridge_cam_{int(time.time())}.jpg")
            take_webcam_photo(temp_path)
            with open(temp_path, "rb") as f:
                b64_str = base64.b64encode(f.read()).decode("utf-8")
            try: os.remove(temp_path)
            except Exception: pass
            return {
                "success": True,
                "image": f"data:image/jpeg;base64,{b64_str}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

        elif action == "sunshine":
            pin = str(payload.get("pin", "")).strip()
            res = pair_sunshine_pin(pin)
            return {"success": True, "message": res}

        elif action == "unlock":
            pwd = payload.get("password")
            res = wake_and_unlock_pc(pwd)
            return {"success": True, "message": res}

        elif action == "cmd":
            cmd_str = str(payload.get("command", "")).strip()
            output = execute_cmd_sync(cmd_str)
            return {"success": True, "output": output}

        elif action == "power":
            act = str(payload.get("action", "")).strip().lower()
            res = power_control(act)
            return {"success": True, "message": res}

        elif action == "cleanup":
            ctype = str(payload.get("type", "temp")).strip().lower()
            if ctype == "recycle":
                msg = empty_recycle_bin()
            else:
                msg = clean_temp_files()
            return {"success": True, "message": msg}

        elif action == "media":
            act = str(payload.get("action", "")).strip().lower()
            val = payload.get("value")
            if act == "volume":
                msg = set_volume(int(val or 50))
            elif act == "mute":
                msg = set_mute(bool(val))
            elif act == "brightness":
                msg = set_brightness(int(val or 50))
            elif act == "media_key":
                msg = media_control(str(val or "playpause"))
            elif act == "desktop":
                msg = show_desktop()
            else:
                msg = "Noma'lum media buyruq."
            return {"success": True, "message": msg}

        elif action == "print_file":
            fp = str(payload.get("file_path", "")).strip()
            res = print_file(fp)
            return {"success": True, "message": res}

        elif action == "read_file":
            fp = str(payload.get("file_path", "")).strip()
            res = read_file_content(fp)
            return {"success": True, "content": res}

        elif action == "download_software":
            tgt = str(payload.get("target", "")).strip()
            res = download_or_install_software(tgt)
            return {"success": True, "message": res}

        elif action == "write_file":
            fp = str(payload.get("file_path", "eslatma.txt")).strip()
            cnt = str(payload.get("content", ""))
            res = write_file_content(fp, cnt)
            return {"success": True, "message": res}

        elif action == "ai":
            from .ai_agent import process_ai_agent_request
            prompt = str(payload.get("prompt", "")).strip()
            res = process_ai_agent_request(8135594558, prompt)
            shot_b64 = None
            if res.get("screenshot_file") and os.path.exists(res["screenshot_file"]):
                try:
                    with open(res["screenshot_file"], "rb") as f:
                        shot_b64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
                    os.remove(res["screenshot_file"])
                except Exception:
                    pass
            return {
                "success": True,
                "action": res.get("action"),
                "message": res.get("message"),
                "exec_result": res.get("exec_result"),
                "screenshot": shot_b64
            }

        elif action == "mtf_convert":
            from services.mtf_converter import process_mtf_to_pdf
            from services.supabase_storage import upload_document_to_supabase

            raw_b64 = payload.get("file_base64", "")
            input_url = payload.get("input_url", "")
            file_path = payload.get("file_path", "")
            filename = payload.get("filename", "test.mtf")
            layout = payload.get("layout", "2col")
            with_answers = bool(payload.get("with_answers", True))
            fan_name = payload.get("fan_name") or None

            file_bytes = None
            if file_path:
                file_path = os.path.normpath(file_path)
                if not os.path.isabs(file_path):
                    file_path = os.path.join(r"D:\MyTestX\tests", file_path)
                if not os.path.exists(file_path):
                    for root, _, files in os.walk(r"D:\MyTestX\tests"):
                        if filename in files:
                            file_path = os.path.join(root, filename)
                            break
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "rb") as f:
                            file_bytes = f.read()
                        filename = os.path.basename(file_path)
                    except Exception as e:
                        logger.warning(f"Failed to read local file_path {file_path}: {e}")

            if not file_bytes and not file_path:
                for root, _, files in os.walk(r"D:\MyTestX\tests"):
                    if filename in files:
                        file_path = os.path.join(root, filename)
                        with open(file_path, "rb") as f:
                            file_bytes = f.read()
                        break


            if not file_bytes and input_url:
                try:
                    r_in = requests.get(input_url, timeout=30)
                    if r_in.status_code == 200:
                        file_bytes = r_in.content
                except Exception as e:
                    logger.warning(f"Failed to download input_url {input_url}: {e}")

            if not file_bytes and raw_b64:
                if "," in raw_b64:
                    raw_b64 = raw_b64.split(",", 1)[1]
                file_bytes = base64.b64decode(raw_b64)

            if not file_bytes:
                return {"success": False, "error": "Fayl ma'lumotlari yuklanmadi yoki topilmadi"}


            res = process_mtf_to_pdf(
                mtf_bytes=file_bytes,
                filename=filename,
                layout=layout,
                with_answers=with_answers,
                fan_name=fan_name
            )
            if not res or not res.get("success"):
                return {"success": False, "error": res.get("error", "Konvertatsiya amalga oshmadi.") if res else "Noma'lum xatolik"}

            clean_stem = Path(filename).stem
            uid = str(uuid.uuid4())[:8]

            pdf_url = ""
            if res.get("pdf_bytes"):
                temp_pdf = os.path.join(tempfile.gettempdir(), f"{clean_stem}_{uid}.pdf")
                with open(temp_pdf, "wb") as f:
                    f.write(res["pdf_bytes"])
                pdf_url = upload_document_to_supabase(temp_pdf, f"mtf_outputs/{clean_stem}_{uid}.pdf")
                try: os.remove(temp_pdf)
                except Exception: pass

            docx_url = ""
            if res.get("docx_bytes"):
                temp_docx = os.path.join(tempfile.gettempdir(), f"{clean_stem}_{uid}.docx")
                with open(temp_docx, "wb") as f:
                    f.write(res["docx_bytes"])
                docx_url = upload_document_to_supabase(temp_docx, f"mtf_outputs/{clean_stem}_{uid}.docx")
                try: os.remove(temp_docx)
                except Exception: pass

            pdf_b64 = base64.b64encode(res["pdf_bytes"]).decode("utf-8") if res.get("pdf_bytes") else None
            docx_b64 = base64.b64encode(res["docx_bytes"]).decode("utf-8") if res.get("docx_bytes") else None

            return {
                "success": True,
                "filename": res.get("filename"),
                "title": res.get("title"),
                "questions_count": res.get("questions_count", 0),
                "pdf_url": pdf_url,
                "docx_url": docx_url,
                "questions_summary": res.get("questions_summary", [])
            }



        elif action == "list_local_tests":
            from services.pc_control.system_tools import scan_mytestx_tests_dir
            return scan_mytestx_tests_dir()

        elif action == "apps":
            metrics = collect_local_pc_metrics()
            return {"success": True, "apps": metrics.get("apps", [])}

        else:
            return {"success": False, "error": f"Noma'lum buyruq turi: {action}"}

    except Exception as e:
        logger.error(f"Error executing command locally: {e}")
        return {"success": False, "error": str(e)}


def _pc_bridge_worker_loop():
    """Lokal Windows kompyuterida doimiy fonda ishlaydigan xizmatchi"""
    logger.info("ATLAS PC Bridge Worker started successfully on Windows host.")
    supa_url, supa_key, headers = _get_supa_headers()
    if not supa_key:
        logger.error("PC Bridge Worker cannot start: Supabase keys missing.")
        return

    heartbeat_counter = 0
    catalog_counter = 0

    while True:
        try:
            # 1. Har 3 soniyada Heartbeat yuborish
            heartbeat_counter += 1
            if heartbeat_counter >= 3:
                heartbeat_counter = 0
                metrics = collect_local_pc_metrics()
                _push_heartbeat_sync(metrics)

            # 2. Har 15 soniyada D:\MyTestX\tests katalogini Supabase'ga sinxronlash
            catalog_counter += 1
            if catalog_counter >= 15:
                catalog_counter = 0
                try:
                    from services.pc_control.system_tools import scan_mytestx_tests_dir
                    cat_data = scan_mytestx_tests_dir()
                    payload = {
                        "key": "mytestx_catalog",
                        "value": json.dumps(cat_data),
                        "category": "mytestx",
                        "description": "Local MyTestX Tests Catalog"
                    }
                    h = dict(headers)
                    h["Prefer"] = "resolution=merge-duplicates"
                    requests.post(f"{supa_url}/rest/v1/atlas_settings", headers=h, json=payload, timeout=3.5)
                except Exception:
                    pass

            # 3. Vercel'dan kelgan 'pending' buyruqlarni tekshirish
            r = requests.get(
                f"{supa_url}/rest/v1/atlas_audit_logs?module=eq.pc_bridge&status=eq.pending&order=id.asc&limit=3",
                headers=headers,
                timeout=3.5
            )


            if r.status_code == 200:
                pending_cmds = r.json()
                for cmd in pending_cmds:
                    cmd_id = cmd["id"]
                    action = cmd.get("action")
                    details = cmd.get("details_json") or {}
                    payload = details.get("payload") or {}

                    # Mark executing
                    patch_headers = dict(headers)
                    requests.patch(
                        f"{supa_url}/rest/v1/atlas_audit_logs?id=eq.{cmd_id}",
                        headers=patch_headers,
                        json={"status": "executing"},
                        timeout=3
                    )

                    # Bajarish
                    exec_res = _execute_command_locally(action, payload)

                    # Mark completed
                    details["result"] = exec_res
                    status = "completed" if exec_res.get("success") else "error"
                    if not exec_res.get("success"):
                        details["error"] = exec_res.get("error", "Bajarishda xatolik")

                    requests.patch(
                        f"{supa_url}/rest/v1/atlas_audit_logs?id=eq.{cmd_id}",
                        headers=patch_headers,
                        json={"status": status, "details_json": details},
                        timeout=20
                    )

        except Exception as e:
            logger.debug(f"PC Bridge Worker cycle warning: {e}")

        time.sleep(1.0)


def start_pc_bridge_daemon():
    """
    Agar Windows muhitida bo'lsa, avtomatik ravishda fonda Bridge Daemon'ni ishga tushiradi.
    """
    global _DAEMON_STARTED
    with _DAEMON_LOCK:
        if _DAEMON_STARTED:
            return
        if not is_system_compatible():
            return  # Linux/Vercel serverless bo'lsa bridge daemon ishga tushmaydi, u faqat buyruq jo'natadi

        _DAEMON_STARTED = True
        worker_thread = threading.Thread(target=_pc_bridge_worker_loop, daemon=True, name="ATLAS_PC_Bridge_Daemon")
        worker_thread.start()
        try:
            print("[ATLAS] Realtime PC Cloud Bridge Worker ishga tushirildi!")
        except Exception:
            pass
