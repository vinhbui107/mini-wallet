from django.db import transaction
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from wallets.models import Wallet as WalletModel, Transaction
from wallets.serializers import (
    WalletSerializer,
    WalletDisabledSerializer,
    PatchWalletSerializer,
    PostTransactionSerializer,
    DepositSerializer,
    WithdrawalSerializer,
)
from common.helpers import (
    get_request_data,
    validate_data,
    check_can_withdrawal,
)
from common.responses import ApiSuccessResponse, ApiErrorResponse


def get_active_wallet(user):
    return WalletModel.objects.filter(user_id=user, is_active=True).first()


def get_disable_wallet(user):
    return WalletModel.objects.filter(user_id=user, is_active=False).first()


class Wallet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        wallet = get_active_wallet(user=user)

        if not wallet:
            return ApiErrorResponse(message="Please enable your wallet!")

        wallet_serializer = WalletSerializer(
            wallet, context={"request": request}
        )
        return ApiSuccessResponse(data={"wallet": wallet_serializer.data})

    def post(self, request):
        user = request.user
        wallet = get_disable_wallet(user)

        if not wallet:
            return ApiErrorResponse(message="Your wallet is already enabled!")

        with transaction.atomic():
            wallet.is_active = True
            wallet.enabled_at = now()
            wallet.save()

        wallet_serializer = WalletSerializer(
            wallet, context={"request": request}
        )
        return ApiSuccessResponse(data={"wallet": wallet_serializer.data})

    def patch(self, request):
        data = validate_data(PatchWalletSerializer, data=request.data)
        is_disabled = data.get("is_disabled")

        user = request.user
        wallet = get_active_wallet(user)

        if not wallet:
            return ApiErrorResponse(message="Please enable your wallet!")

        if not is_disabled:
            return ApiErrorResponse(message="Disable your wallet fail!")

        with transaction.atomic():
            wallet.is_active = False
            wallet.disabled_at = now()
            wallet.save()

        wallet_serializer = WalletDisabledSerializer(
            wallet, context={"request": request}
        )
        return ApiSuccessResponse(data={"wallet": wallet_serializer.data})


class Deposit(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request_data = get_request_data(request)
        data = validate_data(PostTransactionSerializer, request_data)

        amount = data.get("amount")
        reference_id = data.get("reference_id")

        user = request.user
        wallet = get_active_wallet(user)

        if not wallet:
            return ApiErrorResponse(message="Please enable your wallet!")

        try:
            with transaction.atomic():
                new_deposit = Transaction.objects.create(
                    wallet=wallet,
                    amount=amount,
                    transaction_type=True,
                    reference_id=reference_id,
                )
                new_deposit.save()

                wallet.balance += amount
                wallet.save()

            new_deposit_serializer = DepositSerializer(
                new_deposit, context={"request": request}
            )
            return ApiSuccessResponse(
                data={"deposit": new_deposit_serializer.data}
            )
        except Exception:
            return ApiErrorResponse(message=Exception)


class Withdrawal(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request_data = get_request_data(request)
        data = validate_data(PostTransactionSerializer, request_data)

        amount = data.get("amount")
        reference_id = data.get("reference_id")

        user = request.user
        wallet = get_active_wallet(user)

        if not wallet:
            return ApiErrorResponse(message="Please enable your wallet!")

        if not check_can_withdrawal(amount=amount, wallet=wallet):
            return ApiErrorResponse(
                message="Your wallet's not enough money to withdrawal!"
            )

        try:
            with transaction.atomic():
                new_withdrawal = Transaction.objects.create(
                    wallet=wallet,
                    amount=amount,
                    transaction_type=False,
                    reference_id=reference_id,
                )
                new_withdrawal.save()

                wallet.balance -= amount
                wallet.save()

            new_withdrawal_serializer = WithdrawalSerializer(
                new_withdrawal, context={"request": request}
            )
            return ApiSuccessResponse(
                data={"withdrawal": new_withdrawal_serializer.data}
            )
        except Exception:
            return ApiErrorResponse(message="Withdrawal fail!")
