import datetime

SENSOR_TEMP = "sensor.temperature_sensor_pracownia_temperature"
HEATER_SWITCH = "switch.shelly_pracownia"
MIN_TEMP_HELPER = "input_number.temp_min_pracownia"
MAX_TEMP_HELPER = "input_number.temp_max_pracownia"

@state_trigger(SENSOR_TEMP, MIN_TEMP_HELPER, MAX_TEMP_HELPER)
@time_trigger("once(22:00)", "once(06:00)")
def workroom_thermostat_control():
    """
    Standardized thermostat logic for the Workroom.
    Day (06:00-22:00): 20.5 - 21.5°C
    Night (22:00-06:00): 18.5 - 20.5°C
    """
    current_hour = datetime.datetime.now().hour
    
    # 1. Schedule Definition (Standardized)
    if current_hour >= 22 or current_hour < 6:
        target_min, target_max = 18.5, 20.5
        mode = "NIGHT"
    else:
        target_min, target_max = 20.5, 21.5
        mode = "DAY"

    # 2. Sync Home Assistant UI Helpers
    current_min = float(state.get(MIN_TEMP_HELPER) or 0)
    current_max = float(state.get(MAX_TEMP_HELPER) or 0)
    
    if current_min != target_min or current_max != target_max:
        service.call("input_number", "set_value", entity_id=MIN_TEMP_HELPER, value=target_min)
        service.call("input_number", "set_value", entity_id=MAX_TEMP_HELPER, value=target_max)
        log.info(f"WORKROOM: Mode switched to {mode} ({target_min} - {target_max}°C)")

    # 3. Control Logic
    current_temp = float(state.get(SENSOR_TEMP) or 0)
    
    if current_temp < target_min:
        if state.get(HEATER_SWITCH) != "on":
            service.call("switch", "turn_on", entity_id=HEATER_SWITCH)
            log.info(f"WORKROOM: {mode} - Heating ON (Current: {current_temp}°C)")
            
    elif current_temp > target_max:
        if state.get(HEATER_SWITCH) != "off":
            service.call("switch", "turn_off", entity_id=HEATER_SWITCH)
            log.info(f"WORKROOM: {mode} - Heating OFF (Current: {current_temp}°C)")