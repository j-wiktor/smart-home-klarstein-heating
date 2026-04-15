@service
@time_trigger("cron(0 22 * * *)")
def set_night_mode():
    # Ustawiamy progi nocne: 18.5 - 20.0
    input_number.set_value(entity_id="input_number.temp_min_salon", value=18.5)
    input_number.set_value(entity_id="input_number.temp_max_salon", value=20.0)
    log.info("DATA_LOG: Tryb NOCNY. Widełki ustawione na 18.5 - 20.0°C")

@service
@time_trigger("cron(30 6 * * *)")
def set_day_mode():
    # Przywracamy progi dzienne: 20.5 - 21.5
    input_number.set_value(entity_id="input_number.temp_min_salon", value=20.5)
    input_number.set_value(entity_id="input_number.temp_max_salon", value=21.5)
    log.info("DATA_LOG: Tryb DZIENNY. Widełki ustawione na 20.5 - 21.5°C")
