# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-18 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrest', '0002_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('blood_type', models.CharField(max_length=2)),
                ('rhesus_factor', models.CharField(max_length=5)),
                ('gender', models.CharField(max_length=10)),
                ('first_time_donor', models.CharField(max_length=5)),
                ('age', models.IntegerField()),
                ('current_location', models.IntegerField()),
            ],
        ),
    ]