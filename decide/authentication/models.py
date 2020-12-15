from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from decide.voting.models import Candidatura

# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class VotingUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(validators=[
        RegexValidator(
            regex='^\d{8}[A-Z]{1}$',
            message='El formato debe ser 8 digitos y una letra mayuscula.'
        )
        ])
    Sexo_Enum = (
        ('NONE', 'None'),
        ('HOMBRE', 'Hombre'),
        ('MUJER', 'Mujer'),
        ('OTRO', 'Otro'),
    )
    sexo = models.CharField(
        max_length=6,
        choices=Sexo_Enum,
        default='NONE',
    )
    titulo = models.CharField(max_length=100, blank=False)
    curso = IntegerRangeField(min_value=1, max_value=4)
    candidatura = models.models.ForeignKey(Candidatura, on_delete=models.SET_NULL)


