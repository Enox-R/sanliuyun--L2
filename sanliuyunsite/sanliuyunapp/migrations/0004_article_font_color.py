# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-04 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanliuyunapp', '0003_auto_20161104_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='font_color',
            field=models.CharField(choices=[('black', 'black'), ('red', 'red'), ('green', 'green'), ('blue', 'blue'), ('yellow', 'yellow')], default='black', max_length=20),
        ),
    ]
