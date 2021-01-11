from django.forms import ModelForm
from .models import VotingUser
from django.contrib.auth.models import User


class RegisterVotingUserForm(ModelForm):
    class Meta:
        model = VotingUser
        fields = '__all__'
        exclude = ['user']


class ProfileUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileVotingUserForm(ModelForm):
    class Meta:
        model = VotingUser
        fields = ['titulo', 'curso', 'edad']
        exclude = ['user']