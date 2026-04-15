import datetime

# Configuration / Entity IDs
SENSOR_TEMP = "sensor.temperature_sensor_sypialnia_temperature"
MIN_TEMP_HELPER = "input_number.temp_min_sypialnia"
MAX_TEMP_HELPER = "input_number.temp_max_sypialnia"
HEATER_SWITCH = "switch.shelly_sypialnia"

@state_trigger(SENSOR_TEMP, MIN_TEMP_HELPER, MAX_TEMP_HELPER)
@time_trigger("once(22:00)", "once(06:00)")
def bedroom_thermostat_control():
    """
    Manages bedroom heating based on a time-of-day schedule and hysteresis logic.
    """
    current_hour = datetime.datetime.now().hour
    
    # Define target thresholds based on time of day (Night: 22:00-06:00)
    if current_hour >= 22 or current_hour < 6:
        target_min, target_max = 18.5, 20.5
        mode = "NIGHT"
    else:
        target_min, target_max = 20.5, 21.5
        mode = "DAY"

    # Sync Home Assistant UI helpers with schedule
    current_min = float(state.get(MIN_TEMP_HELPER) or 0)
    current_max = float(state.get(MAX_TEMP_HELPER) or 0)
    
    if current_min != target_min or current_max != target_max:
        service.call("input_number", "set_value", entity_id=MIN_TEMP_HELPER, value=target_min)
        service.call("input_number", "set_value", entity_id=MAX_TEMP_HELPER, value=target_max)
        log.info(f"THERMOSTAT: Auto-switched to {mode} mode ({target_min} - {target_max}°C)")

    # 2. Get current temperature
    current_temp = float(state.get(SENSOR_TEMP) or 0)
    
    # 3. Control Logic for Shelly Heater
    if current_temp < target_min:
        if state.get(HEATER_SWITCH) != "on":
            service.call("switch", "turn_on", entity_id=HEATER_SWITCH)
            log.info(f"THERMOSTAT: {mode} mode - Activating heater (Current Temp: {current_temp}°C)")
            
    elif current_temp > target_max:
        if state.get(HEATER_SWITCH) != "off":
            service.call("switch", "turn_off", entity_id=HEATER_SWITCH)
            log.info(f"THERMOSTAT: {mode} mode - Deactivating heater (Current Temp: {current_temp}°C)")