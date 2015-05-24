# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0009_auto_20150519_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario',
            new_name='actividades',
        ),
    ]
