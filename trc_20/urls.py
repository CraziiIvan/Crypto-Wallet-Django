from django.urls import path
from .views import WalletCreateAPIView

urlpatterns = [
    path('api/create-wallet/', WalletCreateAPIView.as_view(), name='create-wallet'),
]
