from data.test_data import TestConstants


class LoginTestData:
    """Тестовые данные для авторизации"""
    
    # Неправильный пароль (email будет заполнен динамически)
    WRONG_PASSWORD = {
        "password": TestConstants.STATIC_WRONG_PASSWORD
    }
    
    # Несуществующий email
    NONEXISTENT_EMAIL = {
        "email": TestConstants.STATIC_NONEXISTENT_EMAIL,
        "password": TestConstants.STATIC_ANY_PASSWORD
    }
    
    # Неполные данные
    MISSING_EMAIL = {
        "password": "password123"
    }
    
    MISSING_PASSWORD = {
        "email": "test@example.com"
    }
    
    EMPTY_DATA = {}
    
    # Невалидный формат email
    INVALID_EMAIL_FORMAT = {
        "email": "invalid-email-format",
        "password": "password123"
    }