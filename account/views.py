from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView



from .serializers import RegistrationSerializer, UserSerializer, GroupSerializer
from .models import User
from django.contrib.auth.models import Group


class RegisterView(GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Succesfully registered", 201)


class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = User.objects.filter(
            email=email, activation_code=activation_code
        ).first()
        message = (
            "User does not exists",
            "Successfully activated"
        )
        if not user:
            return Response(message[0], 400)
        user.activation_code = ""
        user.is_active = True
        user.save()
        return Response(message[-1], 200)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('group',)
    search_fields = ('first_name', 'last_name', 'phone')


class GroupListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
