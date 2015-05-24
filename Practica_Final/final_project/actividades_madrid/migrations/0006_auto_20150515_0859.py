# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0005_remove_actividad_duracion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='precio',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
