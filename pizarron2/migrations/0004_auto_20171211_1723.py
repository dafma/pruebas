# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-11 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizarron2', '0003_auto_20171211_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencia',
            name='CBM',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='referencia',
            name='KG',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
    ]
