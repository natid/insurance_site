from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework import status, views
from rest_framework.response import Response

from .serializers import UserSerializer
from django.contrib.auth.models import User
from insurance_crm.models import Agent
from django.db import IntegrityError


class LoginView(views.APIView):

    #@method_decorator(csrf_protect)
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )

        if user is None or not user.is_active:
            return Response({
                'status': 'Unauthorized',
                'message': 'Incorrect username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(views.APIView):

    def get(self, request):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class SignUpView(views.APIView):

    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email_address = request.data.get("email_address")
        phone_number = request.data.get("phone_number")
        license_number = request.data.get("license_number")
        password = request.data.get("password")


        try:
            user = User.objects.create_user(email_address, email_address, password)
        except IntegrityError:
            return Response({}, status=status.HTTP_409_CONFLICT)

        agent = Agent.objects.create(user=user, first_name=first_name, last_name=last_name, phone_number=phone_number, license_number=license_number)
        user.save()
        agent.save()

        return Response({}, status=status.HTTP_200_OK)





