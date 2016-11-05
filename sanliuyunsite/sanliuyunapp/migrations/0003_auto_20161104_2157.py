# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-04 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanliuyunapp', '0002_article_font_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='font_size',
            field=models.IntegerField(choices=[(3, 3), (5, 5), (8, 8), (20, 20)], default=5),
        ),
    ]