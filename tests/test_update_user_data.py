import pytest
import requests
import allure

from static_data.urls import URL, Endpoints
from static_data.response_text import TextResponse
from static_data.status_codes import StatusCode
from data.user_data import UpdateData
from data.test_data import TestConstants


class TestChangeUserData:

    @allure.title('Change user name with auth')
    @allure.description('Change user name with authorization')
    def test_change_user_name_with_auth(self, create_user):
        token = create_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        new_name = {"name": TestConstants.UPDATED_NAME}
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=new_name
        )
        
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True
        assert response.json()['user']['name'] == TestConstants.UPDATED_NAME

    @allure.title('Change user email with auth - successful update')
    @allure.description('Change user email with authorization - success case')
    def test_change_user_email_with_auth_success(self, create_user_with_unique_email):
        token = create_user_with_unique_email[1].json()['accessToken']
        headers = {'Authorization': token}
        
        new_email = {"email": f"updated_{create_user_with_unique_email[0]['email']}"}
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=new_email
        )
        
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True

    @allure.title('Change user email with auth - email conflict')
    @allure.description('Change user email with authorization - email already exists')
    def test_change_user_email_with_auth_conflict(self, create_two_users):
        first_user, second_user = create_two_users
        token = first_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        # Пытаемся изменить email первого пользователя на email второго
        conflict_email = {"email": second_user[0]['email']}
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=conflict_email
        )
        
        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json().get('success') is False

    @allure.title('Change user password with auth')
    @allure.description('Change user password with authorization')
    def test_change_user_password_with_auth(self, create_user):
        token = create_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        new_password = {"password": TestConstants.UPDATED_PASSWORD}
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=new_password
        )
        
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True

    @allure.title('Change complete user data with auth - successful update')
    @allure.description('Change all user fields with authorization - success case')
    def test_change_complete_user_data_with_auth_success(self, create_user_with_unique_email):
        token = create_user_with_unique_email[1].json()['accessToken']
        headers = {'Authorization': token}
        
        update_data = UpdateData.get_complete_update_test_cases()[0]
        response = requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA, 
            headers=headers, 
            json=update_data
        )
        
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True

    @allure.title('Change data without auth test')
    @allure.description('Attempt to change user data without authorization')
    def test_change_unauthorized_user_data(self):
        update_data = {"name": "Unauthorized Change Attempt"}
        response = requests.patch(URL.main_url + Endpoints.CHANGE_DATA, json=update_data)
        
        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json().get('message') == TextResponse.UNAUTHORIZED_RESPONSE