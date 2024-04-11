# Generated by Django 5.0.1 on 2024-04-11 08:37

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_product_description_alter_product_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_time',
            field=django_jalali.db.models.jDateField(blank=True, default=datetime.date(2024, 4, 11), null=True, verbose_name='تاریخ ثبت محصول'),
        ),
    ]
