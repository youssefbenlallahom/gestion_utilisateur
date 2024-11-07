from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('create-coach-nutri/', add_CoachNutri, name='coach-nutri-nutri'),
    path('delete-coach-nutri/<int:UserId>/', delete_CoachNutri, name='coach-nutri-nutri'),
    path('update-coach-nutri/<int:UserhId>/', update_CoachNutri, name='coach-nutri-nutri'),
    path('all-coach-nutri/', view_CoachNutri, name='view_coach-nutri'),
    path('login-coach/', login, name='token_obtain_pair'),
    #path('login_page/', login_page, name='login_page'),
    #path('login_page_react/', login_page, name='login_page'),
    path('logout-coach/', logout_view, name='token_logout'),
    path('profile-coach/', get_user_profile, name='user_profile'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('dashboard/', dashboard, name='dashboard'),
    #path('dashboard/coach_table/', coach_table, name='coach_table'), 
    #path('dashboard/nutri_table/', nutri_table, name='nutri_table'), 
    path('create-client/', add_Client, name='create-client'),
    path('delete-client/<int:ClientId>/', delete_Client, name='delete-client'),
    path('update-client/<int:ClientId>/', update_Client, name='update-client'),
    path('all-client/', view_Client, name='view-client'),
    path('login-client/', login, name='token_obtain_pair'),  # Login
    path('logout-client/', logout_view, name='token_logout'), 
    path('register-client/', register_client, name='token_logout'),  # Logout
]