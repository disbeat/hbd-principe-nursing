# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-19 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nursing', '0002_visit_nurse'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='nursing.Department'),
        ),
    ]
