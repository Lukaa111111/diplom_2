import pytest
import requests
from helper_methods.helpers import PersonData
from static_data.urls import URL, Endpoints


@pytest.fixture
def create_user():  # Создание пользователя
    payload = PersonData.create_correct_user_data()
    response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
    yield payload, response
    token = response.json()['accessToken']
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})
import pytest
import requests
from helper_methods.helpers import PersonData
from static_data.urls import URL, Endpoints
from static_data.ingredients_hash_data import Ingredients


@pytest.fixture
def create_user():  # Создание пользователя
    payload = PersonData.create_correct_user_data()
    response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
    yield payload, response
    token = response.json()['accessToken']
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})


@pytest.fixture
def user_with_order(create_user):
    """Фикстура для пользователя с заказом (для отдельных тестов)"""
    token = create_user[1].json()['accessToken']
    headers = {'Authorization': token}
    
    # Создаем заказ
    order_response = requests.post(
        URL.main_url + Endpoints.CREATE_ORDER,
        headers=headers, 
        data=Ingredients.correct_ingredients_hash_data
    )
    
    yield {
        "headers": headers,
        "order_response": order_response
    }