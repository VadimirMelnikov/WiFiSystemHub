from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

from flask import Flask, request, render_template
# from flasgger import Swagger
import json

from Repository import Repository
from Signal import Signal

app = Flask('WiFiSystemHub')
# app.config['SWAGGER'] = {
#     'title': 'WiFiSystemHub',
#     'version': '1.0',
#     'description': "Система мониторинга с вай-фай покрытием",
#     'uiversion': 3
# }
# Swagger(app, template_file="swagger.yaml")

rep = Repository(
                'mongodb://localhost:27017/',
                'esp_database',
                'esp_collection'
                )

# Данные о датчиках заглушка
sensors_data = [
    {"id": 1, "group": "Влажность", "value": 100, "unit": "%", "status": "normal"},
    {"id": 2, "group": "Уровень", "value": 180, "unit": "мм", "status": "error"},
    {"id": 3, "group": "Влажность", "value": 180, "unit": "%", "status": "warning"},
    {"id": 4, "group": "Давление", "value": 44, "unit": "кПа", "status": "normal"},
]

# Формирование статусов
def get_status_icon(status):
    if status == "normal":
        return "🟢"
    elif status == "warning":
        return "🟡"
    elif status == "error":
        return "🔴"
    else:
        return "⚪"

# Генерация графика
def generate_chart():
    # Данные для графика
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    pressure_1 = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600]
    pressure_2 = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]

    # Создание графика
    plt.figure(figsize=(8, 6))
    plt.plot(months, pressure_1, label='Pressure_1', color='blue')
    plt.plot(months, pressure_2, label='Pressure_2', color='green')
    plt.fill_between(months, pressure_1, pressure_2, color='lightgray', alpha=0.5)
    plt.xlabel('Month')
    plt.ylabel('Давление, кПа')
    plt.title('Показатели предприятия')
    plt.legend()

    # Сохранение графика в памяти
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Преобразование изображения в base64
    chart_url = base64.b64encode(img.getvalue()).decode()
    return f"data:image/png;base64,{chart_url}"

# Данные для уведомлений, датчиков и механизмов
notifications = [
    "14:23:33 23.02.2025 Сработала защита по превышению давления",
    "14:23:33 23.02.2025 Превышение допустимой температуры на датчике 4",
    "14:23:33 23.02.2025 Сработала защита по превышению давления",
    "14:23:33 23.02.2025 Превышение допустимой температуры на датчике 4",
    "14:23:33 23.02.2025 Сработала защита по превышению давления",
    "14:23:33 23.02.2025 Превышение допустимой температуры на датчике 4",
    "14:23:33 23.02.2025 Сработала защита по превышению давления"
]

sensors = [
    "Датчик 1: Температура 25°C",
    "Датчик 2: Давление 1.2 atm",
    "Датчик 3: Влажность 60%",
    "Датчик 4: Уровень воды 0.8 m"
]

mechanisms = [
    "Механизм 1: Работает нормально",
    "Механизм 2: Неисправен",
    "Механизм 3: Временная остановка",
    "Механизм 4: Работает с перегрузкой"
]




@app.route("/")
def main_page():
    # Получение текущей даты и времени
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # Обработка данных датчиков
    for sensor in sensors_data:
        sensor["status_icon"] = get_status_icon(sensor["status"])

    return render_template('index2.html',
                           sensors_data=sensors_data,
                           current_time=current_time)


@app.route('/operator')
def operator_page():
    chart_url = generate_chart()
    return render_template('index.html',
                           chart_url=chart_url,
                           notifications=notifications,
                           sensors=sensors,
                           mechanisms=mechanisms)


@app.route("/data", methods=['GET'])
def send_signal():
    data = json.loads(request.args.get('data'))
    signal = Signal(
                    name=data['name'],
                    mode=data['mode'],
                    param=data['param'])
    response = "{}"
    if signal.mode == "Sensor":
        rep.save_signal_to_db(signal)

    else:
        response = rep.get_data_by_client_name(signal)
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)