# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades_madrid', '0007_remove_usuario_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateFecha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='actividad',
            name='usuario',
        ),
        migrations.AddField(
            model_name='usuario',
            name='usuario',
            field=models.ManyToManyField(to='actividades_madrid.Actividad', blank=True),
            preserve_default=True,
        ),
    ]
