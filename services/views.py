from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User, Username
from .serializers import UserSerializer
import re 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def server_name(request, username=None):
    if request.method == 'POST':
        username = request.data.get('username')
    elif request.method == 'GET':
        if not username:
            username = request.GET.get('username')

    if not username:
        return Response({"error": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)

    username = username.lower()  # Преобразуем имя в нижний регистр

    # Проверяем, что имя содержит только латинские буквы
    if not re.fullmatch(r'[a-zA-Z]+', username):
        return Response({"error": "Username must contain only Latin letters"}, status=status.HTTP_400_BAD_REQUEST)

    # Проверяем существование имени в базе данных
    if Username.objects.filter(name=username).exists():
        return Response({"username": username}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No such name"}, status=status.HTTP_400_BAD_REQUEST)
