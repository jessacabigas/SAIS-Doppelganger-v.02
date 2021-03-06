# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0017_auto_20160529_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Student')),
                ('subject_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Subjects')),
            ],
        ),
    ]
