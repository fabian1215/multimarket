# Generated by Django 2.2.2 on 2019-09-16 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0007_auto_20190914_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='Descripcion',
            field=models.TextField(),
        ),
    ]
