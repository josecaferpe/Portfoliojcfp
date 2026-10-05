# Scrapper Bot (General Purpose Monitor)

Un bot de monitorización web ligero y flexible, diseñado para rastrear cambios en sitios web estáticos y notificar actualizaciones vía **Telegram**.

Aunque es agnóstico y configurable, este proyecto nació como **"INAP Sniper"**, una herramienta específica para vigilar el portal del **INAP/BOE** y detectar automáticamente la publicación de fechas de exámenes y listas de admitidos, evitando la comprobación manual diaria de los interesados.


## Cómo funciona

A diferencia de *Wallapop Hunter* (que usa un navegador completo), este bot utiliza peticiones HTTP directas, lo que lo hace extremadamente ligero y rápido.

1.  Realiza peticiones `GET` a la URL objetivo.
2.  Analiza el HTML con **BeautifulSoup**.
3.  Compara el contenido con palabras clave definidas.
4.  Si hay coincidencia, envía una alerta Push a Telegram.

## Stack Tecnológico

- **Python 3.9**
- **Requests** (HTTP Client)
- **BeautifulSoup4** (HTML Parsing)
- **Telegram Bot API**
