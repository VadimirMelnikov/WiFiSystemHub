from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

from flask import Flask, request, render_template
# from flasgger import Swagger
import json

from Repository import Repository
from Signal import Signal
from src.SignalService import SignalService

app = Flask('WiFiSystemHub')

# app.config['SWAGGER'] = {
#     'title': 'WiFiSystemHub',
#     'version': '1.0',
#     'description': "Система мониторинга с вай-фай покрытием",
#     'uiversion': 3
# }
# Swagger(app, template_file="swagger.yaml")

# настройка приложения
path_to_config = r"D:\Proggers\Python\WiFiSystemHub\backend\src\resources\appConf.json"

with open(path_to_config, 'r', encoding='utf-8') as file:
    app_config = json.load(file)

service = SignalService(app_config)


@app.route("/")
def main_page():
    return render_template('index2.html',
                           sensors_data=service.get_signals_view())

@app.route("/data", methods=['GET'])
def send_signal():
    data = json.loads(request.args.get('data'))
    return service.save_or_get_signal(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)