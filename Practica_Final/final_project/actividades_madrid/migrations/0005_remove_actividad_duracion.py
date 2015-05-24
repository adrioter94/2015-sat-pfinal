# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0004_auto_20150515_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividad',
            name='duracion',
        ),
    ]
