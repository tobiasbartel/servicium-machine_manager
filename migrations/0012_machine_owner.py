# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact_manager', '0009_contactoptions_human_string'),
        ('machine_manager', '0011_remove_machine_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_of_machine', to='contact_manager.Contact'),
        ),
    ]
