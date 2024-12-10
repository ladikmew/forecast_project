# Пороговые значения для определения плохих погодных условий
criteria = {
    "low_temp": 0,
    "high_temp": 35,
    "max_wind_speed": 50,
    "max_precip_prob": 70,
    "hmidity": 65
}


def check_bad_weather(temp, wind_speed, precip_prob, hmidity):
    """
    Определяет погодные условия на основе параметров.

    :param temp: температура в градусах цельсия
    :param wind_speed: скорость ветра в км/ч
    :param precip_prob: вероятность осадков в процентах
    :hmidity: влажность в процентах
    :return: вердикт по погоде на улице
    """
    if temp is not None and wind_speed is not None and precip_prob is not None and hmidity is not None:
        if temp < criteria["low_temp"]:
            return "Погода холоднее, чем комфортная"
        if temp > criteria["high_temp"]:
            return "Погода жарче, чем комфортная"
        if wind_speed > criteria["max_wind_speed"]:
            return "Сейчас за окном сильный ветер"
        if precip_prob > criteria["max_precip_prob"]:
            return "Высокая вероятность осадков"
        if hmidity > criteria["hmidity"]:
            return "Высокая влажность"
        return "Погода комфортная"
    else:
        return "Некорректные данные по погоде"
