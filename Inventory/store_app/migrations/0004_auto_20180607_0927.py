# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-07 02:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0003_remove_order_tag'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='Product',
        ),
    ]
