from rest_framework import generics
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class UserInformationView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)