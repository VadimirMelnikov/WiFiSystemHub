from flask import Flask, request, render_template, jsonify
#from flasgger import Swagger
import json
import random
import time

from src.SignalService import SignalService

# настройка приложения
path_to_config = r"C:\Users\HONOR\PycharmProjects\WIFACTORY\backend\src\resources\appConf.json"
with open(path_to_config, 'r', encoding='utf-8') as file:
    app_config = json.load(file)

app = Flask('WiFiSystemHub')
#swagger = Swagger(app, template_file=r"D:\Proggers\Python\WiFiSystemHub\backend\src\resources\swagger.yaml")
service = SignalService(app_config)

#---------------------
# Список возможных групп датчиков
GROUPS = ['Температура', 'Влажность', 'Давление']
# Генерация случайного значения в зависимости от группы
def get_random_value(group):
    if group == 'Температура':
        return round(15 + random.uniform(0, 10), 1)  # °C
    elif group == 'Влажность':
        return round(30 + random.uniform(0, 50), 1)  # %
    elif group == 'Давление':
        return round(950 + random.uniform(0, 100), 1)  # мм рт.ст.
    else:
        return round(random.uniform(0, 100), 1)
# Определение статуса датчика на основе значения
def get_status(value, group):
    if group == 'Температура':
        if value < 17:
            return 'inactive'
        else:
            return 'active'
    elif group == 'Влажность':
        if value < 40:
            return 'inactive'
        else:
            return 'active'
    elif group == 'Давление':
        if value < 960 or value > 1040:
            return 'inactive'
        else:
            return 'active'
    else:
        return 'active' if random.random() > 0.2 else 'inactive'
def get_unit(group):
    return {
        'Температура': '°C',
        'Влажность': '%',
        'Давление': 'мм рт.ст.'
    }.get(group, '')
#---------------------
@app.route("/")
def main_page():
    return render_template('index2.html',
                           sensors_data=service.get_signals_view())

@app.route("/operator")
def operator_page():
    # todo добавить страницу
    return "Пока заглушка"

@app.route("/data", methods=['GET'])
def send_signal():
    data = json.loads(request.args.get('data'))
    return service.save_or_get_signal(data)

@app.route("/view", methods=['GET'])
def get_view():
    #---------------------заглушка типо
    sensors_data = []
    for i, group in enumerate(GROUPS):
        value = get_random_value(group)
        status = get_status(value, group)
        unit = get_unit(group)

        sensors_data.append({
            'id': i + 1,
            'group': group,
            'value': value,
            'unit': unit,
            'status': status
        })
    return jsonify(sensors_data)
    #----------------
    #return json.dumps(service.get_signals_view(), ensure_ascii=False)

@app.route("/history", methods=['GET'])
def get_history():
    group_id = request.args.get('id')
    return service.get_sinals_history_by_group_id(group_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)