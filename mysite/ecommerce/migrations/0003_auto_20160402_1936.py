# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-02 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20160402_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrinho',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Usuario'),
            preserve_default=False,
        ),
    ]