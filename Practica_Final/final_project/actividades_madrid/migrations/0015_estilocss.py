# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0014_auto_20150520_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstiloCss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner', models.TextField(blank=True)),
                ('login', models.TextField(blank=True)),
                ('menu', models.TextField(blank=True)),
                ('pie', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
