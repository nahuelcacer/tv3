from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    usuario = models.CharField(max_length=120)
    direccion = models.CharField(max_length=250, null=True)
    dni = models.ImageField()