## Funcionalidades objetivo

### Dashboard
- Diseño moderno y mobile-first.
- Mushroom Cards, Bubble Card, ApexCharts y card-mod cuando aporten valor.
- Vista de múltiples zonas de riego.
- Botones de riego rápido (5, 10, 20, 30 y 60 minutos).
- Indicador de tiempo restante.
- Estado visual de cada válvula.
- Botones "Parar todo" y "Regar todo".
- Estadísticas de consumo diario, semanal y mensual.

### Motor de riego
- Inicio y parada manual.
- Temporizadores.
- Watchdog para evitar válvulas abiertas indefinidamente.
- Programación (scheduler).
- Notificaciones al finalizar el riego.
- Preparado para cancelar el riego por lluvia.

### Adaptadores
- Primer adaptador: SONOFF SWV-BSP (Zigbee2MQTT).
- Descubrimiento automático de entidades a partir del `switch`.
- Arquitectura preparada para futuros adaptadores (ESPHome, Shelly, Tuya, MQTT genérico).

### Calidad
- Código modular y reutilizable.
- Cobertura de pruebas para la lógica principal.
- Documentación actualizada con cada cambio.