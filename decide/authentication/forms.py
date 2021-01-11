from django.forms import ModelForm
from .models import VotingUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email","password1", "password2"]

class RegisterVotingUserForm(ModelForm):
    class Meta:
        model = VotingUser
        fields = '__all__'
        exclude = ['user']


class ProfileUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']


class ProfileVotingUserForm(ModelForm):
    class Meta:
        model = VotingUser
        fields = ['titulo', 'curso', 'edad']
        exclude = ['user']