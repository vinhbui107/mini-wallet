from rest_framework.serializers import Serializer
from wallets.models import Wallet


def validate_data(schema_cls: Serializer, data: dict):
    """
    Validate data using Marshmallow schema
    Return validated data if success, raise ValidationError if failed
    """
    schema = schema_cls(data=data)
    schema.is_valid(raise_exception=True)
    return schema.validated_data


def get_request_data(request):
    request_data = request.data.copy()
    query_params = request.query_params.dict()
    request_data.update(query_params)
    return request_data


def check_can_withdrawal(amount, wallet):
    return True if wallet.balance >= amount else False
