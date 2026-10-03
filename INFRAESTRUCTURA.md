# Infraestructura — SysOps & DevOps Lab

Referencia de red de los servicios desplegados en los dos entornos de la arquitectura híbrida.

Nota: este documento es una versión simplificada para el repositorio público. No incluye IPs, dominios reales, contraseñas ni tokens.

## Entorno local (Home Lab)

DNS local: Pi-hole, los dominios internos (`.lan`) resuelven dentro de la red doméstica.
Reverse proxy: Nginx Proxy Manager, con panel de administración accesible solo en red local.

| Servicio | Contenedor | Imagen | Acceso |
|---|---|---|---|
| Pi-hole | `local-dns-pihole` | `pihole/pihole:latest` | Solo vía reverse proxy |
| Portainer | `local-portainer` | `portainer/portainer-ce:latest` | Red local |
| Uptime Kuma | `local-uptime-kuma` | `louislam/uptime-kuma:1` | Red local |
| Nginx Proxy Manager | `local-proxy` | `jc21/nginx-proxy-manager:latest` | Red local |
| Selenium (Chromium) | `local-selenium` | `seleniarm/standalone-chromium:latest` | Red local (noVNC) |
| Scraper Bot | `local-scraper-bot` | build local | Sin panel web |
| Wallapop Hunter | `local-wallapop-hunter` | build local | Sin panel web |

## Entorno VPS (DigitalOcean)

DNS local: Pi-hole, configurado de forma independiente al del sistema.
Reverse proxy: Nginx Proxy Manager, con dominios públicos propios.
SSL: Let's Encrypt, renovación automática vía NPM en todos los subdominios públicos.

| Servicio | Contenedor | Acceso |
|---|---|---|
| Pi-hole | `local-dns-pihole` | Solo vía reverse proxy |
| Portainer | `local-portainer` | Dominio público (autenticado) |
| Uptime Kuma | `local-uptime-kuma` | Dominio público (autenticado) |
| Nginx Proxy Manager | `local-proxy` | Admin restringido |
| Selenium (Chromium) | `local-selenium` | Interno (noVNC) |
| Scraper Bot | `local-scraper-bot` | Sin panel web, monitorizado vía socket Docker |
| Wallapop Hunter | `local-wallapop-hunter` | Sin panel web |

## Notas de configuración

- Pi-hole no expone su puerto web directamente en ningún entorno; el acceso siempre pasa por el reverse proxy.
- Uptime Kuma y Portainer tienen montado el socket de Docker para poder monitorizar y gestionar contenedores.
- Las credenciales y variables sensibles se gestionan vía `.env`, excluido del control de versiones.
- `.gitignore` excluye los datos reales de Pi-hole y NPM, así como los logs de los bots. Existen en disco en cada entorno pero no se sincronizan vía Git.
- Flujo de despliegue: el entorno local es la única fuente que hace `git push`. El VPS recibe el despliegue automáticamente vía GitHub Actions al hacer push a `main`.

---
Última actualización: Octubre 2026
