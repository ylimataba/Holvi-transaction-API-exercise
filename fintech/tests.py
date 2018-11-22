from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from fintech.models import Account, Transaction

class GetTestCase(APITestCase):
    account = Account.objects.none
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='12345')
        user1.save()
        account = Account.objects.create(name='test account 1', balance=100, user=user1)
        account.save()
        self.account = account

    def test_get_account_balance(self):
        uuid = self.account.uuid
        response = self.client.get('/accounts/' + str(uuid) + '/balance')
        self.assertEqual(response.data, {'balance': 100})

    def test_get_account_transactions(self):
        date = "2018-11-21"
        account = self.account
        transaction1 = Transaction.objects.create(
                account=account,
                transaction_date=date,
                amount=10,
                description='test1',
                active=True)
        transaction2 = Transaction.objects.create(
                account=account,
                transaction_date=date,
                amount=20,
                description='test2',
                active=True)
        transaction3 = Transaction.objects.create(
                account=account,
                transaction_date=date,
                amount=20,
                description='test3',
                active=False)
        transaction1.save()
        transaction2.save()
        transaction3.save()
        response = self.client.get('/transactions/?account=' + str(account.uuid))
        self.assertEqual(len(response.data), 2)

class PostTestCase(APITestCase):
    account = Account.objects.none
    url = reverse('transaction-list')
    data = {
        'transaction_date': "2018-11-21",
        'description':'Test',
        'active':True
    }
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='12345')
        user1.save()
        account = Account.objects.create(name='test account 1', balance=100, user=user1)
        account.save()
        self.account = account
        self.data['account'] = self.account.uuid

    def test_positive_transaction(self):
        self.data['amount'] = 20
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(uuid=response.data['account'])
        self.assertEqual(account.balance, 120)

    def test_negative_transaction(self):
        self.data['amount'] = -20
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(uuid=response.data['account'])
        self.assertEqual(account.balance, 80)

    def test_zero_balance_transaction(self):
        self.data['amount'] = -100
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(uuid=response.data['account'])
        self.assertEqual(account.balance, 0)

    def test_negative_balance_transaction(self):
        self.data['amount'] = -101
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        account = Account.objects.get(uuid=self.account.uuid)
        self.assertEqual(account.balance, 100)
