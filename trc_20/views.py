from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Wallet
from .serializers import WalletSerializer
from .utils import generate_new_wallet

class WalletCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user

        # Check if the user already has a wallet
        wallet = user.wallet if hasattr(user, 'wallet') else None

        if wallet:
            # If wallet exists, return existing wallet details
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If wallet doesn't exist, create a new wallet
            new_wallet = generate_new_wallet(user=user)
            new_wallet.save()

            serializer = WalletSerializer(new_wallet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
