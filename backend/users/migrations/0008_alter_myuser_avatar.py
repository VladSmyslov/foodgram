# Generated by Django 4.2.16 on 2025-01-14 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_myuser_is_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, default=None, upload_to='users_images', verbose_name='Аватар'),
        ),
    ]
