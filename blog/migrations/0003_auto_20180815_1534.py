# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-15 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180815_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleupdown',
            name='comment_count',
        ),
        migrations.RemoveField(
            model_name='articleupdown',
            name='down_count',
        ),
        migrations.RemoveField(
            model_name='articleupdown',
            name='up_count',
        ),
        migrations.AddField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='down_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='up_count',
            field=models.IntegerField(default=0),
        ),
    ]
