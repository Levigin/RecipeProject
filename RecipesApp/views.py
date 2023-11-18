from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from RecipesApp.models import Recipe, Category, Comment
from RecipesApp.forms import SearchForm, GuestCommentForm, UserCommentForm


def main(request: HttpRequest):
    categories = Category.objects.all()
    recipes = Recipe.objects.filter(is_active=True)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(description__icontains=keyword)
        recipes = recipes.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(recipes, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'page': page, 'recipes': page.object_list, 'form': form, 'categories': categories}
    return render(request, 'RecipesApp/index.html', context)


def detail(request: HttpRequest, category_id: int, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    cooking_steps = recipe.cookingstep_set.all()
    ingredients = recipe.ingredients_set.all()
    comments = Comment.objects.filter(is_active=True, recipe=pk)
    initial = {'recipe': recipe.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_user = UserCommentForm
    else:
        form_user = GuestCommentForm
    form = form_user(initial=initial)
    if request.method == 'POST':
        c_form = form_user(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
    context = {
        'recipe': recipe,
        'cooking_steps': cooking_steps,
        'ingredients': ingredients,
        'comments': comments,
        'form': form
    }
    return render(request, 'RecipesApp/detail.html', context)


def get_category(request: HttpRequest, pk):
    category = get_object_or_404(Category, pk=pk)
    recipes = Recipe.objects.filter(is_active=True, category=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(description__icontains=keyword)
        recipes = recipes.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(recipes, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'category': category, 'page': page, 'recipes': page.object_list, 'form': form}
    return render(request, 'RecipesApp/by_category.html', context)


