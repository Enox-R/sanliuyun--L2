# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-04 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanliuyunapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='font_size',
            field=models.IntegerField(default=5),
        ),
    ]
