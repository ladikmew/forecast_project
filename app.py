from flask import Flask, request, render_template, jsonify
from getting_weather import get_weather_data
from weather_model import check_bad_weather

app = Flask(__name__)


# GET /weather?start_lat=34.0522&start_lon=-118.2437&end_lat=40.7128&end_lon=-74.0060 из лос-анджелеса в нью йорк


# Обработчик GET-запроса для отображения html версии
@app.route('/', methods=['GET'])
def form():
    return render_template('html.html')


# Обработчик POST-запроса для получения данных о погоде
@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        # Получаем координаты из формы
        start_lat = request.form.get('start_lat')
        start_lon = request.form.get('start_lon')
        end_lat = request.form.get('end_lat')
        end_lon = request.form.get('end_lon')

        # Проверка на не заполненные ячейки
        if not (start_lat and start_lon and end_lat and end_lon):
            return render_template('error.html', message="Пожалуйста, заполните все поля :)")

        if not validate_coordinates(start_lat, start_lon, end_lat, end_lon):
            return render_template('error.html',
                                   message="Проверьте корректность координат и повторите попытку")

        # Получаем данные о погоде для начальной точки
        start_weather = get_weather_data(start_lat, start_lon)
        if "error" in start_weather:
            print(f"Ошибка при получении погоды для начальной точки: {start_weather['error']}")
            return render_template('error.html',
                                   message=f"Ошибка при получении данных о погоде для начальной точки, попробуйте ввести корректные координаты ещё раз")

        # Получаем данные о погоде для конечной точки
        end_weather = get_weather_data(end_lat, end_lon)
        if "error" in end_weather:
            print(f"Ошибка при получении погоды для конечной точки: {end_weather['error']}")
            return render_template('error.html',
                                   message=f"Ошибка при получении данных о погоде для конечной точки, попробуйте ввести корректные координаты ещё раз")

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
        print("Данные о погоде получены, это победа.")
        return render_template('weather.html', result=result)


    except ValueError as ve:
        return render_template('error.html', message=f"Ошибка данных: {ve}")

    except Exception as e:
        return render_template(
            'error.html',
            message="Произошла неожиданная ошибка, проверьте подключение к сети и повторите попытку"
        )

def validate_coordinates(start_lat, start_lon, end_lat, end_lon):
    """Проверка корректности координат."""
    try:
        start_lat = float(start_lat)
        start_lon = float(start_lon)
        end_lat = float(end_lat)
        end_lon = float(end_lon)

        if not (-90 <= start_lat <= 90 and -180 <= start_lon <= 180):
            return False
        if not (-90 <= end_lat <= 90 and -180 <= end_lon <= 180):
            return False
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(debug=True)
