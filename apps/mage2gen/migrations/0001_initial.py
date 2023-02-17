# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4)),
                ('config', jsonfield.fields.JSONField(default={})),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
