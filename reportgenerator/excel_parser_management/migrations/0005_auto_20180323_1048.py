# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 10:48
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_parser_management', '0004_auto_20180323_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exceljobs',
            name='document',
            field=models.FileField(upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx'])]),
        ),
    ]
