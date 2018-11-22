from fintech.models import Account, Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'uuid',
            'account',
            'transaction_date',
            'amount',
            'description',
            'active',
            'create_time',
            'update_time')

    def validate(self, data):
        """
        Check that the account has enough funds.
        """
        account = data['account']
        balance = account.balance + data['amount']
        if balance < 0:
            raise serializers.ValidationError("Account has not enough funds")
        data['account'].balance = balance
        return data

    def create(self, validated_data):
        account = validated_data['account']
        account.save()
        transaction = Transaction.objects.create(**validated_data)
        return transaction
