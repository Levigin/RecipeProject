from django.core.validators import MinValueValidator
from django.db import models
from UserApp.models import Chef
from RecipesApp.utilities import upload_path_recipe, upload_path_step_cooking
from RecipesApp.utilities import send_new_comment_notification
from django.db.models.signals import post_save


class Recipe(models.Model):
    title = models.CharField(verbose_name='Название', max_length=64)
    description = models.TextField(verbose_name='Описание', max_length=512)
    image = models.ImageField(verbose_name='Изображение', upload_to=upload_path_recipe, blank=True)
    cooking_time = models.IntegerField(verbose_name='Время приготовления', validators=[MinValueValidator(1)])
    step = models.IntegerField(verbose_name='Количество шагов', validators=[MinValueValidator(1)], default=1)
    ingredient_quantity = models.IntegerField(verbose_name='Количество ингредиентов', validators=[MinValueValidator(
        1)], default=1)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    author = models.ForeignKey(Chef, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.PROTECT)
    is_active = models.BooleanField(verbose_name='Выводить?', default=True)

    def __str__(self):
        return f'{self.title}'

    def delete(self, *args, **kwargs):
        for cs in self.cookingstep_set.all():
            cs.delete()
        for i in self.ingredients_set.all():
            i.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']


class CookingStep(models.Model):
    step = models.CharField(verbose_name='Шаг', max_length=32)
    description = models.TextField(verbose_name='Описание', max_length=512)
    image = models.ImageField(verbose_name='Изображение', upload_to=upload_path_step_cooking, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.step}'

    class Meta:
        verbose_name = 'Шаг рецепта'
        verbose_name_plural = 'Шаги рецепта'


class Ingredients(models.Model):
    title = models.CharField(verbose_name='Название', max_length=64)
    quantity = models.CharField(verbose_name='Количество', max_length=64)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=64)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепты')
    author = models.CharField(max_length=128, verbose_name='Автор')
    content = models.TextField(verbose_name='Текст комментария')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].recipe.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])


post_save.connect(post_save_dispatcher, sender=Comment)
