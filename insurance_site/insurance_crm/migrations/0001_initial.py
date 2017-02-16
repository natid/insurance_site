# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 15:31
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
                ('phone_number', models.CharField(max_length=50)),
                ('license_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.TextField(max_length=50000)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=50, null=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='insurance_crm.Agent')),
            ],
        ),
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credentials_file', models.TextField(blank=True, max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mail', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ResponseMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.TextField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identification_number', to='insurance_crm.Client')),
                ('insurance_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='number', to='insurance_crm.InsuranceCompany')),
            ],
        ),
        migrations.CreateModel(
            name='SignedPdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.TextField(max_length=50000)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdf_id', to='insurance_crm.Client')),
            ],
        ),
        migrations.AddField(
            model_name='attachment',
            name='response_mail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment_ids', to='insurance_crm.ResponseMail'),
        ),
    ]
