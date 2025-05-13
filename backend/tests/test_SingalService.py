import json

import pytest
from pymongo import MongoClient

from src.SignalService import SignalService
from src.Repository import Repository
from src.Signal import Signal

# данные для подключения
config = {
    "url" : "mongodb://localhost:27017/",
    "db" : "test_db",
    "collection" : "test_col",
    "path to config" : r"D:\Proggers\Python\WiFiSystemHub\backend\src\resources\sensorConf.json"
}


# настройка и создание временной бд и коллекции
@pytest.fixture(scope="function")
def temp_signal_service():
    yield SignalService(config)
    with MongoClient(config["url"]) as client:
        client.drop_database(config["db"])

# данные для тестов
responce11 = {
    "name": "Client_1_1",
    "mode": "Sensor",
    "param": 345.0
}

responce12 = {
    "name": "Client_1_1",
    "mode": "Actuator",
    "param": 0.0
}

responce21 = {
    "name": "Client_2_1",
    "mode": "Sensor",
    "param": 12.1
}

responce31 = {
    "name": "Client_3_1",
    "mode": "Sensor",
    "param": 62.7
}

view = [
    {
        "id": "Client_1_1",
        "group": "Влажность",
        "value": 345.0,
        "unit": "%",
        "status": "🟢"
    },
    {
        "id": "Client_2_1",
        "group": "Уровень",
        "value": 12.1,
        "unit": "мм",
        "status": "🟢"
    },
    {
        "id": "Client_3_1",
        "group": "Давление",
        "value": 62.7,
        "unit": "кПа",
        "status": "🟢"
    }
]

def test_save_or_get_singal(temp_signal_service):
    assert  "{}" == temp_signal_service.save_or_get_signal(responce11)
    assert "{\"param\": 345.0}" == temp_signal_service.save_or_get_signal(responce12)

def test_get_signals_view(temp_signal_service):
    temp_signal_service.save_or_get_signal(responce11)
    temp_signal_service.save_or_get_signal(responce21)
    temp_signal_service.save_or_get_signal(responce31)
    result = temp_signal_service.get_signals_view()
    assert len(view) == len(result)

    view_set = {json.dumps(item, sort_keys=True) for item in view}
    result_set = {json.dumps(item, sort_keys=True) for item in result}

    assert view_set == result_set



