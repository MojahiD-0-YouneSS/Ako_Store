# Generated by Django 4.2.7 on 2024-08-17 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_productmodel_reviews_delete_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandmodel',
            name='brand_Image',
            field=models.ImageField(blank=True, null=True, upload_to='brand/'),
        ),
    ]
