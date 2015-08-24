# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bump_hunter.models


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0013_logdata_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinsight',
            name='image',
            field=models.FileField(default=None, upload_to=bump_hunter.models.get_upload_path),
        ),
    ]
