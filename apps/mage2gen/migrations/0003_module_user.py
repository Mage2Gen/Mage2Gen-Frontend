# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mage2gen', '0002_auto_20160622_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='user',
            field=models.ForeignKey(related_name='modules', blank=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
