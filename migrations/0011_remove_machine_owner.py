# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 12:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('machine_manager', '0010_auto_20161020_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='owner',
        ),
    ]
