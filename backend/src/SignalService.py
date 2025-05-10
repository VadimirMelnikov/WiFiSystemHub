import json

from Repository import Repository
from Signal import Signal

class SignalService:
    def __init__(self):
        self.rep = Repository(
                'mongodb://localhost:27017/',
                'esp_database',
                'esp_collection'
                )
        self.sensor_config = json.loads('sensorConfig.json')

    def save_or_get_signal(self, data):
        signal = Signal(
            name=data['name'],
            mode=data['mode'],
            param=data['param'])
        response = "{}"
        if signal.mode == "Sensor":
            self.rep.save_signal_to_db(signal)

        else:
            response = self.rep.get_data_by_client_name(signal)
        return json.dumps(response)

    def get_signals_view(self):
        data = self.rep.get_all_signals()
        #todo нужно возращать json всех датчиков в нужном виде
        return
