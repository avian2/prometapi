# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-08 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prometapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cameras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('json_data', models.TextField(blank=True, null=True)),
                ('original_data', models.TextField()),
            ],
        ),
    ]