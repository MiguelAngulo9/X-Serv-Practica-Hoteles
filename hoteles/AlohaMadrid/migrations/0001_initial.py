# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-23 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_comentador', models.CharField(max_length=32)),
                ('contenido', models.TextField(max_length=500)),
                ('id_hotel', models.IntegerField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Estilo_CSS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=32)),
                ('titulo', models.CharField(max_length=32)),
                ('fuente', models.IntegerField()),
                ('color_fondo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('direccion', models.CharField(max_length=300)),
                ('numero_tlf', models.CharField(max_length=300)),
                ('contenido', models.TextField(max_length=800)),
                ('URL', models.URLField()),
                ('categoria', models.TextField(max_length=32)),
                ('subcategoria', models.TextField(max_length=32)),
                ('numero_coment', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel_Identificado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_hotel', models.IntegerField()),
                ('usuario', models.CharField(max_length=32)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_hotel', models.IntegerField()),
                ('URL', models.URLField()),
            ],
        ),
    ]