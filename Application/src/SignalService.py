import json
from datetime import datetime, timedelta
import os
from src.Repository import Repository
from src.Signal import Signal

#    "url": "mongodb://mongo:27017/",
# "url": "mongodb://localhost:27017/",

class SignalService:
    def __init__(self, config):
        self.rep = Repository(
                config["url"],
                config["db"],
                config["collection"])


        path_to_sensor_config = os.path.join(os.path.dirname(__file__), 'resources', 'sensorConf.json')
        with open(path_to_sensor_config, 'r', encoding='utf-8') as file:
            self.sensor_config = json.load(file)

        path_to_setpoints = os.path.join(os.path.dirname(__file__), 'resources', 'sensorSetpoints.json')
        with open(path_to_setpoints, 'r', encoding='utf-8') as file:
            self.setpoints = json.load(file)

    def save_or_get_signal(self, data):
        response = {}
        if data["mode"] == "Sensor":
            signal = Signal(
                name=data['name'],
                param=data['param'][0],
                time_stamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
            self.rep.save_signal_to_db(signal)
        else:
            signal = self.rep.get_last_signal_by_client_name(data["name"])
            response = {"param": signal.param}
        return json.dumps(response)

    def get_signals_view(self):
        data = self.rep.get_all_last_signals()
        result = []
        for signal in data:
            group = self.sensor_config[signal.name[7]][0]
            unit = self.sensor_config[signal.name[7]][1]
            status = "active" \
                if  datetime.now() - datetime.strptime(signal.time_stamp, "%d.%m.%Y %H:%M:%S") < timedelta(seconds=10) \
                else "inactive"
            if status == "active" and self.setpoints[signal.name] is not None:
                if signal.param <= self.setpoints[signal.name][0] or signal.param >= self.setpoints[signal.name][1]:
                    status = "out_of_range"

            result.append(
                {
                    "id": signal.name,
                    "group": group,
                    "value": signal.param,
                    "unit": unit,
                    "status": status
                }
            )
        return result

    def get_sinals_history_by_group_id(self, id):
        if id is None: return self.rep.get_all_signals()
        return self.rep.get_signals_by_group_id(id)