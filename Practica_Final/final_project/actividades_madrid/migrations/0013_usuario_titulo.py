# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0012_auto_20150519_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='titulo',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
