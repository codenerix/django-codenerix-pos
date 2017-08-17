# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-26 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_pos', '0012_merge_20170726_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poshardware',
            name='config',
            field=jsonfield.fields.JSONField(blank=True, null=True, verbose_name='config'),
        ),
        migrations.AlterField(
            model_name='posplant',
            name='billing_series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posplants', to='codenerix_invoicing.BillingSeries', verbose_name='Billing series'),
        ),
    ]