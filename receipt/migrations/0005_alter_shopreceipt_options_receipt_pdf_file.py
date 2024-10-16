# Generated by Django 4.2.7 on 2024-08-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0004_rename_id_receipt_receipt_reference_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopreceipt',
            options={'verbose_name': 'Shop Receipt', 'verbose_name_plural': 'Shop Receipts'},
        ),
        migrations.AddField(
            model_name='receipt',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='receipt_pdf/'),
        ),
    ]
