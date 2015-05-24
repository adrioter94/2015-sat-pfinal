# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.TextField()),
                ('tipo', models.TextField()),
                ('precio', models.IntegerField()),
                ('fecha', models.DateField()),
                ('hora', models.DateTimeField()),
                ('duracion', models.DateTimeField()),
                ('larga_duracion', models.CharField(max_length=32)),
                ('url', models.TextField()),
                ('fecha_seleccion', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='actividad',
            name='usuario',
            field=models.ManyToManyField(to='actividades_madrid.Usuario'),
            preserve_default=True,
        ),
    ]
