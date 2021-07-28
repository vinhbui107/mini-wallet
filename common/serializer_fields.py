from rest_framework.fields import Field
from datetime import datetime
from django.utils import timezone


class WalletStatusField(Field):
    def __init__(self, *args, **kwargs):
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        super(WalletStatusField, self).__init__(**kwargs)

    def to_representation(self, wallet):
        return "enabled" if wallet.is_active is True else "disabled"


class TransactionStatusField(Field):
    def __init__(self, *args, **kwargs):
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        super(TransactionStatusField, self).__init__(**kwargs)

    def to_representation(self, transaction):
        return "success" if transaction.status is True else "failure"
