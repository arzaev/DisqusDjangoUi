# Generated by Django 2.1.5 on 2019-02-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20190221_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='storage_base',
            field=models.TextField(default='-'),
        ),
    ]
