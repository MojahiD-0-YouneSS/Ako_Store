# Generated by Django 4.2.7 on 2024-06-22 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_color_siz_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColorSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('product_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productcolor')),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productsize')),
            ],
        ),
        migrations.DeleteModel(
            name='Product_Color_Siz',
        ),
    ]
