# Generated by Django 4.2.6 on 2023-11-06 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecipesApp', '0006_alter_category_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='recipe',
        ),
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='RecipesApp.category', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
