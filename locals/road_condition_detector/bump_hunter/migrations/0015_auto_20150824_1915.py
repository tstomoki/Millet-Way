# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bump_hunter.models


class Migration(migrations.Migration):

    dependencies = [
        ('bump_hunter', '0014_userinsight_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinsight',
            name='image',
            field=models.FileField(default=b'', upload_to=bump_hunter.models.get_upload_path),
        ),
    ]
