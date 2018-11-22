from rest_framework import views, viewsets, mixins
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import TransactionSerializer

class GetAccountBalance(views.APIView):

    def get(self, request, pk):
        account = Account.objects.get(uuid=pk)
        return Response({'balance': account.balance})

class TransactionList(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.none()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        account = Account.objects.get(uuid=pk)
        return account.transactions.filter(active=True)
