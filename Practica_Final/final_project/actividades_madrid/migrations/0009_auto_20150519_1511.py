# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0008_auto_20150519_1507'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UpdateFecha',
            new_name='UltimaFecha',
        ),
    ]
