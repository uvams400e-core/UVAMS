# UVAMS: Universal Alliance for Mission Safety
## VH Node: West Texas Independent Ground Segment

### Mission Objective
Stabilizing the global space traffic system through independent, non-cooperative RF tracking. The VH Node focuses on high-frequency "Ghost Signal" detection and Doppler-based orbital truth validation.

### Architecture
- **Sentry Mode**: Automated spectrum sweeping (70MHz - 6GHz) to detect uncatalogued assets.
- **Stabilizer Mode**: Precision Doppler tracking and CCSDS TDM data generation.
- **Hardware**: ADALM-PLUTO SDR + Custom Radio Mast Array.

### Data Standards
All tracking logs are formatted to **CCSDS TDM (XML)** for integration with the TraCSS-OASIS ecosystem.
