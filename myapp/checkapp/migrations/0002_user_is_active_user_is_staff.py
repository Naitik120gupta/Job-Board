# Generated by Django 5.1.1 on 2024-11-01 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
