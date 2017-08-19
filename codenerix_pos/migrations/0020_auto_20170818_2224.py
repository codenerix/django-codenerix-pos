# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-18 22:24
from __future__ import unicode_literals

import uuid
import hashlib

from django.db import migrations, models


def set_keyb_defaults(apps, schema_editor):
    POS = apps.get_model('codenerix_pos', 'POS')
    for pos in POS.objects.all().iterator():
        pos.keyb = hashlib.md5(uuid.uuid4().hex.encode('utf-8')).hexdigest()
        pos.save()


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_pos', '0019_posoperator'),
    ]

    operations = [
        migrations.AddField(
            model_name='pos',
            name='keyb',
            field=models.CharField(default='', max_length=32, verbose_name='Key Broadcast'),
        ),
        migrations.RunPython(set_keyb_defaults),
        migrations.AlterField(
            model_name='pos',
            name='keyb',
            field=models.CharField(default='', unique=True, max_length=32, verbose_name='Key Broadcast'),
        ),
        migrations.AlterField(
            model_name='pos',
            name='hardware',
            field=models.ManyToManyField(blank=True, related_name='poss', to='codenerix_pos.POSHardware', verbose_name='Hardware it can use'),
        ),
        migrations.AlterField(
            model_name='pos',
            name='payments',
            field=models.ManyToManyField(blank=True, related_name='poss', to='codenerix_payments.PaymentRequest', verbose_name='Payments'),
        ),
    ]