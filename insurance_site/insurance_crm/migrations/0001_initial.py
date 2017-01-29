# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 11:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(max_length=50)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='insurance_crm.Agent')),
            ],
        ),
    ]
