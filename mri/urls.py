from django.urls import path
from . import views
from .views import user_register
from .views import user_login, user_logout
from .views import dashboard
from .views import update_hospital
from .views import delete_hospital
from .views import register_hospital



urlpatterns = [
    # path('', views.upload_image, name='upload_image'),
    path('result/<int:pk>/', views.result, name='result'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('dashboard/', dashboard, name='dashboard'),  # Add this
     path('update-hospital/', update_hospital, name='update_hospital'),
     path('delete-hospital/', delete_hospital, name='delete_hospital'),
    path('register-hospital/', register_hospital, name='register_hospital'),
    
    path('', views.home, name='home'),  # First page is login but only on first visit
    path('upload/', views.upload_image, name='upload_image'),
    
    
    path('mri-history/', views.mri_history, name='mri_history'),
    
    
]
