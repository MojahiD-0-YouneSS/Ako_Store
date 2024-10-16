# Generated by Django 4.2.7 on 2024-08-21 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_brandmodel_brand_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='FabricModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'FabricModel',
                'verbose_name_plural': 'FabricModels',
            },
        ),
        migrations.CreateModel(
            name='ProductFabric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pure', models.BooleanField(default=True)),
                ('fabric', models.CharField(max_length=100, unique=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productmodel')),
            ],
        ),
    ]
