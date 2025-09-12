import requests
from static_data.urls import URL, Endpoints


class UserAPI:
    """Клиент для работы с API пользователей"""
    
    @staticmethod
    def create_user(user_data):
        return requests.post(URL.main_url + Endpoints.CREATE_USER, json=user_data)
    
    @staticmethod
    def delete_user(token):
        return requests.delete(
            URL.main_url + Endpoints.DELETE_USER, 
            headers={"Authorization": token}
        )
    
    @staticmethod
    def login(login_data):
        return requests.post(URL.main_url + Endpoints.LOGIN, json=login_data)
    
    @staticmethod
    def update_user(token, update_data):
        return requests.patch(
            URL.main_url + Endpoints.CHANGE_DATA,
            headers={"Authorization": token},
            json=update_data
        )


class OrderAPI:
    """Клиент для работы с API заказов"""
    
    @staticmethod
    def create_order(token, ingredients):
        headers = {"Authorization": token} if token else {}
        return requests.post(
            URL.main_url + Endpoints.CREATE_ORDER,
            headers=headers,
            json=ingredients
        )
    
    @staticmethod
    def get_orders(token):
        headers = {"Authorization": token} if token else {}
        return requests.get(
            URL.main_url + Endpoints.GET_ORDERS,
            headers=headers
        )