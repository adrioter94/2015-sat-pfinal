# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0015_estilocss'),
    ]

    operations = [
        migrations.AddField(
            model_name='estilocss',
            name='usuario',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
