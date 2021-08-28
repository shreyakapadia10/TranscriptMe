from django import forms
from .models import User
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserChangeForm

# User Registration Form
class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Create New Password'}))
    confirm_password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'app_id', 'secret_id', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs) -> None:
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if self.fields[field].help_text != '':
                self.fields[field].widget.attrs['placeholder'] = self.fields[field].help_text

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("New Password and Confirm Password Doesn't Match")


# User Updation Form at Admin Side
class UserUpdationForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')


# User Profile Updation Form
class UserProfileUpdationForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'app_id', 'secret_id', 'profile_picture']
    
    def __init__(self, *args, **kwargs) -> None:
        super(UserProfileUpdationForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'