# Generated by Django 2.0.5 on 2018-05-27 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180527_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.CharField(default='', max_length=300),
        ),
    ]
