from django.urls import path
from .views import *

urlpatterns = [
    path('create-client/', add_Client, name='create-client'),
    path('delete-client/<int:ClientId>/', delete_Client, name='delete-client'),
    path('update-client/<int:ClientId>/', update_Client, name='update-client'),
    path('all-client/', view_Client, name='view-client'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('logout/', logout_view, name='token_logout'),                        # Logout
]