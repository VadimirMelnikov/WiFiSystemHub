import pytest
from src import Repository

@pytest.fixture
def mock_mongo_collection(mocker):
    """Фикстура для мокирования коллекции MongoDB."""
    mock_collection = mocker.MagicMock()
    mocker.patch.object(Repository, "collection", new_callable=mocker.PropertyMock(return_value=mock_collection))
    return mock_collection

def test_save_signal(mock_mongo_collection):
    """Проверяем, что сигнал сохраняется в MongoDB."""
    repo = Repository("mongodb://localhost:27017", "test_db", "signals")
    test_signal = {"name": "test_signal", "value": 123}

    # Мокируем insert_one
    mock_mongo_collection.insert_one.return_value = InsertOneResult(inserted_id="abc123", acknowledged=True)

    repo.save_signal(test_signal)

    # Проверяем, что insert_one был вызван с правильными аргументами
    mock_mongo_collection.insert_one.assert_called_once_with(test_signal)

