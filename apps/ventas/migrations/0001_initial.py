# Generated by Django 2.1.5 on 2019-01-21 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articulos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('id_articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articulos.Articulo')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateField()),
                ('estado', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='detalle',
            name='id_venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Venta'),
        ),
    ]