from faker import Faker


class PersonData:

    # Создаем корректные данные пользователя
    @staticmethod
    def create_correct_user_data():
        faker = Faker('ru_RU')
        data = {
            'email': faker.email(),
            'password': faker.password(),
            'name': faker.first_name()
        }
        return data

    # Создаем данные пользователя без email
    @staticmethod
    def create_incorrect_user_data_without_email():
        faker = Faker('ru_RU')
        data = {
            'password': faker.password(),
            'name': faker.first_name()
        }
        return data

    # Создаем данные пользователя без имени
    @staticmethod
    def create_incorrect_user_data_without_name():
        faker = Faker('ru_RU')
        data = {
            'email': faker.email(),
            'password': faker.password()
        }
        return data

    # Создаем данные пользователя без пароля
    @staticmethod
    def create_incorrect_user_data_without_password():
        faker = Faker('ru_RU')
        data = {
            'email': faker.email(),
            'name': faker.first_name()
        }
        return data