# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-30 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20, unique=True)),
                ('upwd', models.CharField(max_length=20)),
            ],
        ),
    ]
