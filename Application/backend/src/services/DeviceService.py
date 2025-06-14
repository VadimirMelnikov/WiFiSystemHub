import os
import json
from datetime import datetime, timedelta
import requests
from dto.Signal import Signal
from src.repositories.SignalRepository import SignalRepository

class DeviceService:
    def __init__(self, config):
        self.rep = SignalRepository(
                config["url"],
                config["db"],
                config["collection"])

        path_to_sensor_config = os.path.join(os.path.dirname(__file__), '..', 'resources', 'groupUnits.json')
        with open(path_to_sensor_config, 'r', encoding='utf-8') as file:
            self.sensor_config = json.load(file)

        path_to_setpoints = os.path.join(os.path.dirname(__file__), '..', 'resources', 'setpoints.json')
        with open(path_to_setpoints, 'r', encoding='utf-8') as file:
            self.setpoints = json.load(file)

    def get_status(self, signal: Signal):
        status =  "active" \
            if datetime.now() - datetime.strptime(signal.time_stamp, "%d.%m.%Y %H:%M:%S") < timedelta(seconds=10) \
            else "inactive"
        if status == "active" and self.setpoints[signal.name] is not None:
            if signal.value <= self.setpoints[signal.name][0] or signal.value >= self.setpoints[signal.name][1]:
                status = "out_of_range"
        return status

    def get_sensors(self):
        signals = self.rep.get_all_last_signals()
        result = list()
        for signal in signals:
            result.append({
                "name": signal.name,
                "group": signal.group,
                "value": signal.value,
                "unit": self.sensor_config[signal.group],
                "status": self.get_status(signal)
            })
        return result

    def get_actuators(self):
        result = list()
        response = requests.get(
            "http://localhost:18083/api/v5/subscriptions",
            auth=("8335fa56d487562d", "ngF2YTKW3rdoN9C4uqbxpl80DZf9A4FcP9AOoVyNQWibFK"),
            timeout=5
        )
        for node in response.json()["data"]:
            if node["clientid"] != "python-listener":
                result.append({
                    "name": node["clientid"],
                    "sensor": node["topic"].split("/")[-1],
                })
        return result

    def get_history_by_group(self, group):
        return self.rep.get_signals_by_group(group)