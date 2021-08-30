import json

from rest_framework import status

from apps.transactions.tests.init_tests import (BaseAPITests, create_category,
                                                create_widget)


class WidgetAPITests(BaseAPITests):
    def setUp(self):
        super().setUp()
        self.widget_init_data = {
            'owner': self.user.id,
            'category': None,
            'amount_limit': '200',
            'period': 1,
            'criterion': '>',
            'hex_color': '#ffffff',
        }

    def test_delete_widget(self):
        """Пользователь может удалить свой виджет"""
        self.set_token(self.user)
        _, widget_id = create_widget(self.user)
        delete_response = self.client.delete(f'/api/transactions/widget/{widget_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_widget_fake(self):
        """Пользователь не может удалить чужой виджет"""
        _, widget_id = create_widget(self.user)
        self.set_token(self.fake_user)
        delete_response = self.client.delete(f'/api/transactions/widget/{widget_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_widget(self):
        """Пользователь может получить свои виджеты"""
        self.set_token(self.user)
        create_widget(self.user)
        get_response = self.client.get('/api/transactions/widget/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(get_response.content)['count'], 1)

    def test_get_widget_fake(self):
        """Пользователь не может получить чужие виджеты"""
        create_widget(self.user)
        self.set_token(self.fake_user)
        get_response = self.client.get('/api/transactions/widget/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(get_response.content)['count'], 0)

    def test_post_widget(self):
        """Пользователь может создать виджет"""
        self.set_token(self.user)
        category_id = create_category(self.user)
        widget_init_data = self.widget_init_data | {'category': category_id}
        post_response = self.client.post('/api/transactions/widget/',
                                         widget_init_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    def test_post_widget_fake(self):
        """Анонимный пользователь не может создать виджет"""
        category_id = create_category(self.user)
        widget_init_data = self.widget_init_data | {'category': category_id}
        self.set_token()
        post_response = self.client.post('/api/transactions/widget/',
                                         widget_init_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)
