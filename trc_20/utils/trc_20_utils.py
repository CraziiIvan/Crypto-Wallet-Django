from tronpy import Tron
from tronpy.keys import PrivateKey
from ..models import Wallet, Transaction
from django.contrib.auth import get_user_model
import os
import dotenv

dotenv.load_dotenv()

User = get_user_model()
client = Tron(network=os.environ.get("TRON"))


def generate_new_wallet(user):

    private_key = PrivateKey.random()
    address = private_key.public_key.to_base58check_address()

    try:
        wallet = Wallet.objects.create(
            user=user,
            address=address,
            private_key=private_key.hex(),
            balance=0.0,
        )
    except:
        wallet = user.wallet

    return wallet


def make_transaction(sender_wallet, recipient_address, amount):
    try:
        private_key = PrivateKey(bytes.fromhex(sender_wallet.private_key))
        txn = (
            client.trx.transfer(
                sender_wallet.address, recipient_address, int(amount * 1000000)
            )
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(private_key)
            .broadcast()
        )
        txn_result = txn.wait()

        transaction = Transaction.objects.create(
            sender=sender_wallet,
            recipient=recipient_address,
            amount=amount,
            transaction_hash=txn_result["id"],
            status=txn_result.get("status", ""),
            block_number=txn_result.get("block_number"),
            fee=txn_result.get("fee", 0.0),
        )

        return transaction
    except Exception as ex:
        return {"error": str(ex)}


def get_transaction_history(wallet):
    return Transaction.objects.filter(sender=wallet).order_by("-timestamp")


def get_wallet_balance(wallet):
    try:
        balance = client.get_account_balance(wallet.address)
    except:
        balance = 0
    wallet.balance = balance
    wallet.save()
    return balance
