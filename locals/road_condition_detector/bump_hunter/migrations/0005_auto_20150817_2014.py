# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0004_userinsight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinsight',
            name='user',
        ),
        migrations.AddField(
            model_name='userinsight',
            name='user_name',
            field=models.CharField(default=b'John Doe', max_length=200),
        ),
    ]
