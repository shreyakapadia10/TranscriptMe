from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='Register'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout, name='Logout'),

    path('activate/<uidb64>/<token>/', views.activate_account, name='ActivateAccount'),
    # Forget Password URLs
    path('forgot-password/', views.forgotPassword, name='ForgotPassword'),
    path('reset-password-validate/<uidb64>/<token>/', views.resetPasswordValidate, name='ResetPasswordValidate'),
    path('reset-password/', views.resetPassword, name='ResetPassword'),
]