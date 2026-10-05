import os
import time
import requests
import schedule
from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()

# Cliente Amadeus
amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY').strip(),
    client_secret=os.getenv('AMADEUS_API_SECRET').strip()
)

# Configuración Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
        print("Telegram enviado.")
    except Exception as e:
        print(f"Error enviando Telegram: {e}")

def buscar_vuelos():
    origin = os.getenv('ORIGIN_CODE', 'MAD').strip()
    destination = os.getenv('DEST_CODE', 'CDG').strip()
    date = os.getenv('DEPARTURE_DATE').strip()
    max_price = float(os.getenv('MAX_PRICE', 100))
    
    print(f"\n[RADAR] Buscando Top 3: {origin} -> {destination} ({date})")

    try:
        # Petición a Amadeus
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1,
            currencyCode='EUR',
            max=10 
        )

        if not response.data:
            print("No hay vuelos disponibles.")
            return

        # 1. TRADUCTOR DE AEROLÍNEAS
        # La API nos da los códigos en una sección separada llamada 'dictionaries'
        nombres_aerolineas = response.result.get('dictionaries', {}).get('carriers', {})

        # 2. CONSTRUIR EL MENSAJE
        msg = f"**TOP 3 VUELOS: {origin} a {destination}**\n Fecha: {date}\n\n"
        
        precios = []

        # 3. BUCLE DE LOS 3 MEJORES
        # Iteramos solo los primeros 3 resultados (que ya vienen ordenados por precio)
        for i, vuelo in enumerate(response.data[:3]):
            price = float(vuelo['price']['total'])
            currency = vuelo['price']['currency']
            
            codigo = vuelo['validatingAirlineCodes'][0]
            nombre = nombres_aerolineas.get(codigo, codigo)

            icono = "1" if i == 0 else "🥈" if i == 1 else "🥉"
            
            msg += f"{icono} **{price} {currency}** | {nombre}\n"
            precios.append(price)

        msg += f"\n Objetivo: < {max_price} EUR"
        
        mejor_precio = precios[0]
        print(f" Mejores precios encontrados: {precios}")

        if mejor_precio <= max_price:
            print(" ¡Precio encontrado! Enviando Telegram...")
            enviar_telegram(msg)
        else:
            print(f" El más barato ({mejor_precio}€) sigue por encima de {max_price}€. A dormir.")

    except ResponseError as error:
        print(f" Error de Amadeus: {error}")
    except Exception as e:
        print(f" Error general: {e}")

if __name__ == "__main__":
    print(" mRadar de Vuelos Iniciado (Daemon Mode)")
    
    # Primera ejecución al arrancar
    buscar_vuelos()

    # Programar cada 4 horas
    schedule.every(4).hours.do(buscar_vuelos)

    while True:
        schedule.run_pending()
        time.sleep(60)
