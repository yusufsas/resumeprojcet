from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account

from .models import ImageUpload

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Lütfen geçerli bir e-posta adresi girin.')

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

class ClientSignUpForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['number']
        
        