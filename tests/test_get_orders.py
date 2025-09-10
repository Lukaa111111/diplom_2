import requests
import allure

from static_data.urls import URL, Endpoints
from static_data.status_codes import StatusCode
from static_data.response_text import TextResponse


class TestGetOrder:
    
    @allure.title('Get empty orders by authorized user')
    @allure.description('''
    1. Get user orders with auth;
    2. Verify empty orders list;
    ''')
    def test_get_empty_orders_by_authorized_user(self, create_user):
        """Получение пустого списка заказов (атомарный тест)"""
        token = create_user[1].json()['accessToken']
        headers = {'Authorization': token}
        
        response_get_order = requests.get(
            URL.main_url + Endpoints.GET_ORDERS, 
            headers=headers
        )
        
        assert response_get_order.status_code == StatusCode.OK
        assert "orders" in response_get_order.json()
        assert isinstance(response_get_order.json()["orders"], list)
        # Проверяем, что список заказов пустой (атомарная проверка)
        assert len(response_get_order.json()["orders"]) == 0

    @allure.title('Get orders by authorized user with orders')
    @allure.description('''
    1. Create user and order;
    2. Get user orders with auth;
    3. Verify orders list contains the order;
    ''')
    def test_get_orders_by_authorized_user_with_orders(self, user_with_order):
        """Получение списка заказов пользователя с заказами"""
        response_get_orders = requests.get(
            URL.main_url + Endpoints.GET_ORDERS, 
            headers=user_with_order["headers"]
        )
        
        assert response_get_orders.status_code == StatusCode.OK
        assert response_get_orders.json().get("success") is True
        assert "orders" in response_get_orders.json()
        assert isinstance(response_get_orders.json()["orders"], list)
        # Проверяем, что список заказов не пустой
        assert len(response_get_orders.json()["orders"]) > 0

    @allure.title('Get order by unauthorized user')
    @allure.description('''
    1. Get user orders without auth;
    2. Verify error response.
    ''')
    def test_get_orders_by_unauthorized_user(self):
        response_get_orders = requests.get(URL.main_url + Endpoints.GET_ORDERS)
        assert response_get_orders.status_code == StatusCode.UNAUTHORIZED
        assert TextResponse.UNAUTHORIZED_RESPONSE in response_get_orders.text