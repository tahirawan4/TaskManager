# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-09 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
