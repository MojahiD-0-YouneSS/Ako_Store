# Generated by Django 4.2.7 on 2024-08-08 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_brandmodel_productmodel_search_labls_productbrand_and_more'),
        ('cart', '0004_cartitem_color_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='temprarycartcartitem',
            name='color_size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productcolorsize'),
        ),
    ]
