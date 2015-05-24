# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0002_auto_20150514_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='duracion',
            field=models.TimeField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='fecha',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='fecha_seleccion',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='hora',
            field=models.TimeField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='larga_duracion',
            field=models.CharField(max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='precio',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='tipo',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='titulo',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='url',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='usuario',
            field=models.ManyToManyField(to='actividades_madrid.Usuario', blank=True),
            preserve_default=True,
        ),
    ]
