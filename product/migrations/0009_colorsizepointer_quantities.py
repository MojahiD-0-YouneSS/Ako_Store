# Generated by Django 4.2.7 on 2024-06-23 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_colorsizepointer_product_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorsizepointer',
            name='quantities',
            field=models.IntegerField(default=0),
        ),
    ]
