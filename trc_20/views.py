from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from .utils import generate_new_wallet, make_transaction, get_transaction_history


class WalletCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a wallet for the authenticated user",
        responses={
            200: WalletSerializer(),
            201: WalletSerializer(),
            404: openapi.Response(description="No wallet found"),
        },
    )
    def post(self, request):
        user = self.request.user

        wallet = user.wallet if hasattr(user, "wallet") else None

        if wallet:
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            new_wallet = generate_new_wallet(user=user)
            new_wallet.save()

            serializer = WalletSerializer(new_wallet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class WalletDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the wallet details of the authenticated user",
        responses={
            200: WalletSerializer(),
            404: openapi.Response(description="No wallet found"),
        },
    )
    def get(self, request):
        user = self.request.user

        wallet = user.wallet if hasattr(user, "wallet") else None

        if wallet:
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "No wallet found."}, status=status.HTTP_404_NOT_FOUND
            )


class TransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a transaction from the authenticated user's wallet",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["recipient", "amount"],
            properties={
                "recipient": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Recipient address"
                ),
                "amount": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Amount to be transferred"
                ),
            },
        ),
        responses={
            201: TransactionSerializer(),
            400: openapi.Response(description="Invalid request"),
            404: openapi.Response(description="No wallet found"),
        },
    )
    def post(self, request):
        user = self.request.user
        recipient_address = request.data.get("recipient")
        amount = request.data.get("amount")

        if not recipient_address or not amount:
            return Response(
                {"message": "Recipient address and amount are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = float(amount)
        except ValueError:
            return Response(
                {"message": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST
            )

        wallet = user.wallet if hasattr(user, "wallet") else None

        if wallet:
            transaction = make_transaction(wallet, recipient_address, amount)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": "You have no existing wallet."},
                status=status.HTTP_404_NOT_FOUND,
            )


class TransactionHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the transaction history of the authenticated user's wallet",
        responses={
            200: openapi.Response(
                description="List of transactions",
                schema=TransactionSerializer(many=True),
            ),
            404: openapi.Response(description="No wallet found"),
        },
    )
    def get(self, request):
        user = self.request.user
        wallet = user.wallet if hasattr(user, "wallet") else None

        if wallet:
            transactions = get_transaction_history(wallet)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "No wallet found."}, status=status.HTTP_404_NOT_FOUND
            )


class SingleTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific transaction by ID",
        responses={
            200: TransactionSerializer(),
            404: openapi.Response(
                description="Transaction not found or No wallet found"
            ),
        },
    )
    def get(self, request, transaction_id):
        user = self.request.user
        wallet = user.wallet if hasattr(user, "wallet") else None

        if wallet:
            try:
                transaction = Transaction.objects.get(sender=wallet, id=transaction_id)
                serializer = TransactionSerializer(transaction)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Transaction.DoesNotExist:
                return Response(
                    {"message": "Transaction not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": "No wallet found."}, status=status.HTTP_404_NOT_FOUND
            )
