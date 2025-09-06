import random
import string


class PersonData:
    @staticmethod
    def generate_random_email():
        """Генерация уникального email"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@example.com"
    
    @staticmethod
    def generate_random_name():
        """Генерация случайного имени"""
        names = ["Иван", "Мария", "Петр", "Анна", "Сергей", "Ольга", "Алексей", "Елена"]
        return random.choice(names)
    
    @staticmethod
    def generate_random_password():
        """Генерация случайного пароля"""
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=10))
    
    @staticmethod
    def create_correct_user_data():
        """Создает корректные данные пользователя"""
        return {
            "email": PersonData.generate_random_email(),
            "password": PersonData.generate_random_password(),
            "name": PersonData.generate_random_name()
        }
    
    @staticmethod
    def create_incorrect_user_data_without_email():
        """Данные пользователя без email"""
        return {
            "password": PersonData.generate_random_password(),
            "name": PersonData.generate_random_name()
        }
    
    @staticmethod
    def create_incorrect_user_data_without_password():
        """Данные пользователя без пароля"""
        return {
            "email": PersonData.generate_random_email(),
            "name": PersonData.generate_random_name()
        }
    
    @staticmethod
    def create_incorrect_user_data_without_name():
        """Данные пользователя без имени"""
        return {
            "email": PersonData.generate_random_email(),
            "password": PersonData.generate_random_password()
        }
    
    @staticmethod
    def invalid_email_format():
        """Данные с невалидным email"""
        return {
            "email": "invalid-email",
            "password": PersonData.generate_random_password(),
            "name": PersonData.generate_random_name()
        }


class UpdateData:
    @staticmethod
    def get_update_test_cases():
        """Тестовые случаи для обновления данных пользователя"""
        return [
            {"name": "Новое Имя " + ''.join(random.choices(string.digits, k=3))},
            {"email": f"updated_{random.randint(1000, 9999)}@example.com"},
            {"password": "new_password_123!"}
        ]
    
    @staticmethod
    def get_complete_update_test_cases():
        """Полные тестовые случаи с заполнением всех полей"""
        return [
            {
                "name": "Обновленное Имя",
                "email": f"user_{random.randint(1000, 9999)}@example.com",
                "password": "updated_password_123!"
            }
        ]