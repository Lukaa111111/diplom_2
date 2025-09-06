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

    @allure.title('Get order by unauthorized user')
    @allure.description('''
    1. Get user orders without auth;
    2. Verify error response.
    ''')
    def test_get_orders_by_unauthorized_user(self):
        response_get_orders = requests.get(URL.main_url + Endpoints.GET_ORDERS)
        assert response_get_orders.status_code == StatusCode.UNAUTHORIZED
        assert TextResponse.UNAUTHORIZED_RESPONSE in response_get_orders.text