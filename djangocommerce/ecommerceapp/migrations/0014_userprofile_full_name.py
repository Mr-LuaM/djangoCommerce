# Generated by Django 4.2.7 on 2023-12-04 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0013_userprofile_alter_cart_user_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]
