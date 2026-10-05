# Wallapop Hunter 

Un sistema autónomo de **Web Scraping y Monitorización** diseñado para detectar productos específicos en Wallapop en tiempo real y notificar vía Telegram.

Desplegado con **Docker Compose** y **Selenium**, implementando lógica de evasión de detección y persistencia de datos.

## Características (

- **Dockerizado:** Despliegue en un clic con Docker Compose.
- **Memoria Persistente:** Evita duplicados y detecta si un producto ya fue notificado.
- **Rastreo de Precios:** Notifica si un producto conocido baja de precio.
- **Modo Visual:** Envía notificaciones a Telegram con la foto del producto, precio y enlace directo.
- **Evasión de Bots:** Usa Selenium con Chrome WebDriver y comportamiento humano (scroll dinámico, tiempos de espera aleatorios).
- **Filtros Inteligentes:**
  - *Anti-Reservados:* Ignora productos vendidos o reservados.
  - *Blacklist:* Filtra palabras clave no deseadas (ej: "mando", "caja").
  - *Smart Parse:* Analiza precios y títulos independientemente del formato del anuncio.

## Stack

- **Python 3.9**
- **Selenium WebDriver** (Chrome Headless)
- **Docker & Docker Compose**
- **Telegram Bot API**
- **memoria.json: Base de datos local (JSON) para persistencia.**

Este proyecto es para fines educativos y de aprendizaje de DevOps y Automatización.
