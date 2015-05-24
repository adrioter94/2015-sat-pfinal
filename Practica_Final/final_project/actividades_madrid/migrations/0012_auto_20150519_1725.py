# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0011_auto_20150519_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='actividades',
            field=models.ManyToManyField(to='actividades_madrid.Actividad', blank=True),
            preserve_default=True,
        ),
    ]
