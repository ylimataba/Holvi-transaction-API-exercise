from rest_framework import views, viewsets, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import TransactionSerializer

class GetAccountBalance(views.APIView):
    def get(self, request, pk):
        account = Account.objects.get(uuid=pk)
        return Response({'balance': account.balance})

class TransactionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.none()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.none()
        account_uuid = self.request.query_params.get('account', None)
        if account_uuid is not None:
            account = Account.objects.get(uuid=account_uuid)
            queryset = account.transactions.filter(active=True)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
