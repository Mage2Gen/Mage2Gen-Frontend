# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('license_short_text', models.TextField(default='')),
                ('license_text', models.TextField(default='')),
                ('user', models.ForeignKey(related_name='licenses', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
