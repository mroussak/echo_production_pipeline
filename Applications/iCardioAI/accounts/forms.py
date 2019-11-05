from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django import forms


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=20, help_text='Required.')
    full_name = forms.CharField(max_length=100, help_text='Required.')

    class Meta:
        model = User
        fields = ('email', 'phone')
        
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
           raise ValidationError("Email exists")
       return self.cleaned_data