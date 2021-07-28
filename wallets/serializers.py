from rest_framework import serializers

from wallets.models import Wallet, Transaction
from common.validators import validate_uuid4, reference_id_not_taken_validator
from common.serializer_fields import WalletStatusField, TransactionStatusField


class WalletSerializer(serializers.ModelSerializer):
    owner_by = serializers.UUIDField(source="user", read_only=True)
    status = WalletStatusField()

    class Meta:
        model = Wallet
        fields = (
            "id",
            "owner_by",
            "balance",
            "status",
            "enabled_at",
        )


class WalletDisabledSerializer(serializers.ModelSerializer):
    owner_by = serializers.UUIDField(source="user", read_only=True)
    status = WalletStatusField()

    class Meta:
        model = Wallet
        fields = (
            "id",
            "owner_by",
            "balance",
            "status",
            "disabled_at",
        )


class PatchWalletSerializer(serializers.Serializer):
    is_disabled = serializers.BooleanField(required=True)


class PostTransactionSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True, min_value=0)
    reference_id = serializers.UUIDField(
        validators=[validate_uuid4, reference_id_not_taken_validator],
        required=True,
    )


class DepositSerializer(serializers.ModelSerializer):
    deposited_by = serializers.UUIDField(source="wallet.user", read_only=True)
    status = TransactionStatusField()
    deposited_at = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Transaction
        fields = (
            "id",
            "deposited_by",
            "status",
            "deposited_at",
            "amount",
            "reference_id",
        )


class WithdrawalSerializer(serializers.ModelSerializer):
    withdrawn_by = serializers.UUIDField(source="wallet.user", read_only=True)
    status = TransactionStatusField()
    withdrawn_at = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Transaction
        fields = (
            "id",
            "withdrawn_by",
            "status",
            "withdrawn_at",
            "amount",
            "reference_id",
        )
