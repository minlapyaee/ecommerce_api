from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User

import jwt
import datetime


class Register(APIView):
    def post(self, request):

        print(request.data)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": 'success',
            "data": serializer.data
        })


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2400),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            "message": 'success',
            'token': token
        }
        return response


class UserAuth(APIView):

    def post(self, request):

        token = request.data['token']
        print(token)
        print(request.COOKIES)
        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')

        user = User.objects.get(pk=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
