# Generated by Django 5.1.6 on 2025-03-02 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safety', '0003_remove_countrysafety_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrysafety',
            name='code',
            field=models.CharField(max_length=2),
        ),
    ]
