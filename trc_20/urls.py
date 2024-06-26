from django.urls import path
from .views import (
    WalletCreateAPIView,
    WalletDetailAPIView,
    TransactionAPIView,
    TransactionHistoryAPIView,
    SingleTransactionAPIView,
)

urlpatterns = [
    path("wallet/", WalletCreateAPIView.as_view(), name="create_wallet"),
    path("wallet/details/", WalletDetailAPIView.as_view(), name="wallet_details"),
    path("transaction/", TransactionAPIView.as_view(), name="make_transaction"),
    path(
        "transaction/history/",
        TransactionHistoryAPIView.as_view(),
        name="transaction_history",
    ),
    path(
        "transaction/<str:transaction_hash>/",
        SingleTransactionAPIView.as_view(),
        name="single_transaction",
    ),
]
