# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 17:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_auto_20170926_1709'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': 'Участник', 'verbose_name_plural': 'Участники'},
        ),
        migrations.AlterModelTable(
            name='participant',
            table='participant',
        ),
    ]