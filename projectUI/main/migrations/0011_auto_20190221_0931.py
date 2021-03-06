# Generated by Django 2.1.5 on 2019-02-21 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cookie',
            field=models.TextField(default='-'),
        ),
        migrations.AddField(
            model_name='item',
            name='email',
            field=models.CharField(default='-', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='login',
            field=models.CharField(default='-', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='password',
            field=models.CharField(default='-', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='user_agent',
            field=models.TextField(default='-'),
        ),
    ]
