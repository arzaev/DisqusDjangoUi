# Generated by Django 2.1.5 on 2019-01-28 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190128_1756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='infomations',
            new_name='infomation',
        ),
    ]