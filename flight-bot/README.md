# ✈️ Flight Price Tracker (Amadeus API)

Un bot especializado en la monitorización de precios de vuelos utilizando la **API oficial de Amadeus** (GDS).

A diferencia de los scrapers tradicionales que leen el HTML de una web, este bot se comunica directamente con los sistemas de reservas globales mediante **OAuth2**, garantizando datos precisos, legales y sin riesgo de bloqueos por IP.

# Funcionalidades

- **Integración API REST:** Autenticación segura mediante tokens (Client Credentials Flow).
- **Umbral de Precio:** Solo notifica si el vuelo encontrado está por debajo del precio máximo que tú definas.
- **Renovación de Tokens:** Gestión automática de la caducidad de las credenciales de la API.
- **Rutas Flexibles:** Configuración de origen, destino y fechas desde variables de entorno.

## Stack Tecnológico

- **Python 3.9**
- **Amadeus Self-Service API** (Flight Offers Search)
- **Requests** (Gestión de tokens y peticiones HTTP)
- **Docker & Docker Compose**
- **Telegram Bot API**

## Requisitos Previos

Necesitas una cuenta de desarrollador (gratuita) en Amadeus para obtener las claves:
1. Registro en [developers.amadeus.com](https://developers.amadeus.com).
2. Crea una nueva "App".
3. Obtén tu `API Key` y `API Secret`.

**Configuración:**
   Crea un archivo `.env` con credenciales y preferencias de viaje:
   ```ini
   # --- Telegram ---
   TELEGRAM_TOKEN=tu_token
   TELEGRAM_CHAT_ID=tu_id

   # --- Amadeus API Credenciales ---
   AMADEUS_CLIENT_ID=tu_api_key_de_amadeus
   AMADEUS_CLIENT_SECRET=tu_api_secret_de_amadeus

   # --- Configuración del Viaje ---
   ORIGIN=MAD        # Código IATA (ej: Madrid)
   DESTINATION=TYO   # Código IATA (ej: Tokyo)
   DEPARTURE_DATE=2024-12-25
   MAX_PRICE=800     # Solo avisa si es menor a esto
   ```
