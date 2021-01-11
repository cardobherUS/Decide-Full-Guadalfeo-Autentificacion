from django.forms import ModelForm
from .models import VotingUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use")
       return self.cleaned_data

    class Meta:
        model = User
        fields = ["username", "email","password1", "password2"]

class RegisterVotingUserForm(ModelForm):
    class Meta:
        model = VotingUser
        fields = '__all__'
        exclude = ['user']


class ProfileUserForm(ModelForm):
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use")
       return self.cleaned_data

    class Meta:
        model = User
        fields = ['username','email']


class ProfileVotingUserForm(ModelForm):
    class Meta:
        model = VotingUser
        fields = ['titulo', 'curso', 'edad']
        exclude = ['user']