from django.db import models

# Create your models here.


class Actividad(models.Model):
    titulo = models.TextField(blank=True)
    tipo = models.TextField(blank=True)
    precio = models.TextField(blank=True)
    fecha = models.DateField(blank=True)
    hora = models.TimeField(blank=True)
    larga_duracion = models.CharField(max_length=32, blank=True)
    url = models.TextField(blank=True) 
    fecha_seleccion = models.DateField(blank=True)

    def get_absolute_url(self):
        return '/actividades/%d' % self.id

class Usuario(models.Model):
    nombre = models.CharField(max_length=32)
    titulo_personal = models.TextField(blank=True)
    actividades = models.ManyToManyField(Actividad, blank=True)

class UltimaFecha(models.Model):
    #Fecha actualizacion de actividades
    fecha = models.DateTimeField()

class EstiloCss(models.Model):
    usuario = models.TextField(blank=True)
    banner = models.TextField(blank=True)
    login = models.TextField(blank=True)
    menu = models.TextField(blank=True)
    pie = models.TextField(blank=True)
    

