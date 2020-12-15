from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Candidatura(models.Model):
    nombre = models.TextField()
    delegadoCentro = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='delegado_centro')
    representanteDelegadoPrimero = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='representante_primero')
    representanteDelegadoSegundo = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='representante_segundo')
    representanteDelegadoTercero = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='representante_tercero')
    representanteDelegadoCuarto = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='representante_cuarto')
    representanteDelegadoMaster = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='representante_master')

    def __str__(self):
        return self.nombre