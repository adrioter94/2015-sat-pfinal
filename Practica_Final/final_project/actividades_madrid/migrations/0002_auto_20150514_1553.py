# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='duracion',
            field=models.TimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='hora',
            field=models.TimeField(),
            preserve_default=True,
        ),
    ]
