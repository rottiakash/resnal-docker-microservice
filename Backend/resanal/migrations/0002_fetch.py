# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-28 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resanal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fetch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcode', models.CharField(max_length=10)),
                ('subname', models.CharField(max_length=100)),
                ('intmarks', models.IntegerField()),
                ('extmarks', models.IntegerField()),
                ('totalmarks', models.IntegerField()),
                ('initial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resanal.Result')),
            ],
        ),
    ]
