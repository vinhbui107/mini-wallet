from django.db import models
from uuid import uuid4

from users.models import User


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    enabled_at = models.DateTimeField(auto_now_add=True)
    disabled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wallet"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="wallet"
    )
    reference_id = models.UUIDField(default=uuid4, unique=True, editable=False)
    amount = models.IntegerField(default=0)
    transaction_type = models.BooleanField(
        default=True
    )  # withdrawal = 0, deposit = 1
    status = models.BooleanField(default=True)  # success = 1, failure = 0
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction"

    @classmethod
    def is_reference_id_taken(cls, reference_id):
        transaction = cls.objects.filter(reference_id=reference_id)
        if not transaction.exists():
            return False
        return True
