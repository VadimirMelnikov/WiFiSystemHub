from pymongo import MongoClient
from src.dto.Signal import Signal

class SignalRepository:
    def __init__(self, path, database, collection):
        self.path = path
        self.db = database
        self.col = collection

    def save_signal(self, signal: Signal):
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            collection.insert_one({'name': signal.name, 'group': signal.group, 'value': signal.value, 'time_stamp': signal.time_stamp})

    def get_last_signal_by_name(self, sensor_name):
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            json = collection.find_one({'name': sensor_name}, sort=[('time_stamp', -1)])
            if not json:
                return None
            json.pop('_id')
        return Signal(
                        name=json["name"],
                        group=json["group"],
                        value=json["value"],
                        time_stamp=json["time_stamp"])

    def get_signal_by_name(self, sensor_name):
        data = []
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            for json in collection.find({'name': sensor_name}):
                json.pop('_id')
                data.append(
                    Signal(
                        name=json["name"],
                        group=json["group"],
                        value=json["value"],
                        time_stamp=json["time_stamp"]
                    )
                )
        return data

    def get_all_last_signals(self):
        data = []
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            pipeline = [
                {
                    "$sort": {"time_stamp": -1}  # Сначала сортируем по времени (новые вверху)
                },
                {
                    "$group": {
                        "_id": "$name",  # Группируем по полю 'name'
                        "latest_doc": {"$first": "$$ROOT"},  # Берём первый документ (он самый новый)
                    }
                },
                {
                    "$replaceRoot": {"newRoot": "$latest_doc"}  # Заменяем корень документа на latest_doc
                }
            ]

            latest_signals = list(collection.aggregate(pipeline))
            for json in latest_signals:
                json.pop('_id')
                data.append(
                    Signal(
                        name=json["name"],
                        group=json["group"],
                        value=json["value"],
                        time_stamp=json["time_stamp"]
                    )
                )
            return data


    def get_all_signals(self):
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            return [{k: v for k, v in doc.items() if k != "_id"} for doc in collection.find()]

    def get_signals_by_group(self, group):
        if group is None: return None
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            print(group)
            cursor = collection.find({"group": group})
            result = [{k: v for k, v in doc.items() if k != "_id" and k != "group"} for doc in cursor]
            return result
