from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='Login')
def home(request):
    return render(request=request, template_name='index.html')