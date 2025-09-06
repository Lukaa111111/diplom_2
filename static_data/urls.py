class URL:
    main_url = 'https://stellarburgers.nomoreparties.site'  # Базовый URL сервиса Stellar Burgers


class Endpoints:
    CREATE_USER = '/api/auth/register'  # Создание пользователя
    DELETE_USER = '/api/auth/user'  # Удаление пользователя
    LOGIN = '/api/auth/login'  # Логин пользователя
    CREATE_ORDER = '/api/orders'  # Создание заказа
    GET_ORDERS = '/api/orders'  # Получение заказа
    CHANGE_DATA = '/api/auth/user'  # Изменение данных пользователя