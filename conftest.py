import pytest
import requests
from data.user_data import PersonData
from static_data.urls import URL, Endpoints
from static_data.ingredients_hash_data import Ingredients


@pytest.fixture
def create_user():
    """Фикстура для создания пользователя с последующим удалением"""
    payload = PersonData.create_correct_user_data()
    response = requests.post(URL.main_url + Endpoints.CREATE_USER, json=payload)
    
    yield payload, response
    
    # Cleanup - удаляем пользователя после теста
    if response.status_code == 200 and 'accessToken' in response.json():
        token = response.json()['accessToken']
        requests.delete(
            URL.main_url + Endpoints.DELETE_USER, 
            headers={"Authorization": token}
        )


@pytest.fixture
def user_with_order(create_user):
    """Фикстура для пользователя с заказом"""
    token = create_user[1].json().get('accessToken')
    if not token:
        pytest.skip("Не удалось получить токен пользователя")
    
    headers = {'Authorization': token}
    
    # Создаем заказ
    order_response = requests.post(
        URL.main_url + Endpoints.CREATE_ORDER,
        headers=headers, 
        json=Ingredients.correct_ingredients_hash_data
    )
    
    yield {
        "user_data": create_user[0],
        "token": token,
        "order_response": order_response,
        "headers": headers
    }