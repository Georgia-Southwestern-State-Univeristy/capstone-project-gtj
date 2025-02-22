# Generated by Django 5.1.6 on 2025-02-22 03:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('transit_website', models.URLField(help_text='Official transit authority website')),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.RemoveField(
            model_name='ride',
            name='airport',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='user',
        ),
        migrations.CreateModel(
            name='TransitLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('line_type', models.CharField(choices=[('METRO', 'Metro/Subway'), ('BUS', 'Bus'), ('TRAM', 'Tram'), ('TRAIN', 'Train'), ('FERRY', 'Ferry'), ('BIKE', 'Bike Share')], max_length=10)),
                ('description', models.TextField()),
                ('schedule_url', models.URLField(help_text='Link to line schedule')),
                ('map_url', models.URLField(help_text='Link to line map')),
                ('operating_hours', models.CharField(max_length=200)),
                ('frequency', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transit_lines', to='transport.city')),
            ],
        ),
        migrations.CreateModel(
            name='TransitPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pass_type', models.CharField(choices=[('DAY', 'Day Pass'), ('WEEK', 'Weekly Pass'), ('MONTH', 'Monthly Pass'), ('SINGLE', 'Single Ride')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('purchase_url', models.URLField(help_text='Where to buy this pass')),
                ('description', models.TextField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transit_passes', to='transport.city')),
            ],
        ),
        migrations.CreateModel(
            name='TransitStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('accessibility', models.BooleanField(default=True)),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='transport.transitline')),
            ],
        ),
        migrations.DeleteModel(
            name='Airport',
        ),
        migrations.DeleteModel(
            name='Ride',
        ),
    ]
