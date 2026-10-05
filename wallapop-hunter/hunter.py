import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

SEARCH_KEYWORD = os.getenv('SEARCH_KEYWORD', 'ps5 pro')
MIN_PRICE = float(os.getenv('MIN_PRICE', 350.0))
MAX_PRICE = float(os.getenv('MAX_PRICE', 900.0))

try:
    SCAN_LIMIT = int(os.getenv('SCAN_LIMIT', 30))
except ValueError:
    SCAN_LIMIT = 30 

excluded_raw = os.getenv('EXCLUDED_WORDS', '')
EXCLUDED_WORDS = [word.strip().lower() for word in excluded_raw.split(',') if word.strip()]

WALLAPOP_URL = f"https://es.wallapop.com/app/search?keywords={SEARCH_KEYWORD.replace(' ', '%20')}&max_sale_price={MAX_PRICE}&order_by=newest"

MEMORY_FILE = "memoria.json"

print(f" CONFIGURACIÓN CARGADA:")
print(f"   - Buscando: {SEARCH_KEYWORD}")
print(f"   - Rango: {MIN_PRICE}€ - {MAX_PRICE}€")
print(f"   - Límite Escaneo: {SCAN_LIMIT} productos") # <--- AQUÍ VERÁS SI LO COGE
print(f"   - Ignorando: {EXCLUDED_WORDS}")

def cargar_memoria():
    if not os.path.exists(MEMORY_FILE): return {} 
    try:
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    except: return {}

def guardar_memoria(memoria):
    with open(MEMORY_FILE, "w") as f: json.dump(memoria, f, indent=4)

def enviar_tarjeta_telegram(texto, imagen_url=None):
    try:
        if imagen_url and "http" in imagen_url:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            payload = {
                "chat_id": CHAT_ID,
                "photo": imagen_url,
                "caption": texto,
                "parse_mode": "Markdown"
            }
            requests.post(url, data=payload)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
            
        print("Tarjeta enviada a Telegram.")
    except Exception as e:
        print(f"Error Telegram: {e}")

def get_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = None
    for i in range(5):
        try:
            print(f"🔌 Conectando con Chrome (Intento {i+1}/5)...")
            selenium_host = os.getenv('SELENIUM_HOST', 'selenium')
            driver = webdriver.Remote(
                command_executor=f"http://{selenium_host}:4444/wd/hub",
                options=options
            )
            print("Conexión con Chrome establecida.")
            return driver
        except Exception as e:
            print(f"Chrome no está listo. Esperando 5s...")
            time.sleep(5)
    raise Exception("Imposible conectar tras 5 intentos.")

def cazar():
    print(f"\n Escaneando Wallapop...")
    
    memoria = cargar_memoria()
    print(f"Memoria cargada: {len(memoria)} productos.")

    driver = None
    try:
        driver = get_driver()
        driver.get(WALLAPOP_URL)
        time.sleep(3) 
        
        # CÁLCULO DE SCROLLS DINÁMICO
        num_scrolls = int(SCAN_LIMIT / 10) + 1
        print(f" Ejecutando {num_scrolls} scrolls para llegar a {SCAN_LIMIT} items...")
        
        for i in range(num_scrolls):
            driver.execute_script(f"window.scrollTo(0, {(i+1)*1500});")
            time.sleep(1.5)

        productos = driver.find_elements(By.CSS_SELECTOR, "a[href*='/item/']")
        print(f" Elementos cargados: {len(productos)}")

        hallazgos = [] 
        cambios_en_memoria = False
        
        for prod in productos[:SCAN_LIMIT]:
            try:
                raw_text = prod.text
                link = prod.get_attribute("href")
                
                # FOTO ANUNCIO
                foto_url = None
                try:
                    img_elem = prod.find_element(By.TAG_NAME, "img")
                    foto_url = img_elem.get_attribute("src")
                except: foto_url = None 

                # FILTRO ANTI-RESERVADOS
                if "reservado" in raw_text.lower() or "vendido" in raw_text.lower():
                    continue

                # PARSEO
                lineas = [l.strip() for l in raw_text.split('\n') if l.strip()]
                precio_actual = 0.0
                titulo = "Título desconocido"
                
                for linea in lineas:
                    if "€" in linea:
                        try:
                            p = float(linea.replace('€', '').replace('.', '').replace(',', '.').strip())
                            precio_actual = p
                        except: continue
                    elif len(linea) > 5 and "envío" not in linea.lower():
                        titulo = linea

                if precio_actual == 0: continue
                titulo_lower = titulo.lower()

                # FILTROS
                if not (MIN_PRICE <= precio_actual <= MAX_PRICE): continue
                if any(bad in titulo_lower for bad in EXCLUDED_WORDS): continue
                if "ps5" not in titulo_lower and "playstation 5" not in titulo_lower: continue

                # COMPARACIÓN
                titulo_aviso = None

                if link not in memoria:
                    titulo_aviso = " NUEVO PRODUCTO DETECTADO"
                    print(f"      Encontrado: {titulo} ({precio_actual}€)")
                    memoria[link] = precio_actual
                    cambios_en_memoria = True
                else:
                    precio_viejo = memoria[link]
                    if precio_actual < precio_viejo:
                        titulo_aviso = " BAJADA DE PRECIO DETECTADA"
                        print(f"      ¡Bajada!: {titulo} ({precio_viejo}€ -> {precio_actual}€)")
                        memoria[link] = precio_actual
                        cambios_en_memoria = True
                    else:
                        if precio_actual != precio_viejo:
                            memoria[link] = precio_actual
                            cambios_en_memoria = True
                        continue

                hallazgos.append({
                    "aviso": titulo_aviso,
                    "titulo": titulo,
                    "precio": precio_actual,
                    "link": link,
                    "foto": foto_url
                })

            except Exception as e:
                continue
        
        if cambios_en_memoria:
            guardar_memoria(memoria)

        if len(hallazgos) > 0:
            print(f" Enviando {len(hallazgos)} tarjetas...")
            for item in hallazgos:
                msg = (
                    f"**{item['aviso']}**\n"
                    f"{item['titulo']}\n"
                    f"**{item['precio']} €**\n"
                    f"[Ver en Wallapop]({item['link']})"
                )
                enviar_tarjeta_telegram(msg, item['foto'])
                time.sleep(1)
        else:
            print("💤 Sin novedades.")

    except Exception as e:
        print(f"Error general: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    MINUTOS = 3
    print(f" Hunter V12 (Configurable - Cada {MINUTOS} min)")
    cazar() 
    import schedule
    schedule.every(MINUTOS).minutes.do(cazar)
    while True:
        schedule.run_pending()
        time.sleep(60)
