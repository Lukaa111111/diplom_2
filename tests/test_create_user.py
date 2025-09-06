import pytest
import allure
import requests

from data.user_data import PersonData
from static_data.urls import URL, Endpoints
from static_data.status_codes import StatusCode
from static_data.response_text import TextResponse


class TestCreateUser:
    
    @allure.title('Успешное создание уникального пользователя')
    @allure.description('''
    1. Отправка запроса на создание пользователя;
    2. Проверка успешного ответа;
    3. Удаление пользователя.
    ''')
    def test_create_unique_user_success(self, create_user):
        response = create_user
        assert response[1].status_code == StatusCode.OK
        assert response[1].json().get("success") is True
        assert "accessToken" in response[1].json()
        assert "refreshToken" in response[1].json()
        assert "user" in response[1].json()

    @allure.title('Создание уже зарегистрированного пользователя')
    @allure.description('''
    1. Попытка создания пользователя с существующими данными;
    2. Проверка ошибки;
    ''')
    def test_create_existing_user_failure(self):
        """Тест двойной регистрации (атомарный - создает пользователя сам)"""
        # 1. Создаем первого пользователя
        payload = PersonData.create_correct_user_data()
        first_response = requests.post(
            URL.main_url + Endpoints.CREATE_USER, 
            json=payload
        )
        
        # 2. Пытаемся создать второго с теми же данными (основная проверка)
        second_response = requests.post(
            URL.main_url + Endpoints.CREATE_USER, 
            json=payload
        )
        
        assert second_response.status_code == StatusCode.FORBIDDEN
        assert second_response.json().get('success') is False
        assert second_response.json().get('message') == TextResponse.DOUBLE_USER_CREATED
        
        # 3. Удаляем первого пользователя (cleanup)
        if first_response.status_code == StatusCode.OK:
            token = first_response.json()['accessToken']
            requests.delete(
                URL.main_url + Endpoints.DELETE_USER, 
                headers={"Authorization": token}
            )

    @allure.title('Создание пользователя без обязательных полей')
    @allure.description('''
    1. Попытка создания пользователя без обязательных полей;
    2. Проверка ошибки валидации.
    ''')
    @pytest.mark.parametrize('payload', [
        PersonData.create_incorrect_user_data_without_email(),
        PersonData.create_incorrect_user_data_without_password(),
        PersonData.create_incorrect_user_data_without_name()
    ])
    def test_create_user_missing_required_fields(self, payload):
        response = requests.post(
            URL.main_url + Endpoints.CREATE_USER, 
            json=payload
        )
        
        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json().get("success") is False

    @allure.title('Создание пользователя с некорректным email')
    @allure.description('Проверка валидации email при регистрации')
    def test_create_user_invalid_email_format(self):
        payload = PersonData.invalid_email_format()
        
        response = requests.post(
            URL.main_url + Endpoints.CREATE_USER, 
            json=payload
        )
        
        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json().get("success") is False