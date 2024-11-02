# Generated by Django 5.1.1 on 2024-10-31 11:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('account_type', models.CharField(choices=[('Job Seeker', 'Job Seeker'), ('Company', 'Company'), ('Admin', 'Admin')], default='Job Seeker', max_length=10)),
                ('salt', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('application_deadline', models.DateField()),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=10)),
                ('applicants', models.ManyToManyField(related_name='applications', to='checkapp.user')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkapp.job')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkapp.user')),
            ],
        ),
    ]