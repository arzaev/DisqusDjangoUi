# Generated by Django 2.1.5 on 2019-02-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190221_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='profile',
            field=models.BooleanField(default=False),
        ),
    ]
