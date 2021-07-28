from django.contrib import admin
from django.urls import path, include

from users.views import User
from wallets.views import Wallet, Withdrawal, Deposit

api_patterns = [
    path("init", User.as_view()),
    path("wallet", Wallet.as_view()),
    path("wallet/deposits", Deposit.as_view()),
    path("wallet/withdrawals", Withdrawal.as_view()),
]

urlpatterns = [
    path("api/v1/", include(api_patterns)),
    path("admin/", admin.site.urls),
]
