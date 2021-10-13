from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializers


# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException("Password do not match!")

    serializer = UserSerializers(data=data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    pasword = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed("User not Found")
    if not user.check_password():
        raise exceptions.AuthenticationFailed("Incorrect Password")

    return Response("Success Login")


@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UserSerializers(users, many=True)
    return Response(serializer.data)
