from datetime import datetime

from pymongo import MongoClient
from Signal import  Signal

class Repository:
    def __init__(self, path, database, collection):
        self.path = path
        self.db = database
        self.col = collection

    def save_signal_to_db(self, signal: Signal):
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            collection.insert_one({'name': signal.name, 'param': signal.param, 'time_stamp': datetime.now().strftime("%d.%m.%Y %H:%M:%S")})

    def get_data_by_client_name(self, signal:Signal):
        data = []
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            for json in collection.find({'name': signal.name}):
                json.pop('_id')
                data.append(json)
        return data

    def get_all_signals(self):
        data = []
        with MongoClient(self.path) as client:
            db = client[self.db]
            collection = db[self.col]
            for json in collection.find():
                json.pop('_id')
                data.append(json)
        return data

