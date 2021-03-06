# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 15:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=50, verbose_name='标题')),
                ('text', models.TextField(verbose_name='编辑文档')),
                ('save_time', models.DateTimeField(auto_now=True)),
                ('local_article', models.FileField(blank=True, null=True, upload_to='localArt', verbose_name='上传本地文档')),
                ('is_write', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.FileField(blank=True, null=True, upload_to='avatar', verbose_name='头像')),
                ('email_address', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('nickname', models.CharField(max_length=25, verbose_name='昵称')),
                ('belong_to', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ManyToManyField(related_name='article_author', to='sanliuyunapp.Person'),
        ),
    ]
