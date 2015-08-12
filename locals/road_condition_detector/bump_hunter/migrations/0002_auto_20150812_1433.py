# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='logged_at',
            field=models.DateTimeField(),
        ),
    ]
