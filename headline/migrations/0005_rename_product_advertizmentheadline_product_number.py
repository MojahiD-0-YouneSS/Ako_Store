# Generated by Django 4.2.7 on 2024-07-28 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('headline', '0004_advertizmentheadline_for_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertizmentheadline',
            old_name='product',
            new_name='product_number',
        ),
    ]
