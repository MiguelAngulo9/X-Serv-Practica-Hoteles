from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hotel(models.Model):
    nombre = models.CharField(max_length = 300)
    direccion = models.CharField(max_length = 300)
    numero_tlf = models.CharField(max_length = 300)
    contenido = models.TextField(max_length = 800)
    URL = models.URLField()
    categoria = models.TextField(max_length =32)
    subcategoria = models.TextField(max_length =32)
    numero_coment = models.IntegerField()

class Imagen(models.Model):
    id_hotel = models.IntegerField()
    URL = models.URLField()

class Comentario(models.Model):
    usuario_comentador = models.CharField(max_length = 32)
    contenido = models.TextField(max_length = 500)
    id_hotel = models.IntegerField()
    fecha = models.DateField()

class Hotel_Identificado(models.Model):
    id_hotel = models.IntegerField()
    usuario = models.CharField(max_length = 32)
    fecha = models.DateField()

class Estilo_CSS(models.Model):
    usuario = models.CharField(max_length = 32)
    titulo = models.CharField(max_length = 32)
    fuente = models.IntegerField()
    color_fondo = models.TextField()
