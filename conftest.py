import pytest
from data.user_data import PersonData
from api_client import UserAPI, OrderAPI
from static_data.ingredients_hash_data import Ingredients
from static_data.status_codes import StatusCode


@pytest.fixture
def create_user():
    """Фикстура для создания пользователя с последующим удалением"""
    payload = PersonData.create_correct_user_data()
    response = UserAPI.create_user(payload)
    
    yield payload, response
    
    # Cleanup - удаляем пользователя после теста
    if response.status_code == StatusCode.OK and 'accessToken' in response.json():
        token = response.json()['accessToken']
        UserAPI.delete_user(token)


@pytest.fixture
def create_unique_user_for_double_registration():
    """Фикстура для теста двойной регистрации"""
    payload = PersonData.create_correct_user_data()
    first_response = UserAPI.create_user(payload)
    
    yield payload, first_response
    
    
    if first_response.status_code == StatusCode.OK and 'accessToken' in first_response.json():
        token = first_response.json()['accessToken']
        UserAPI.delete_user(token)


@pytest.fixture
def create_user_with_unique_email():
    """Фикстура для пользователя с гарантированно уникальным email"""
    payload = PersonData.create_correct_user_data()
    response = UserAPI.create_user(payload)
    
    yield payload, response
    
    
    if response.status_code == StatusCode.OK and 'accessToken' in response.json():
        token = response.json()['accessToken']
        UserAPI.delete_user(token)


@pytest.fixture
def create_two_users():
    """Фикстура для создания двух пользователей"""
    # Первый пользователь
    payload1 = PersonData.create_correct_user_data()
    response1 = UserAPI.create_user(payload1)
    
    # Второй пользователь
    payload2 = PersonData.create_correct_user_data()
    response2 = UserAPI.create_user(payload2)
    
    yield (payload1, response1), (payload2, response2)
    
    
    for response in [response1, response2]:
        if response.status_code == StatusCode.OK and 'accessToken' in response.json():
            token = response.json()['accessToken']
            UserAPI.delete_user(token)


@pytest.fixture
def user_with_order(create_user):
    """Фикстура для пользователя с заказом"""
    # Гарантируем, что пользователь создан успешно
    assert create_user[1].status_code == StatusCode.OK
    assert 'accessToken' in create_user[1].json()
    
    token = create_user[1].json()['accessToken']
    
    # Создаем заказ
    order_response = OrderAPI.create_order(token, Ingredients.correct_ingredients_hash_data)
    
    yield {
        "user_data": create_user[0],
        "token": token,
        "order_response": order_response
    }

