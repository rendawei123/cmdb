# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_server_latest_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='os_version',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='系统版本'),
        ),
        migrations.AlterField(
            model_name='server',
            name='sn',
            field=models.CharField(db_index=True, max_length=128, verbose_name='SN号'),
        ),
    ]
