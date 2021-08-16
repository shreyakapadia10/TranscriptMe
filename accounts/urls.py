from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='Register'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout, name='Logout'),

    path('activate/<uidb64>/<token>/', views.activate_account, name='ActivateAccount'),
]