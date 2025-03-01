# Generated by Django 5.1.6 on 2025-03-01 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safety', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountrySafety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=2)),
                ('capital', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('overall_safety_score', models.IntegerField(default=0)),
                ('women_safety_score', models.IntegerField(default=0)),
                ('night_safety_score', models.IntegerField(default=0)),
                ('crime_score', models.IntegerField(default=0)),
                ('safety_summary', models.TextField(blank=True)),
                ('women_safety_info', models.TextField(blank=True)),
                ('night_safety_info', models.TextField(blank=True)),
                ('solo_traveler_info', models.TextField(blank=True)),
                ('crime_info', models.TextField(blank=True)),
                ('transportation_safety_info', models.TextField(blank=True)),
                ('emergency_numbers', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
