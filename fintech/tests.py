from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from fintech.models import Account, Transaction

class GetTestCase(APITestCase):
    def test_get_account_balance(self):
        user1 = User.objects.create_user(username='user1', password='12345')
        user1.save()
        account = Account.objects.create(name='test account 1', balance=100, user=user1)
        account.save()
        response = self.client.get('/accounts/' + str(account.uuid) + '/balance')
        self.assertEqual(response.data, {'balance': 100})

    def test_get_account_transactions(self):
        user1 = User.objects.create_user(username='user1', password='12345')
        user1.save()
        account = Account.objects.create(name='test account 1', balance=100, user=user1)
        account.save()
        date = "2018-11-21"
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
        response = self.client.get('/accounts/' + str(account.uuid) + '/transactions/')
        self.assertEqual(len(response.data), 2)
