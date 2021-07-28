import datetime
from pytz import utc
from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import User as UserModel
from users.serializers import PostUserSerializer
from wallets.models import Wallet
from common.helpers import get_request_data, validate_data
from common.responses import ApiSuccessResponse


class User(APIView):
    def post(self, request):
        data = validate_data(PostUserSerializer, data=request.data)
        user_id = data.get("customer_xid")

        user = UserModel.objects.filter(pk=user_id).first()

        if user:
            token, created = Token.objects.get_or_create(user=user)

            if not created:  # handle expire token
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()
        else:
            with transaction.atomic():
                new_user = UserModel.objects.create_user(
                    username=user_id,
                    id=user_id,
                    email="",
                    password="",
                )
                new_user.save()

                Wallet.objects.create(user=new_user)
                token, created = Token.objects.get_or_create(user=new_user)

        return ApiSuccessResponse(data={"token": token.key})
