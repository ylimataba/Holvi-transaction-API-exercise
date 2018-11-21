from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from fintech.models import Account

class BalanceTestCase(APITestCase):
    def test_get_account_balance(self):
        user1 = User.objects.create_user(username='user1', password='12345')
        user1.save()
        account = Account.objects.create(name='test account 1', balance=100, user=user1)
        account.save()
        response = self.client.get('/accounts/' + str(account.uuid) + '/balance')
        self.assertEqual(response.data, {'balance': 100})
