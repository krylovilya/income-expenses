from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from apps.transactions.tests.factories import (CategoryFactory,
                                               TransactionFactory, UserFactory,
                                               WidgetFactory)


class BaseAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.fake_user = UserFactory()
        self.token = get_token(self.user)

    def set_token(self, user=None):
        """Добавить токен пользователя в запрос"""
        if user:
            token = get_token(user)
            self.client.credentials(HTTP_AUTHORIZATION=' '.join(('Bearer', token)))
        else:
            self.client.credentials(HTTP_AUTHORIZATION='')


def get_token(user):
    """Получить токен"""
    return AccessToken.for_user(user).__str__()


def create_category(owner):
    """Создать объект 'Категория' и вернуть его id"""
    category = CategoryFactory(owner=owner)
    return category.id


def create_transaction(owner):
    """Создать объект 'Транзакция' и вернуть id категории и id транзакции"""
    transaction = TransactionFactory(owner=owner)
    return transaction.category.id, transaction.id


def create_widget(owner):
    """Создать объект 'Виджет' и вернуть id категории и id виджета"""
    widget = WidgetFactory(owner=owner)
    return widget.category.id, widget.id
