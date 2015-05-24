# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0003_auto_20150515_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='precio',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
    ]
