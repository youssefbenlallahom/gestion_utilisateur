from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth import authenticate
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


#def login_page(request):
    #return render(request, 'authentication-login.html')

#def dashboard(request):
   # return render(request, 'dashboard.html')

#def nutri_table(request):
    #return render(request, 'nutri_table.html')

#def coach_table(request):
    #return render(request, 'coach_table.html')
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    user_profile = {
        'userId': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'is_coach': getattr(user, 'is_coach', False),  # Use getattr to prevent errors if the field doesn't exist
        'is_nutritionist': getattr(user, 'is_nutritionist', False),
        'certifications': getattr(user, 'certifications', ''),
        'bio': getattr(user, 'bio', ''),
        'specialization': getattr(user, 'specialization', ''),
        'photo':user.photo,
    }
    return Response(user_profile)

# Login View
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Generate tokens for the user
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    # Serialize the user data
    serializer = CoachNutriSerializer(user)
    
    return Response({
        'user': serializer.data,
        'token': {
            'refresh': str(refresh),
            'access': str(access_token),
        }
    }, status=status.HTTP_200_OK)

# Logout View
@api_view(['POST'])
def logout_view(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def view_CoachNutri(request):
    if request.query_params:
        items = CoachNutri.objects.filter(**request.query_params.dict())
    else:
        items = CoachNutri.objects.all()

    if items:
        serializer = CoachNutriSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def add_CoachNutri(request):
    serializer = CoachNutriSerializer(data=request.data)
    if serializer.is_valid():
        CoachNutri_instance = serializer.save()  
        response_serializer = CoachNutriSerializer(CoachNutri_instance)  # Utiliser le serializer pour formater la réponse
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperUser])
def delete_CoachNutri(request, CoachNutriId):
    try:
        CoachNutri_instance = CoachNutri.objects.get(id=CoachNutriId)
    except CoachNutri.DoesNotExist:
        return Response({'error': 'CoachNutri not found.'}, status=status.HTTP_404_NOT_FOUND)

    CoachNutri_instance.delete()
    return Response({'message': 'CoachNutri deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperUser])
def update_CoachNutri(request, CoachNutriId):
    try:
        CoachNutri_instance = CoachNutri.objects.get(id=CoachNutriId)
    except CoachNutri.DoesNotExist:
        return Response({'error': 'CoachNutri not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CoachNutriSerializer(CoachNutri_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


