# Arquitectura

La arquitectura queda congelada.

Dashboard

↓

Scripts

↓

Automations

↓

Engine

↓

Device Adapter

↓

Home Assistant

↓

Device

---

## Dashboard

Solo UI.

Nunca lógica.

---

## Engine

Toda la lógica.

No conoce fabricantes.

No conoce entidades.

Solo conoce dispositivos y zonas.

---

## Adapter

Convierte un dispositivo físico en un dispositivo lógico.

Debe existir un adaptador por fabricante.

Ejemplos

Sonoff

ESPHome

Shelly

Tuya

Generic MQTT

---

## Registry

El usuario únicamente configura

id

nombre

adapter

switch principal

Todo lo demás se descubre automáticamente.