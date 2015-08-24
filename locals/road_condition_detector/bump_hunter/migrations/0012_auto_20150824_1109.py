# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0011_userinsight_insight_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='logdata',
            name='log_type',
            field=models.CharField(default=b'Roadway', max_length=20, choices=[(b'roadway', b'Roadway'), (b'sidewalk', b'Sidewalk')]),
        ),
        migrations.AlterField(
            model_name='userinsight',
            name='insight_type',
            field=models.CharField(default=b'Roadway', max_length=20, choices=[(b'roadway', b'Roadway'), (b'sidewalk', b'Sidewalk')]),
        ),
    ]
