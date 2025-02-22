# Generated by Django 4.2.19 on 2025-02-20 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0010_alter_favourites_options_alter_ingredient_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to=settings.AUTH_USER_MODEL, verbose_name='Владелец подписки'),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptionn', to=settings.AUTH_USER_MODEL, verbose_name='Подписка'),
        ),
    ]
