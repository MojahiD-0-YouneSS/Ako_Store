# Generated by Django 4.2.7 on 2024-06-23 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_colorsizepointer'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorsizepointer',
            name='product_color',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='product.productcolor'),
            preserve_default=False,
        ),
    ]
