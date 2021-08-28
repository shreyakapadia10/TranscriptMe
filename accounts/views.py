from accounts.models import User
from django.shortcuts import redirect, render
from .forms import UserProfileUpdationForm, UserRegistrationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Email Verification Imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # Getting form data
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password= form.cleaned_data.get('password')
            app_id = form.cleaned_data.get('app_id')
            secret_id = form.cleaned_data.get('secret_id')
            profile_picture = 'default/user_avatar.png'

            # Creating user
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, app_id=app_id, secret_id=secret_id, profile_picture=profile_picture, password=password)

            user.is_active = False
            user.save()

            # Email Verification Process
            current_site = get_current_site(request) # getting current site
            mail_subject = 'Activate Your Account' # Setting mail subject
            # Rendering html template and passing it necessary values
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email # email of the user
            send_email = EmailMessage(mail_subject, message, to=[to_email]) # creating mail to be sent
            send_email.send() # Sending mail

            return redirect(f'/accounts/login/?command=verification&email={email}')
        else:
            messages.error(request, form.errors, form.errors)
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request=request, template_name='accounts/register.html', context=context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(request=request, email=email, password=password)

        if user is not None:
            auth.login(request=request, user=user)
            return redirect('Home')
        else:
            messages.error(request, 'Please check the credentials again!')
            return redirect('Login')

    return render(request=request, template_name='accounts/login.html')


@login_required(login_url='Login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out now!')
    return redirect('Login')

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # decoding the url
        user = User._default_manager.get(pk=uid) # getting user from the given uid
    except (TypeError, ValueError, User.DoesNotExist, OverflowError): # in case of invalid uid or user
        user = None

    if user is not None and default_token_generator.check_token(user, token): # if the link is valid
        user.is_active = True # set is_active status of user to true, so that user can login
        user.save() # saving user details

        messages.success(request=request, message='Your account has been activated successfully! You can login now!')
        
    else:
        messages.error(request, 'Invalid activation link!')

    return redirect('Login')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)

            # Reset Password Mail
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/password/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request=request, message='Password Reset Link Has Been Sent Successfully! Click on the link to reset your password!')

            return redirect('Login')
        else:
            messages.error(request=request, message='Account does not exists!')
            return redirect('ForgotPassword')
    
    return render(request, 'accounts/password/forgot-password.html')


def resetPasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExistError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password!')
        return redirect('ResetPassword')
    else:
        messages.error(request, 'This Link Has Been Expired!')
        return redirect('Login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been changed successfully! You can Login Now!')
            return redirect('Login')
        else:
            messages.error(request, "Password doesn't match!")
            return redirect('ResetPassword')

    return render(request, 'accounts/password/reset-password.html')
@login_required(login_url='Login')
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileUpdationForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('UpdateProfile')
    else:
        form = UserProfileUpdationForm(instance=user)
    
    context={
        'user': user,
        'form': form,
    }

    return render(request, 'accounts/update_profile.html', context)
