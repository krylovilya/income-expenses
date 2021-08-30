import json

from rest_framework import status

from apps.transactions.models import Transaction
from apps.transactions.tests.init_tests import (BaseAPITests, create_category,
                                                create_transaction)


class TransactionAPITests(BaseAPITests):
    def setUp(self):
        super().setUp()
        self.transaction_init_data = {
            'owner': self.user.id,
            'category': None,
            'amount': 100,
        }

    def test_put_transaction(self):
        """Пользователь может заменить свою транзакцию"""
        self.set_token(self.user)
        category_id, transaction_id = create_transaction(self.user)
        put_response = self.client.put(f'/api/transactions/transaction/{transaction_id}/',
                                       self.transaction_init_data | {
                                           'amount': 150,
                                           'category': category_id,
                                       }, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        transaction_object = Transaction.objects.get(id=transaction_id)
        self.assertEqual(transaction_object.amount, 150)

    def test_put_transaction_fake(self):
        """Пользователь не может заменить чужую транзакцию"""
        category_id, transaction_id = create_transaction(self.user)
        self.set_token(self.fake_user)
        put_response = self.client.put(f'/api/transactions/transaction/{transaction_id}/',
                                       self.transaction_init_data | {
                                           'amount': 150,
                                           'category': category_id,
                                       }, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_404_NOT_FOUND)
        transaction_object = Transaction.objects.get(id=transaction_id)
        self.assertEqual(transaction_object.amount, 100)

    def test_patch_transaction(self):
        """Пользователь может обновить свою транзакцию"""
        self.set_token(self.user)
        _, transaction_id = create_transaction(self.user)
        patch_response = self.client.patch(f'/api/transactions/transaction/{transaction_id}/',
                                           {'amount': 150}, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        transaction_object = Transaction.objects.get(id=transaction_id)
        self.assertEqual(transaction_object.amount, 150)

    def test_patch_transaction_fake(self):
        """Пользователь не может обновить чужую транзакцию"""
        _, transaction_id = create_transaction(self.user)
        self.set_token(self.fake_user)
        put_response = self.client.patch(f'/api/transactions/transaction/{transaction_id}/',
                                         {'amount': 150}, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_404_NOT_FOUND)
        transaction_object = Transaction.objects.get(id=transaction_id)
        self.assertEqual(transaction_object.amount, 100)

    def test_delete_transaction(self):
        """Пользователь может удалить свою транзакцию"""
        self.set_token(self.user)
        _, transaction_id = create_transaction(self.user)
        delete_response = self.client.delete(f'/api/transactions/transaction/{transaction_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_transaction_fake(self):
        """Пользователь не может удалить чужую транзакцию"""
        _, transaction_id = create_transaction(self.user)
        self.set_token(self.fake_user)
        delete_response = self.client.delete(f'/api/transactions/transaction/{transaction_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_transaction(self):
        """Пользователь может получить свои транзакции"""
        self.set_token(self.user)
        _, transaction_id = create_transaction(self.user)
        get_response = self.client.get('/api/transactions/transaction/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(get_response.content)['count'], 1)

    def test_get_transaction_fake(self):
        """Пользователь не может получить чужие транзакции"""
        _, transaction_id = create_transaction(self.user)
        self.set_token(self.fake_user)
        get_response = self.client.get('/api/transactions/transaction/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(get_response.content)['count'], 0)

    def test_post_transaction(self):
        """Пользователь может создать транзакцию"""
        self.set_token(self.user)
        category_id = create_category(self.user)
        transaction_init_data = self.transaction_init_data | {'category': category_id}
        post_response = self.client.post('/api/transactions/transaction/',
                                         transaction_init_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    def test_post_transaction_fake(self):
        """Анонимный пользователь не может создать транзакцию"""
        category_id = create_category(self.user)
        transaction_init_data = self.transaction_init_data | {'category': category_id}
        self.set_token()
        post_response = self.client.post('/api/transactions/transaction/',
                                         transaction_init_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)
