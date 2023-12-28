# Generated by Django 4.2.7 on 2023-12-04 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0016_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_details',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_details',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
