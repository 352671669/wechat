# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin_core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='BkWeixinUser',
            old_name='openid',
            new_name='userid',
        ),
        migrations.RenameField(
            model_name='BkWeixinUser',
            old_name='nickname',
            new_name='name',
        ),
    ]
