# Generated by Django 4.2.7 on 2024-08-08 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_client_email'),
        ('product', '0013_brandmodel_productmodel_search_labls_productbrand_and_more'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonRegestredOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='NonRegestredOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.nonregestredorder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productmodel')),
            ],
        ),
        migrations.AddField(
            model_name='nonregestredorder',
            name='products',
            field=models.ManyToManyField(through='order.NonRegestredOrderItem', to='product.productmodel'),
        ),
        migrations.AddField(
            model_name='nonregestredorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.nonregesteredclient'),
        ),
    ]
