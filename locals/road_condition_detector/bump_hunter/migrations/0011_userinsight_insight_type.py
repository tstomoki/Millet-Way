# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0010_auto_20150824_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinsight',
            name='insight_type',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
