from rest_framework import serializers
from transactions.models import Transaction
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(many=True, queryset=Transaction.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'transactions')

class TransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Transaction
        fields = ('id', 'transaction_type', 'crypto_symbol', 'price', 'amount', 'created', 'owner')