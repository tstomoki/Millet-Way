# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0005_auto_20150817_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinsight',
            name='user_name',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
