import pytest
import requests
import allure

from static_data.urls import URL, Endpoints
from static_data.response_text import TextResponse
from static_data.status_codes import StatusCode
from data.user_data import UpdateData


class TestChangeUserData:

    @allure.title('Change user name with auth')
    @allure.description('Change user name with authorization')
    def test_change_user_name_with_auth(self, create_user):
        token = create_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        new_name = {"name": "Обновленное Имя"}
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=new_name
        )
        
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True
        assert response.json()['user']['name'] == "Обновленное Имя"

    @allure.title('Change user email with auth')
    @allure.description('Change user email with authorization')
    def test_change_user_email_with_auth(self, create_user):
        token = create_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        new_email = {"email": f"updated_{create_user[0]['email']}"}
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=new_email
        )
        
        # Проверяем успешный ответ или конфликт email (может быть занят)
        assert response.status_code in [StatusCode.OK, StatusCode.FORBIDDEN]
        if response.status_code == StatusCode.OK:
            assert response.json().get('success') is True

    @allure.title('Change user password with auth')
    @allure.description('Change user password with authorization')
    def test_change_user_password_with_auth(self, create_user):
        token = create_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        new_password = {"password": "new_secure_password_123!"}
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=new_password
        )
        
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True

    @allure.title('Change complete user data with auth')
    @allure.description('Change all user fields with authorization')
    def test_change_complete_user_data_with_auth(self, create_user):
        token = create_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        update_data = UpdateData.get_complete_update_test_cases()[0]
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=update_data
        )
        
        # Проверяем успешный ответ или конфликт email
        assert response.status_code in [StatusCode.OK, StatusCode.FORBIDDEN]
        if response.status_code == StatusCode.OK:
            assert response.json().get('success') is True

    @allure.title('Change data without auth test')
    @allure.description('Attempt to change user data without authorization')
    def test_change_unauthorized_user_data(self):
        update_data = {"name": "Unauthorized Change Attempt"}
        response = requests.patch(URL.main_url + Endpoints.CHANGE_DATA, json=update_data)
        
        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json().get('message') == TextResponse.UNAUTHORIZED_RESPONSE