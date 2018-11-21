from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, Transaction

class GetAccountBalance(APIView):

    def get(self, request, pk):
        account = Account.objects.get(uuid=pk)
        return Response({'balance': account.balance})
