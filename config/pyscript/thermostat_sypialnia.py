import datetime

@state_trigger("sensor.temperature_sensor_sypialnia_temperature", "input_number.temp_min_sypialnia", "input_number.temp_max_sypialnia")
@time_trigger("once(22:00)", "once(06:00)")
def termostat_sypialnia():
    # 1. Zarządzanie harmonogramem
    teraz = datetime.datetime.now().hour
    
    # Określamy docelowe progi na podstawie godziny
    if teraz >= 22 or teraz < 6:
        d_min, d_max = 18.5, 20.5
        tryb = "NOCNY"
    else:
        d_min, d_max = 20.5, 21.5
        tryb = "DZIENNY"

    # Sprawdzamy i ewentualnie korygujemy suwaki
    current_min = float(state.get("input_number.temp_min_sypialnia") or 0)
    current_max = float(state.get("input_number.temp_max_sypialnia") or 0)
    
    if current_min != d_min or current_max != d_max:
        service.call("input_number", "set_value", entity_id="input_number.temp_min_sypialnia", value=d_min)
        service.call("input_number", "set_value", entity_id="input_number.temp_max_sypialnia", value=d_max)
        log.info(f"TERMOSTAT: Automatyczna zmiana na tryb {tryb} ({d_min} - {d_max}°C)")

    # 2. Pobieranie aktualnej temperatury
    t_teraz = float(state.get("sensor.temperature_sensor_sypialnia_temperature") or 0)
    
    # 3. Logika sterowania Shelly Sypialnia
    # Używamy d_min i d_max, żeby mieć pewność, że sterujemy według aktualnego trybu
    if t_teraz < d_min:
        if state.get("switch.shelly_sypialnia") != "on":
            service.call("switch", "turn_on", entity_id="switch.shelly_sypialnia")
            log.info(f"TERMOSTAT: {tryb} - Włączam grzejnik (Temp: {t_teraz})")
    elif t_teraz > d_max:
        if state.get("switch.shelly_sypialnia") != "off":
            service.call("switch", "turn_off", entity_id="switch.shelly_sypialnia")
            log.info(f"TERMOSTAT: {tryb} - Wyłączam grzejnik (Temp: {t_teraz})")
