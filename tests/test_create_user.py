import pytest
import allure
from api_client import UserAPI
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
    def test_create_existing_user_failure(self, create_unique_user_for_double_registration):
        """Тест двойной регистрации"""
        user_data, first_response = create_unique_user_for_double_registration
        
        # Пытаемся создать второго с теми же данными
        second_response = UserAPI.create_user(user_data)
        
        assert second_response.status_code == StatusCode.FORBIDDEN
        assert second_response.json().get('success') is False
        assert second_response.json().get('message') == TextResponse.DOUBLE_USER_CREATED

    @allure.title('Создание пользователя без email')
    def test_create_user_without_email(self):
        payload = PersonData.create_incorrect_user_data_without_email()
        response = UserAPI.create_user(payload)
        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json().get("success") is False

    @allure.title('Создание пользователя без пароля')
    def test_create_user_without_password(self):
        payload = PersonData.create_incorrect_user_data_without_password()
        response = UserAPI.create_user(payload)
        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json().get("success") is False

    @allure.title('Создание пользователя без имени')
    def test_create_user_without_name(self):
        payload = PersonData.create_incorrect_user_data_without_name()
        response = UserAPI.create_user(payload)
        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json().get("success") is False

    @allure.title('Создание пользователя с некорректным email')
    @allure.description('Проверка валидации email при регистрации')
    def test_create_user_invalid_email_format(self):
        payload = PersonData.invalid_email_format()
        response = UserAPI.create_user(payload)
        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json().get("success") is False