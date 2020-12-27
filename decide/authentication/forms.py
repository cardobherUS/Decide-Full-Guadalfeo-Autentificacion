from django.forms import ModelForm
from .models import VotingUser


class RegisterVotingUserForm(ModelForm):
    class Meta:
        model = VotingUser
        fields = ['dni', 'sexo', 'titulo', 'curso', 'candidatura']