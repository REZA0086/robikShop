# Generated by Django 5.0.1 on 2024-04-08 15:08

import datetime
import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='دسته بندی')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='category/', verbose_name='عکس دسته بندی')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/', verbose_name='عکس محصول')),
                ('name', models.CharField(max_length=250, verbose_name='نام محصول')),
                ('price', models.DecimalField(decimal_places=0, max_digits=11, verbose_name='قیمت')),
                ('discount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='تخفیف')),
                ('created_time', django_jalali.db.models.jDateField(blank=True, default=datetime.date(2024, 4, 8), null=True, verbose_name='تاریخ ثبت محصول')),
                ('order_count', models.IntegerField(default=0, verbose_name='تعداد فروش')),
                ('visited_count', models.IntegerField(default=0, verbose_name='تعداد بازدید')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='دسته بندی محصول')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='عکس محصول')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product', verbose_name=' محصول')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=250, null=True, verbose_name='مقدار ویژگی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product', verbose_name='ویژگی محصول')),
            ],
        ),
    ]