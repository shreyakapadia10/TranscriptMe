from accounts.models import User
from django.shortcuts import redirect, render
from .forms import UserProfileUpdationForm, UserRegistrationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password= form.cleaned_data.get('password')
            app_id = form.cleaned_data.get('app_id')
            secret_id = form.cleaned_data.get('secret_id')
            profile_picture = 'default/user_avatar.png'

            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, app_id=app_id, secret_id=secret_id, profile_picture=profile_picture, password=password)

            user.is_active = True
            user.save()

            messages.success(request=request, message='Account Created Successfully!')
            return redirect('Login')
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