from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .models import Client, CoachNutritionist
from .serializers import ClientSerializer, CoachNutriSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#User = get_user_model()

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

# Profile utilisateur générique
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_user_profile(request):
    user = request.user

    # Prepare user profile data
    user_profile = {
        'userId': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'is_client': getattr(user, 'is_client', False),
        'is_coach': getattr(user, 'is_coach', False),
        'is_nutritionist': getattr(user, 'is_nutritionist', False),
    }

    # Check if the user is a CoachNutritionist and retrieve the instance
    if user.is_coach or user.is_nutritionist:
        try:
            coach_nutritionist_instance = CoachNutritionist.objects.get(pk=user.pk)
            user_profile.update({
                'certifications': coach_nutritionist_instance.certifications or '',
                'bio': coach_nutritionist_instance.bio or '',
                'photo': coach_nutritionist_instance.photo or '',  # Provide a default value if not set
            })
        except CoachNutritionist.DoesNotExist:
            # Handle the case where the user is not found in the CoachNutritionist table
            user_profile.update({
                'certifications': '',
                'bio': '',
                'photo': None,
            })
    else:
        # If the user is not a CoachNutritionist, we can add empty values or omit them
        user_profile.update({
            'certifications': '',
            'bio': '',
            'photo': None,
        })

    return Response(user_profile)

# Inscription d'un client
@api_view(['POST'])
def register_client(request):
    print(request.data)
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        client = serializer.save(is_client=True)
        return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'error': 'User  account is inactive.'}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    # Retrieve the appropriate instance based on user type
    if user.is_client:
        client_nutritionist_instance = Client.objects.get(pk=user.pk)
        serializer = ClientSerializer(client_nutritionist_instance)
                
    elif user.is_coach or user.is_nutritionist:
        # Assuming CoachNutritionist is the base class for both Coach and Nutritionist
        coach_nutritionist_instance = CoachNutritionist.objects.get(pk=user.pk)
        serializer = CoachNutriSerializer(coach_nutritionist_instance)
    else:
        return Response({'error': 'User  type not recognized.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'user': serializer.data,
        'token': {
            'refresh': str(refresh),
            'access': str(access_token),
        }
    }, status=status.HTTP_200_OK)
# Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = request.auth
        if token:
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"detail": "No active token found."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Gestion des Coach/Nutritionist
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def view_CoachNutri(request):
    items = CoachNutritionist.objects.filter(**request.query_params.dict()) if request.query_params else CoachNutritionist.objects.all()
    if items:
        serializer = CoachNutriSerializer(items, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def add_CoachNutri(request):
    serializer = CoachNutriSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # This will call the `create` method in the serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperUser])
def delete_CoachNutri(request, CoachNutriId):
    try:
        coach_nutri = CoachNutritionist.objects.get(id=CoachNutriId)
        coach_nutri.delete()
        return Response({'message': 'Coach/Nutritionist deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except CoachNutritionist.DoesNotExist:
        return Response({'error': 'Coach/Nutritionist not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperUser])
def update_CoachNutri(request, CoachNutriId):
    try:
        coach_nutri = CoachNutritionist.objects.get(id=CoachNutriId)
        serializer = CoachNutriSerializer(coach_nutri, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    except CoachNutritionist.DoesNotExist:
        return Response({'error': 'Coach/Nutritionist not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Gestion des Clients
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_Client(request):
    items = Client.objects.filter(**request.query_params.dict()) if request.query_params else Client.objects.all()
    if items:
        serializer = ClientSerializer(items, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_Client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        client = serializer.save(is_client=True)
        return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_Client(request, ClientId):
    try:
        client = Client.objects.get(id=ClientId)
        client.delete()
        return Response({'message': 'Client deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_Client(request, ClientId):
    try:
        client = Client.objects.get(id=ClientId)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
