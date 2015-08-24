# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0009_logdata_acc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logdata',
            name='acc_x',
        ),
        migrations.RemoveField(
            model_name='logdata',
            name='acc_y',
        ),
        migrations.RemoveField(
            model_name='logdata',
            name='acc_z',
        ),
    ]
