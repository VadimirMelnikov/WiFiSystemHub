from datetime import datetime
import pytest
from pymongo import MongoClient

from src.Repository import Repository
from src.Signal import Signal


# данные для подключения
path = "mongodb://localhost:27017/"
db = "test_db"
collection = "test_col"

# настройка и создание временной бд и коллекции
@pytest.fixture(scope="function")
def temp_repo():
    rep = Repository(
        path,
        db,
        collection)
    yield rep
    with MongoClient(path) as client:
        client.drop_database(db)

# данные для тестов
signal11 = Signal(
    "Client_1_1",
    234.1,
    datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

signal12 = Signal(
    "Client_1_1",
    200.0,
    '13.05.2025 22:04:00'
)

signal21 = Signal(
    "Client_1_2",
    60.0,
    datetime.now().strftime("%d.%m.%Y %H:%M:%S")
)

signal22 = Signal(
    "Client_1_2",
    67.0,
    '13.05.2025 22:10:00'
)

signal31 = Signal(
    "Client_1_3",
    15.3,
    datetime.now().strftime("%d.%m.%Y %H:%M:%S")
)

signal32 = Signal(
    "Client_1_3",
    27.3,
    '13.05.2025 22:10:00'
)

#тесты
def test_save_and_get_last_signal(temp_repo):
    rep = temp_repo
    rep.save_signal_to_db(signal11)
    result = rep.get_last_signal_by_client_name(signal11.name)
    print()
    print(result)
    assert signal11 == result
    assert rep.get_last_signal_by_client_name("dummy") is None

def test_get_signal_by_client_name(temp_repo):
    rep = temp_repo
    rep.save_signal_to_db(signal11)
    rep.save_signal_to_db(signal12)
    assert [signal11, signal12] == rep.get_signal_by_client_name(signal11.name)
    assert not rep.get_signal_by_client_name("dummy")

def test_get_all_signals(temp_repo):
    rep = temp_repo
    rep.save_signal_to_db(signal11)
    rep.save_signal_to_db(signal12)
    rep.save_signal_to_db(signal21)
    assert {signal11, signal12, signal21} == set(rep.get_all_signals())


def test_get_all_last_signals(temp_repo):
    rep = temp_repo
    rep.save_signal_to_db(signal11)
    rep.save_signal_to_db(signal12)
    rep.save_signal_to_db(signal21)
    rep.save_signal_to_db(signal22)
    rep.save_signal_to_db(signal31)
    rep.save_signal_to_db(signal32)
    result = rep.get_all_last_signals()
    assert {signal12, signal22, signal32} == set(rep.get_all_last_signals())