# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0013_usuario_titulo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='titulo',
            new_name='titulo_personal',
        ),
    ]
