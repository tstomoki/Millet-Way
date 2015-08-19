# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0006_auto_20150818_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='lat',
            field=models.DecimalField(max_digits=20, decimal_places=17),
        ),
        migrations.AlterField(
            model_name='logdata',
            name='lon',
            field=models.DecimalField(max_digits=20, decimal_places=17),
        ),
    ]
