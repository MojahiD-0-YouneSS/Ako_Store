# Generated by Django 4.2.7 on 2024-08-10 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0004_remove_userprofile_promo_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopPoster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='poster_shop/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('for_product', models.BooleanField(default=False)),
                ('product_number', models.CharField(max_length=50, null=True)),
                ('redirection_section', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
