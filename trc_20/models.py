from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_init
from django.dispatch import receiver
from tronpy import Tron
import os

client = Tron(network=os.environ.get("TRON"))

User = get_user_model()


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    address = models.CharField(max_length=42, unique=True)
    private_key = models.CharField(max_length=64, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)

    def update_balance(self):
        try:
            balance = client.get_account_balance(self.address)
        except:
            balance = 0
        self.balance = balance
        self.save()
        return balance

    def __str__(self):
        return f"Wallet({self.address}) - Balance: {self.balance}"


@receiver(post_init, sender=Wallet)
def update_wallet_on_retrieve(sender, instance, **kwargs):
    instance.update_balance()


class Transaction(models.Model):
    sender = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="sent_transactions"
    )
    recipient = models.CharField(max_length=42)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    transaction_hash = models.CharField(max_length=66, unique=True)
    status = models.CharField(max_length=20, blank=True)
    block_number = models.IntegerField(blank=True, null=True)
    fee = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return f"Transaction ID: ({self.transaction_hash}) - Amount: {self.amount}"
