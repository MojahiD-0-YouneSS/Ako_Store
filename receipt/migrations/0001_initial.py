# Generated by Django 5.0.4 on 2024-04-27 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('expiredateValue', models.IntegerField(default=5)),
                ('downlowdedReceipts', models.IntegerField(default=0)),
                ('expireedReceipts', models.IntegerField(default=0)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Receipt',
                'verbose_name_plural': 'Receipts',
            },
        ),
        migrations.CreateModel(
            name='ReceiptID',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptCollector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipt.receipt')),
                ('id_collection', models.ManyToManyField(to='receipt.receiptid')),
            ],
        ),
    ]
