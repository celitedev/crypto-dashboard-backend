from transactions.models import Transaction
from transactions.models import UserBalance
from transactions.serializers import TransactionSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from transactions.serializers import UserSerializer
from rest_framework import permissions
from transactions.permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def make_transaction(request):
    user = UserSerializer(User.objects.get(username=request.user))
    balance = UserBalance.objects.get(user=user.data['id'])
    if request.data['transaction_type'] == 1 and balance.balance < request.data['price'] * request.data['amount']:
        return Response({"details": "Your balance is not enough."}, status=status.HTTP_400_BAD_REQUEST)

    newBalance = balance.balance
    if request.data['transaction_type'] == 1:
        newBalance -= request.data['price'] * request.data['amount']
    else:
        newBalance += request.data['price'] * request.data['amount']
    balance.balance = newBalance
    balance.save()
   
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def get_balance(request):
    user = UserSerializer(User.objects.get(username=request.user))
    balance = UserBalance.objects.get(user=user.data['id'])
    return JsonResponse({"balance": balance.balance}, status=status.HTTP_200_OK)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_anonymous:
            return Transaction.objects.all()
        else:
            return Transaction.objects.filter(owner=user)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
