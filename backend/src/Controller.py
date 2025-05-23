from flask import Flask, request, render_template
from flasgger import Swagger
import json

from src.SignalService import SignalService

# настройка приложения
path_to_config = r"D:\Proggers\Python\WiFiSystemHub\backend\src\resources\appConf.json"
with open(path_to_config, 'r', encoding='utf-8') as file:
    app_config = json.load(file)

app = Flask('WiFiSystemHub')
swagger = Swagger(app, template_file=r"D:\Proggers\Python\WiFiSystemHub\backend\src\resources\swagger.yaml")
service = SignalService(app_config)


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
    return json.dumps(service.get_signals_view(), ensure_ascii=False)

@app.route("/history", methods=['GET'])
def get_history():
    group_id = request.args.get('id')
    return service.get_sinals_history_by_group_id(group_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)