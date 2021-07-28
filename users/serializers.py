from rest_framework import serializers

from common.validators import validate_uuid4


class PostUserSerializer(serializers.Serializer):
    customer_xid = serializers.UUIDField(
        validators=[validate_uuid4],
        required=True,
    )
