from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import requests
import json
import os

from src.services.DeviceService import DeviceService
from src.services.MQTTPublisher import MQTTPublisher

path_to_config = os.path.join(os.path.dirname(__file__), '..', 'resources', 'mongoConfig.json')
with open(path_to_config, 'r', encoding='utf-8') as file:
    mongo_config = json.load(file)
app = Flask('WiFiSystemHub')
CORS(app, origins="*")
service = DeviceService(mongo_config)
mqtt_publisher = MQTTPublisher()
@app.route('/sensors', methods=['GET'])
def get_sensors():
    return service.get_sensors()

@app.route('/actuators', methods=['GET'])
def get_actuators():
    return service.get_actuators()

@app.route('/history', methods=['GET'])
def get_history():
    group = request.args.get('group')
    return service.get_history_by_group(group)

@app.route('/data', methods=['PUT'])
def put_data():
    data = request.args.get('data')
    try:
        float(data)
        mqtt_publisher.send_data(data)
        return jsonify({'message': 'data send successfully'}), 200
    except ValueError:
        abort(400)


@app.errorhandler(400)
def handle_400(error):
    return jsonify({'message': 'data must be numeric'}), 400