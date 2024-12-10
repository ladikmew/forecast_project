from flask import Flask, request, json
from getting_weather import get_weather_data
from weather_model import check_bad_weather

app = Flask(__name__)
#GET /weather?start_lat=34.0522&start_lon=-118.2437&end_lat=40.7128&end_lon=-74.0060 из лос-анджелеса в нью йорк

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Обработчик маршрута для получения данных о погоде.
    Принимает параметры start_lat, start_lon, end_lat, end_lon в запросе.
    """
    # Получаем начальные и конечные координаты из запроса
    start_lat = request.args.get('start_lat')
    start_lon = request.args.get('start_lon')
    end_lat = request.args.get('end_lat')
    end_lon = request.args.get('end_lon')

    # Проверяем, что все координаты переданы
    if not (start_lat and start_lon and end_lat and end_lon):
        response = {"error": "Укажите, пожалуйста начальные и конечные координаты вашего маршрута :)"}
        return json.dumps(response, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}

    # Получаем данные о погоде для начальной точки
    start_weather = get_weather_data(start_lat, start_lon)
    if "error" in start_weather:
        response = {"error": f"Ошибка для начальной точки: {start_weather['error']}"}
        return json.dumps(response, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}

    # Получаем данные о погоде для конечной точки
    end_weather = get_weather_data(end_lat, end_lon)
    if "error" in end_weather:
        response = {"error": f"Ошибка для конечной точки: {end_weather['error']}"}
        return json.dumps(response, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}

    # Оценка погодных условий для начальной точки
    start_weather_status = check_bad_weather(
        start_weather["Temperature (C)"],
        start_weather["Wind Speed (km/h)"],
        start_weather["Precipitation Probability (%)"],
        start_weather["Humidity (%)"]
    )

    # Оценка погодных условий для конечной точки
    end_weather_status = check_bad_weather(
        end_weather["Temperature (C)"],
        end_weather["Wind Speed (km/h)"],
        end_weather["Precipitation Probability (%)"],
        end_weather["Humidity (%)"]
    )

    # Подготовка ответа с результатами для обеих точек
    result = {
        "start_point": {
            "coordinates": {"lat": start_lat, "lon": start_lon},
            "weather": start_weather,
            "status": start_weather_status
        },
        "end_point": {
            "coordinates": {"lat": end_lat, "lon": end_lon},
            "weather": end_weather,
            "status": end_weather_status
        }
    }

    return json.dumps(result, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run(debug=True)
