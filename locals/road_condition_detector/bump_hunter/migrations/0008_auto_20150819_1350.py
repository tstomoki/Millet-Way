# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0007_auto_20150819_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='lat',
            field=models.DecimalField(max_digits=12, decimal_places=9),
        ),
        migrations.AlterField(
            model_name='logdata',
            name='lon',
            field=models.DecimalField(max_digits=12, decimal_places=9),
        ),
        migrations.AlterField(
            model_name='userinsight',
            name='lat',
            field=models.DecimalField(max_digits=20, decimal_places=17),
        ),
        migrations.AlterField(
            model_name='userinsight',
            name='lon',
            field=models.DecimalField(max_digits=20, decimal_places=17),
        ),
    ]
