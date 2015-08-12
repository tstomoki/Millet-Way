# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.DecimalField(max_digits=12, decimal_places=9)),
                ('lon', models.DecimalField(max_digits=12, decimal_places=9)),
                ('acc_x', models.DecimalField(max_digits=7, decimal_places=3)),
                ('acc_y', models.DecimalField(max_digits=7, decimal_places=3)),
                ('acc_z', models.DecimalField(max_digits=7, decimal_places=3)),
                ('logged_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='logdata',
            name='user',
            field=models.ForeignKey(to='bump_hunter.User'),
        ),
    ]
