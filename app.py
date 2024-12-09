from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'liST7ItQKke0mlj7TYArcsvOe7Krk5jD'

# тестовая координата для проверки
test = [
    {'lat': 34.0522, 'lon': -118.2437} # Лос-Анджелес
]

# Определяем маршрут для обработки GET-запроса на /weather
@app.route('/weather', methods=['GET'])
def get_weather():
    # Получаем координаты
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    # Если координаты не переданы в запросе, то используюм тестовые координаты
    if not latitude or not longitude:
        latitude, longitude = test[0]['lat'], test[0]['lon']
        print(f"Используем тестовые координаты: {latitude}, {longitude}")

    location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
    params = {
        'apikey': API_KEY,
        'q': f'{latitude},{longitude}'
    }

    # Инфа о местоположении
    response = requests.get(location_url, params=params)

    # Если всё хорошо, то продолжаем работу
    if response.status_code == 200:
        location_data = response.json()  # Преобразуем ответ в формат джейсон
        location_key = location_data.get('Key')

        # получаем данные о текущей погоде по locationKey
        forecast_url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}'
        forecast_params = {'apikey': API_KEY,
                           'details': True}

        # Лутаем данные о погоде
        forecast_response = requests.get(forecast_url, params=forecast_params)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()[0]

            # Извлекаем ключевые параметры из данных о погоде
            temperature = forecast_data['Temperature']['Metric']['Value']
            humidity = forecast_data['RelativeHumidity']
            wind_speed = forecast_data['Wind']['Speed']['Metric']['Value']
            precipitation_probability = forecast_data.get('PrecipitationProbability',0)

            #Ответ с итоговыми данными в формате джэйсон
            weather_info = {
                "Temperature (C)": temperature,
                "Humidity (%)": humidity,
                "Wind Speed (km/h)": wind_speed,
                "Precipitation Probability (%)": precipitation_probability
            }

            # Возвращаем данные в формате JSON
            return jsonify(weather_info)
        else:
            return jsonify({"error": "Ошибка получения прогноза"}), forecast_response.status_code
    else:
        return jsonify({"error": "Ошибка получения локации"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
