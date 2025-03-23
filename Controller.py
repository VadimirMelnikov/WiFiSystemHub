from flask import Flask, request
from flasgger import Swagger
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

@app.route("/data", methods=['GET'])
def send_signal():
    data = json.loads(request.args.get('data'))
    signal = Signal(
                    name=data['name'],
                    mode=data['mode'],
                    param=data['param'])
    response = "{}";
    if signal.mode == "Sensor":
        rep.save_signal_to_db(signal)

    else:
        response = rep.get_data_by_client_name(signal)
    return json.dumps(response)





if __name__ == "__main__":
    app.run(debug=True, port=5000)