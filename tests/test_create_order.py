import allure
from api_client import OrderAPI
from static_data.status_codes import StatusCode
from static_data.response_text import TextResponse
from static_data.ingredients_hash_data import Ingredients


class TestCreateOrder:

    @allure.title('Order creation by authorized user')
    @allure.description('''
    1. Create order with auth;
    2. Verify success;
    ''')
    def test_create_order_with_authorized_user(self, create_user):
        token = create_user[1].json()['accessToken']
        response = OrderAPI.create_order(token, Ingredients.correct_ingredients_hash_data)
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True

    @allure.title('Order creation by unauthorized user')
    @allure.description('''
    1. Create order without auth;
    2. Verify success.
    ''')
    def test_create_order_by_unauthorized_user(self):
        response = OrderAPI.create_order(None, Ingredients.correct_ingredients_hash_data)
        assert response.status_code == StatusCode.OK
        assert response.json().get('success') is True

    @allure.title('Order creation with invalid hash')
    @allure.description('''
    1. Create order with invalid ingredients;
    2. Verify error;
    ''')
    def test_create_order_with_invalid_hash(self, create_user):
        token = create_user[1].json()['accessToken']
        response = OrderAPI.create_order(token, Ingredients.incorrect_ingredients_hash_data)
        assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR
        assert TextResponse.INTERNAL_SERVER_ERROR in response.text

    @allure.title('Order creation without ingredients')
    @allure.description('''
    1. Create order without ingredients;
    2. Verify error;
    ''')
    def test_create_order_without_ingredients(self, create_user):
        token = create_user[1].json()['accessToken']
        response = OrderAPI.create_order(token, Ingredients.empty_ingredients_data)
        assert response.status_code == StatusCode.BAD_REQUEST
        assert response.json().get('success') is False
