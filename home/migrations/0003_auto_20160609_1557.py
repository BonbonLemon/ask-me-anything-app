# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 22:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160609_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='ama',
            name='title',
            field=models.CharField(default='placeholder', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ama',
            name='description_text',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='ama',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=400),
        ),
    ]
