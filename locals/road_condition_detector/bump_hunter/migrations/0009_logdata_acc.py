# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0008_auto_20150819_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='logdata',
            name='acc',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=3),
            preserve_default=False,
        ),
    ]
