import requests
import time
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- CONFIGURACIÓN ---
URL = os.getenv('TARGET_URL', 'https://sede.inap.gob.es/tai')
SEARCH_TEXT_RAW = os.getenv('SEARCH_TEXT', 'Convocatoria 2025')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 1800))

# CREDENCIALES
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
EMAIL_USER = os.getenv('EMAIL_USER')     
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD') 

LOG_FILE = "/app/logs/historial.txt"

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def log_to_file(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{message}\n")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = { "chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML" }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error Telegram: {e}")

def send_email(asunto, cuerpo):
    """Envío simple usando Gmail"""
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("Faltan datos de correo. Saltando envío.")
        return

    msg = EmailMessage()
    msg.set_content(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER # Nos lo enviamos a nosotros mismos (Infalible)

    try:
        # Conexión SSL directa a Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Error enviando Email: {e}")

def check_website():
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36' }
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        content = response.text.lower()
        keywords = [k.strip().lower() for k in SEARCH_TEXT_RAW.split(',')]
        
        for keyword in keywords:
            if keyword in content:
                return keyword
        return None
    except Exception as e:
        err = f"[{get_timestamp()}] Error conexión: {e}"
        print(err)
        log_to_file(err)
        return None

def main():
    minutes = CHECK_INTERVAL / 60
    inicio_msg = (f"[{get_timestamp()}] <b>Bot Iniciado</b>\n"
                  f"Objetivo: {URL}\n"
                  f"Frecuencia: {minutes} minutos")
    
    print(inicio_msg)
    log_to_file(inicio_msg)
    send_telegram(inicio_msg)
    
    found_mode = False 

    while True:
        found_keyword = check_website()
        
        if found_keyword:
            if not found_mode:
                # --- ALERTA ---
                timestamp = get_timestamp()
                texto_aviso = f"¡Han publicado algo! He encontrado: '{found_keyword.upper()}'"
                
                # 1. Telegram
                send_telegram(f"🚨 <b>¡ALERTA!</b>\n{texto_aviso}\n<a href='{URL}'>VER WEB</a>")
                
                # 2. Email 
                cuerpo_mail = f"Hola Jose Carlos,\n\n{texto_aviso}\n\nHora: {timestamp}\nLink: {URL}"
                send_email(f"URGENTE: {found_keyword.upper()} DETECTADO", cuerpo_mail)
                
                print(f"[{timestamp}] ALERTA ENVIADA")
                log_to_file(f"[{timestamp}] ALERTA ENVIADA: {found_keyword}")
                found_mode = True
            else:
                print(f"[{get_timestamp()}] Objetivo sigue visible (Esperando...)")
        else:
            print(f"[{get_timestamp()}] Sin cambios...")
            if found_mode: found_mode = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
