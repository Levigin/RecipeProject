from django.contrib import admin
from RecipesApp.models import *


class CategoryAdmin(admin.ModelAdmin):
    model = Category


class CookingStepInline(admin.StackedInline):
    model = CookingStep
    can_delete = False


class IngredientsInline(admin.StackedInline):
    model = Ingredients
    can_delete = False


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInline, CookingStepInline)
    list_display = ('title', 'description', 'author', 'created_at', )
    readonly_fields = ['created_at']
    ordering = ['-created_at']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)

