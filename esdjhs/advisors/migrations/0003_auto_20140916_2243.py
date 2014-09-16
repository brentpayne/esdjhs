# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advisors', '0002_auto_20140911_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
