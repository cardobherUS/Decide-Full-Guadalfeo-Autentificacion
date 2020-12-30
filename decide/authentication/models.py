from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from voting.models import Candidatura


class VotingUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    dni = models.CharField(max_length=9, unique=True, validators=[
        RegexValidator(
            regex='^\d{8}[A-Z]{1}$',
            message='El formato debe ser 8 digitos y una letra mayuscula.'
        )
    ], verbose_name="NIF")

    Sexo_Enum = (
        ('HOMBRE', 'Man'),
        ('MUJER', 'Woman'),
        ('OTRO', 'Other'),
    )
    sexo = models.CharField(max_length=6, choices=Sexo_Enum, default='OTRO', blank=False, verbose_name="Gender")
    titulo = models.CharField(max_length=100, blank=False, verbose_name="Grade")

    Curso_Enum = (
        ('PRIMERO', 'First'),
        ('SEGUNDO', 'Second'),
        ('TERCERO', 'Third'),
        ('CUARTO', 'Fourth'),
        ('MASTER', 'Master'),
    )

    curso = models.CharField(max_length=7, choices=Curso_Enum, default='PRIMERO', blank=False, verbose_name="Year")
    candidatura = models.ForeignKey(Candidatura, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Candidature")

    def __str__(self):
        return self.user.__str__()
