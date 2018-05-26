from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        (1, 'buy'),
        (2, 'sell'),
    )
    created = models.DateTimeField(auto_now_add=True)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPES, default=1)
    crypto_symbol = models.CharField(max_length=10, blank=True, default='')
    price = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    owner = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

class UserBalance(models.Model):
    balance = models.FloatField(default=10000.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(user=instance)
