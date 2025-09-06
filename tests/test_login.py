import pytest
import allure
import requests

from helper_methods.helpers import PersonData
from static_data.urls import URL, Endpoints
from static_data.status_codes import StatusCode
from static_data.response_text import TextResponse


class TestLoginUser:
    
    @allure.title('Successful login with existing user')
    @allure.description('''
    1. Login with correct credentials;
    2. Verify success;
    ''')
    def test_login_existing_user_success(self, create_user):
        """Логин существующего пользователя"""
        login_data = {
            "email": create_user[0]["email"],
            "password": create_user[0]["password"]
        }
        
        login_response = requests.post(
            URL.main_url + Endpoints.LOGIN, 
            json=login_data
        )
        
        assert login_response.status_code == StatusCode.OK
        assert login_response.json().get("success") is True
        assert "accessToken" in login_response.json()

    @allure.title('Login with wrong password')
    @allure.description('''
    1. Login with wrong password;
    2. Verify error;
    ''')
    def test_login_wrong_password(self, create_user):
        login_data = {
            "email": create_user[0]["email"],
            "password": "wrong_password_123"
        }
        
        login_response = requests.post(
            URL.main_url + Endpoints.LOGIN, 
            json=login_data
        )
        
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False

    # Остальные атомарные тесты не трогаем
    @allure.title('Login with non-existent email')
    def test_login_nonexistent_email(self):
        login_data = {
            "email": "nonexistent@example.com",
            "password": "any_password"
        }
        
        login_response = requests.post(
            URL.main_url + Endpoints.LOGIN, 
            json=login_data
        )
        
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False

    @allure.title('Login without required fields')
    @pytest.mark.parametrize('login_data', [
        {"password": "password123"},
        {"email": "test@example.com"}, 
        {}
    ])
    def test_login_missing_required_fields(self, login_data):
        login_response = requests.post(
            URL.main_url + Endpoints.LOGIN, 
            json=login_data
        )
        
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False