from fintech.models import Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('transaction_date', 'amount', 'description', 'create_time', 'update_time')
