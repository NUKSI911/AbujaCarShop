# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-02 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=b'abc'),
        ),
    ]
