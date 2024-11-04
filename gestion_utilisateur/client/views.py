from rest_framework.decorators import api_view, permission_classes 
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajoute des claims supplémentaires
        token['username'] = user.username
        return token

# View pour le login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def view_Client(request):
    if request.query_params:
        items = Client.objects.filter(**request.query_params.dict())
    else:
        items = Client.objects.all()

    if items:
        serializer = ClientSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def add_Client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        Client_instance = serializer.save()  
        response_serializer = ClientSerializer(Client_instance)  # Utiliser le serializer pour formater la réponse
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperUser])
def delete_Client(request, ClientId):
    try:
        Client_instance = Client.objects.get(id=ClientId)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

    Client_instance.delete()
    return Response({'message': 'Client deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperUser])
def update_Client(request, ClientId):
    try:
        Client_instance = Client.objects.get(id=ClientId)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(Client_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View pour le logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # On récupère le token à partir des en-têtes
        token = request.auth
        if token:
            # On blackliste le token
            token.blacklist()  # Nécessite la configuration de la blacklist
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"detail": "No active token found."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
