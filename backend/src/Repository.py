from pymongo import MongoClient
from src.Signal import Signal

class Repository:
    def __init__(self, path, database, collection):
        self.path = path
        self.db = database
        self.col = collection

    def save_signal_to_db(self, signal: Signal):
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            collection.insert_one({'name': signal.name, 'param': signal.param, 'time_stamp': signal.time_stamp})

    def get_last_signal_by_client_name(self, client_name):
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            json = collection.find_one({'name': client_name}, sort=[('time_stamp', -1)])
            if not json:
                return None
            json.pop('_id')
        return Signal(
                        name=json["name"],
                        param=json["param"],
                        time_stamp=json["time_stamp"])

    def get_signal_by_client_name(self, client_name):
        data = []
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            for json in collection.find({'name': client_name}):
                json.pop('_id')
                data.append(
                    Signal(
                        name=json["name"],
                        param=json["param"],
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
                        param=json["param"],
                        time_stamp=json["time_stamp"]
                    )
                )
            return data


    def get_all_signals(self):
        data = []
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            for json in collection.find():
                json.pop('_id')
                data.append(
                    Signal(
                        name=json["name"],
                        param=json["param"],
                        time_stamp=json["time_stamp"]
                    )
                )
        return data

