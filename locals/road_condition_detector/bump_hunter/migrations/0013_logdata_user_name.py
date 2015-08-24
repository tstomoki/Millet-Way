# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0012_auto_20150824_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='logdata',
            name='user_name',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
