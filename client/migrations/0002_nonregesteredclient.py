# Generated by Django 5.0.4 on 2024-04-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonRegesteredClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'NonRegesteredClient',
                'verbose_name_plural': 'NonRegesteredClients',
            },
        ),
    ]
