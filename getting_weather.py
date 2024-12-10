import requests

API_KEY = "widkjpsFWnAnvAqLN7X6WKukyEPeW17A"


def get_weather_data(lat, lon):
    """
    Запрашивает данные о погоде по координатам широты и долготы.
    :param lat: Широта
    :param lon: Долгота
    :return: Словарь с ключевыми параметрами погоды или ошибка
    """
    try:
        # URL для получения ключа местоположения
        location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
        params = {
            'apikey': API_KEY,
            'q': f'{lat},{lon}'
        }

        response = requests.get(location_url, params=params)

        if response.status_code == 200:
            location_data = response.json()
            location_key = location_data.get('Key')

            # Получение погодных условий
            forecast_url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}'
            forecast_params = {
                'apikey': API_KEY,
                'details': True
            }

            forecast_response = requests.get(forecast_url, params=forecast_params)
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()[0]

                # Извлекаем параметры
                weather_info = {
                    "Temperature (C)": forecast_data['Temperature']['Metric']['Value'],
                    "Humidity (%)": forecast_data['RelativeHumidity'],
                    "Wind Speed (km/h)": forecast_data['Wind']['Speed']['Metric']['Value'],
                    "Precipitation Probability (%)": forecast_data.get('PrecipitationProbability', 0)
                }
                # print(weather_info["Temperature (C)"])
                return weather_info
            else:
                return {"error": "Ошибка получения прогноза"}, forecast_response.status_code
        else:
            return {"error": "Ошибка получения локации"}, response.status_code

    except Exception as e:
        return {"error": str(e)}
