# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mage2gen', '0003_module_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='download_count',
            field=models.IntegerField(default=0),
        ),
    ]
