# Generated by Django 2.0.5 on 2018-05-27 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180520_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='artists',
            field=models.ManyToManyField(blank=True, null=True, to='main.Artist'),
        ),
    ]
