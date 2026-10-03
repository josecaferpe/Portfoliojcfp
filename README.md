# SysOps & DevOps Lab

Laboratorio personal donde pongo en práctica conceptos de administración de sistemas, automatización y DevOps. El repositorio centraliza varias herramientas y servicios desplegados en una arquitectura híbrida (VPS + Home Lab), usando Docker, infraestructura como código y monitorización.

Estado actual: desplegado y operativo, con despliegue automático vía GitHub Actions.

## Proyectos

### Wallapop Hunter (`./wallapop-hunter`)
Scraper con Selenium para detectar oportunidades de mercado en Wallapop en tiempo real.
- Tech: Selenium WebDriver, Chrome Headless, Python, Docker
- Incluye evasión de detección básica, scroll infinito dinámico y persistencia de resultados en JSON

### Scrapper Bot (`./scrapper-bot`)
Bot de vigilancia ligero para webs estáticas, que detecta actualizaciones de contenido y envía alertas.
- Tech: BeautifulSoup4, Requests, Python
- Consumo mínimo de recursos y parsing HTML rápido

### Infraestructura & Monitorización (`./uptime-kuma`)
Monitorización de disponibilidad desplegada de forma redundante en ambos entornos.
- Tech: Uptime Kuma (self-hosted)
- Una instancia en el VPS (India) supervisa servicios públicos; otra en el Home Lab supervisa contenedores y servicios internos de la red doméstica

### DNS y Reverse Proxy local (`./local-dns`)
DNS local y proxy inverso para acceder a los paneles de administración del Home Lab (Portainer, Uptime Kuma, etc.) mediante dominios internos en vez de IPs y puertos.
- Tech: Pi-hole (DNS + bloqueo de publicidad), Nginx Proxy Manager (proxy inverso + SSL), Docker
- Dominios `.lan` internos (`portainer.lan`, `uptime.lan`...), certificados gestionados de forma centralizada

## Arquitectura

El sistema corre en un modelo híbrido:

| Entorno | Ubicación | Servicios | Hardware |
|---|---|---|---|
| VPS (producción) | DigitalOcean, Bangalore | Monitorización, bots en producción |
