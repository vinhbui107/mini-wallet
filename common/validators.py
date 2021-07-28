from uuid import UUID
from rest_framework.exceptions import ValidationError

from wallets.models import Transaction, Wallet


def validate_uuid4(uuid_string):
    try:
        version = UUID(str(uuid_string)).version
        if version != 4:
            raise ValidationError("Must be a valid UUID4")
    except (ValueError):
        raise ValidationError("Must be a valid UUID4")


def reference_id_not_taken_validator(reference_id):
    if Transaction.is_reference_id_taken(reference_id):
        raise ValidationError("The reference id is already taken.")
