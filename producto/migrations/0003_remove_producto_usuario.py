# Generated by Django 2.2.2 on 2019-07-25 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_auto_20190725_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='usuario',
        ),
    ]
