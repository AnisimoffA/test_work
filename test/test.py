import pytest
from fastapi.testclient import TestClient
from main import app
import redis
from config import REDIS_HOST, REDIS_PORT


client = TestClient(app)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


# фикстура для чистки Redis перед каждым тестом
@pytest.fixture(scope="function")
def clear_redis():
    redis_client.flushdb()

# тест для проверки записи новых данных
def test_write_data(clear_redis):
    response = client.post("/write_data", json={"phone": "12345", "address": "123 Main St"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully added"}

    address = redis_client.get("12345")
    assert address.decode("utf-8") == "123 Main St"


# тест для проверки обновления данных
def test_update_data(clear_redis):
    # Добавляем данные, которые будем менять
    redis_client.set("12345", "123 Main St")

    response = client.put("/write_data", json={"phone": "12345", "address": "456 Elm St"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully updated"}

    # Проверяем, что данные обновлены в Redis
    address = redis_client.get("12345")
    assert address.decode("utf-8") == "456 Elm St"


# тест для проверки пограничного случая, когда нет нужных данных для обновления
def test_update_data_not_found(clear_redis):
    response = client.put("/write_data", json={"phone": "99999", "address": "No Address"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found"}


# тест для проверки получения данных
def test_check_data(clear_redis):
    # Сначала нужно записать данные
    redis_client.set("12345", "123 Main St")

    response = client.get("/check_data", params={"phone": "12345"})
    assert response.status_code == 200
    assert response.json() == {"phone": "12345", "address": "123 Main St"}


# тест для проверки пограничного случая, когда нет нужных данных для получения
def test_check_data_not_found(clear_redis):
    response = client.get("/check_data", params={"phone": "99999"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found"}

