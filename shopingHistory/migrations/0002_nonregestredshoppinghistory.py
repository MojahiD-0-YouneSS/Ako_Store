# Generated by Django 4.2.7 on 2024-08-08 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_client_email'),
        ('order', '0002_nonregestredorder_nonregestredorderitem_and_more'),
        ('shopingHistory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonRegestredShoppingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.ManyToManyField(to='order.nonregestredorder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.nonregesteredclient')),
            ],
        ),
    ]
