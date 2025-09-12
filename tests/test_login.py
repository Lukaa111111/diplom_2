import pytest
import allure
from api_client import UserAPI
from data.login_data import LoginTestData
from static_data.urls import URL, Endpoints
from static_data.status_codes import StatusCode


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
        
        login_response = UserAPI.login(login_data)
        
        assert login_response.status_code == StatusCode.OK
        assert login_response.json().get("success") is True
        assert "accessToken" in login_response.json()

    @allure.title('Login with wrong password')
    @allure.description('''
    1. Login with wrong password;
    2. Verify error;
    ''')
    def test_login_wrong_password(self, create_user):
        login_data = LoginTestData.WRONG_PASSWORD.copy()
        login_data["email"] = create_user[0]["email"]
        
        login_response = UserAPI.login(login_data)
        
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False

    @allure.title('Login with non-existent email')
    def test_login_nonexistent_email(self):
        login_response = UserAPI.login(LoginTestData.NONEXISTENT_EMAIL)
        
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False

    @allure.title('Login without email')
    def test_login_missing_email(self):
        login_response = UserAPI.login(LoginTestData.MISSING_EMAIL)
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False

    @allure.title('Login without password')
    def test_login_missing_password(self):
        login_response = UserAPI.login(LoginTestData.MISSING_PASSWORD)
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False

    @allure.title('Login with empty data')
    def test_login_empty_data(self):
        login_response = UserAPI.login(LoginTestData.EMPTY_DATA)
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False

    @allure.title('Login with invalid email format')
    def test_login_invalid_email_format(self):
        login_response = UserAPI.login(LoginTestData.INVALID_EMAIL_FORMAT)
        assert login_response.status_code == StatusCode.UNAUTHORIZED
        assert login_response.json().get("success") is False
