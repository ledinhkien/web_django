# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-21 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_ward'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='userprofile',
        ),
    ]