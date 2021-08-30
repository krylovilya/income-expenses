import json

from rest_framework import status

from apps.transactions.tests.init_tests import BaseAPITests, create_category


class CategoryAPITests(BaseAPITests):
    def setUp(self):
        super().setUp()
        self.category_init_data = {
            'title': 'test_category',
            'type': 'IN',
            'owner': self.user.id,
        }

    def test_delete_category(self):
        """Пользователь может удалить свою категорию"""
        self.set_token(self.user)
        category_id = create_category(self.user)
        delete_response = self.client.delete(f'/api/transactions/category/{category_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_fake(self):
        """Пользователь не может удалить чужую категорию"""
        self.set_token(self.user)
        category_id = create_category(self.user)
        self.set_token(self.fake_user)
        delete_response = self.client.delete(f'/api/transactions/category/{category_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_category(self):
        """Пользователь может получить свои категории"""
        self.set_token(self.user)
        create_category(self.user)
        get_response = self.client.get('/api/transactions/category/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(get_response.content)['count'], 1)

    def test_get_category_fake(self):
        """Пользователь не может получить чужие категории"""
        create_category(self.user)
        self.set_token(self.fake_user)
        get_response = self.client.get('/api/transactions/category/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(get_response.content)['count'], 0)

    def test_post_category(self):
        """Пользователь может создать категорию"""
        self.set_token(self.user)
        post_response = self.client.post('/api/transactions/category/', self.category_init_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    def test_post_category_fake(self):
        """Анонимный пользователь не может создать категорию"""
        self.set_token()
        post_response = self.client.post('/api/transactions/category/', self.category_init_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)
