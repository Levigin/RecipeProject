# Generated by Django 4.2.6 on 2023-11-06 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecipesApp', '0004_alter_cookingstep_image_alter_cookingstep_recipe_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='RecipesApp.category', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
