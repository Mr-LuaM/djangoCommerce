# Generated by Django 4.2.7 on 2023-12-14 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0020_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_images/'),
        ),
    ]
