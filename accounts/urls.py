from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='Register'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout, name='Logout'),

    path('change-password/', views.change_password, name='ChangePassword'),
]