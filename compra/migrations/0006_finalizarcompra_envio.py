# Generated by Django 2.2.2 on 2019-09-18 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Adicionales', '0001_initial_manual'),
        ('compra', '0005_auto_20190915_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalizarcompra',
            name='Envio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Adicionales.Envio'),
        ),
    ]