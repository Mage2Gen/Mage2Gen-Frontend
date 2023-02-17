# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mage2gen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='name',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='module',
            name='package_name',
            field=models.CharField(default='', max_length=128),
        ),
    ]
