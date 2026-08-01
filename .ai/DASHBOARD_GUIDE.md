# Dashboard Guide — HA Irrigation Engine

## UI Principles
- **Mobile First & Responsive**: Designed primarily for mobile usage (smartphones, Home Assistant companion app) and tablet dashboards.
- **Zero Business Logic**: The dashboard is strictly a representation layer. It must NEVER execute calculations, timers, or state logic directly in templates. All states must be driven by backend HA helpers/sensors.
- **Professional Design**: Premium aesthetic using Mushroom Cards, Bubble Card, ApexCharts, and card-mod.

## Key UI Components
1. **Multi-Zone View**: Card grid summarizing active status, flow rate, battery level, and remaining irrigation time per device/zone.
2. **Quick Action Controls**: Buttons for fixed irrigation durations (5, 10, 20, 30, 60 minutes).
3. **Master Controls**: "Parar todo" (Stop All) and "Regar todo" (Water All) master controls.
4. **Telemetry & Analytics**: ApexCharts card showing historical water consumption (daily, weekly, monthly).
5. **Safety Visualizations**: Active warning badges for low battery, offline devices, or valve stuck errors.
