# IoT Smart Heating Control System 🌡️💻

## Project Overview
An automated heating management system designed for **Klarstein Wonderwall** and other infrared heating units from this company. By bypassing producer controll modules you can apply this solutions to any heating plug powered heaters. This project focuses on building a solid data pipeline to monitor environmental conditions and optimize energy consumption using Python and Home Automation tools.

**Target Role:** Transitioning into **Data Engineering** by applying cost-optimization strategies, energy efficiency logic, and real-time data processing. Learning Python, Linux and Data on real-life enviorment. 

## 💡 Engineering Decisions: Unified Control Strategy
The system integrates various Klarstein heater models with different proprietary control methods (capacitive touch, radio frequency, internal thermostats). To ensure a unified and reliable data pipeline, I implemented the following hardware strategies:

### 1. Bypassing Wired/Capacitive Controllers
- **The Challenge:** Heaters with built-in capacitive buttons required manual interaction (physical button press) every time power was restored. An initial attempt to automate this using Shelly Uni to mimic button presses proved unreliable due to wire-length sensitivity and signal interference.
- **The Solution:** I modified the internal wiring using WAGO connector to put the units in an **"Always Heat when Powered"** mode. This effectively moved the "intelligence" from the heater's unreliable built-in controller to my centralized Python and Home Assistant logic.

### 2. Bypassing Radio-Controlled Units (2.4GHz)
- **The Challenge:** One model relied on a 2.4GHz remote thermostat, which also required a manual "wake-up" after power-on.
- **The Solution:** Instead of adding unnecessary complexity (RF bridges/gateways), I applied the same WAGO + Shelly Plug S bypass. This reduced hardware overhead and centralized all control into the Zigbee/Wi-Fi mesh.

### 3. Why This Approach?
- **Reliability:** Hardware-level bypasses eliminate the "state-mismatch" common in software-only integrations.
- **Accuracy:** Built-in sensors showed a **1-3°C discrepancy** due to casing heat. External Sonoff sensors provide true ambient data, critical for precise Data Engineering analysis.
- **Data Uniformity:** Every heater now reports power consumption via Shelly Plug S, providing a consistent schema for my future InfluxDB data pipeline.
- **Abstraction:** All heaters, regardless of original tech, are now identical entities in Home Assistant and my Python scripts.


## 🏗️ Tech Stack & Architecture
- **Language:** Python (Pyscript for custom automation logic)
- **Home Lab:** Intel NUC DN2820FYK (Linux Mint XFCE)
- **Data Integration:** Home Assistant, Zigbee2MQTT
- **Sensors & Actuators:** 
  - **Sonoff SNZB-02D**: Primary Zigbee LCD sensors for multi-room monitoring.
  - **Xiaomi LYWSD03MMC**: Legacy sensor used for initial bedroom setup.
  - **Shelly Plug S MTR Gen3**: Power monitoring & actuator via Wi-Fi.
  - **Sonoff Zigbee 3.0 USB Dongle Plus (ZBDongle-E)**: Central Zigbee coordinator.
- **Infrastructure:** Docker (Planned: InfluxDB + Grafana for historical analysis).

## 🐍 Python Automations (`/config/pyscript/`)
The system uses a hybrid approach: **Home Assistant Input Helpers** (Global Variables) allow for easy UI adjustments of temperature thresholds, while **Python scripts** handle the complex logic:
- **`thermostat_sypialnia.py`**: Manages real-time heating states.
- **`night_optimizer.py`**: Implements energy-saving setbacks during sleep cycles.

## 📈 Data Pipeline Goals
1. **Ingestion:** Real-time data collection from Zigbee and Wi-Fi devices.
2. **Processing:** Python-based state management and energy optimization.
3. **Storage (In Progress):** Implementation of InfluxDB for time-series data storage.
4. **Visualization (Planned):** Grafana dashboards for power vs. temperature trend analysis.

## 🚀 How to Run
-🚧 Work on this section in progress. 