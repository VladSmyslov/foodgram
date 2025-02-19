# Generated by Django 4.2.16 on 2025-01-12 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='ingredientsrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_list', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipe_images', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.tag'),
        ),
    ]
