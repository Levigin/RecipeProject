from django.contrib.auth import logout
from django.core.signing import BadSignature
from django.forms import inlineformset_factory
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from UserApp.utilities import signer
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from UserApp.models import Chef
from UserApp.forms import ChangeUserInfoForm, RegisterChefForm, RecipeForm
from django.contrib import messages
from RecipesApp.models import Recipe, Ingredients, CookingStep


class ChefLoginView(LoginView):
    template_name = 'UserApp/login.html'


@login_required
def add_recipe_profile(request: HttpRequest):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save()
            messages.add_message(request, messages.SUCCESS, 'Рецепт добавлен')
            url_redirect = reverse('add_ingredient_profile', kwargs={'pk': recipe.pk})
            return redirect(url_redirect)
    else:
        form = RecipeForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'UserApp/add_recipe_profile.html', context)


@login_required
def add_ingredient_profile(request: HttpRequest, pk: int):
    recipe = Recipe.objects.filter(pk=pk).first()
    IngredientsFormSet = inlineformset_factory(Recipe, Ingredients, fields='__all__', extra=recipe.ingredient_quantity)
    if request.method == 'POST':
        formset_ingredients = IngredientsFormSet(request.POST, instance=recipe)
        if formset_ingredients.is_valid():
            formset_ingredients.save()
            messages.add_message(request, messages.SUCCESS, 'Ингредиенты добавлены')
            url_redirect = reverse(add_cooking_step_profile, kwargs={'pk': recipe.pk})
            return redirect(url_redirect)
        else:
            messages.add_message(request, messages.WARNING, 'Поля заполнены не правильно')
    else:
        formset_ingredients = IngredientsFormSet()
    context = {'formset_ingredients': formset_ingredients, 'recipe': recipe}
    return render(request, 'UserApp/add_ingredient_profile.html', context)


@login_required
def add_cooking_step_profile(request: HttpRequest, pk: int):
    recipe = Recipe.objects.filter(pk=pk).first()
    CookingStepFormSet = inlineformset_factory(Recipe, CookingStep, fields='__all__', extra=recipe.step)
    if request.method == 'POST':
        formset_cooking_step = CookingStepFormSet(request.POST, instance=recipe)
        if formset_cooking_step.is_valid():
            formset_cooking_step.save()
            messages.add_message(request, messages.SUCCESS, 'Шаги приготовления добавлены!')
            return redirect('profile')
        else:
            messages.add_message(request, messages.WARNING, 'Некорректно введенные данные')
    else:
        formset_cooking_step = CookingStepFormSet()
    context = {'formset_cooking_step': formset_cooking_step, 'recipe': recipe}
    return render(request, 'UserApp/add_cooking_step_profile.html', context)


@login_required
def change_profile_recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    CookingStepFormSet = inlineformset_factory(Recipe, CookingStep, fields='__all__')
    IngredientsFormSet = inlineformset_factory(Recipe, Ingredients, fields='__all__')
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            formset_ingredients = IngredientsFormSet(request.POST, instance=recipe)
            formset_cooking_step = CookingStepFormSet(request.POST, request.FILES, instance=recipe)
            if formset_ingredients.is_valid() and formset_cooking_step.is_valid():
                formset_ingredients.save()
                formset_cooking_step.save()
                messages.add_message(request, messages.SUCCESS, 'Рецепт изменен')
                return redirect('profile')
    else:
        form = RecipeForm(instance=recipe)
        formset_ingredients = IngredientsFormSet(instance=recipe)
        formset_cooking_step = CookingStepFormSet(instance=recipe)
    context = {'formset_cooking_step': formset_cooking_step, 'formset_ingredients': formset_ingredients, 'form': form}
    return render(request, 'UserApp/change_profile_recipe.html', context)


@login_required
def delete_profile_recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        messages.add_message(request, messages.SUCCESS, 'Рецепт удален')
        return redirect('profile')
    else:
        context = {'recipe': recipe}
        return render(request, 'UserApp/delete_profile_recipe.html', context)


@login_required
def profile(request: HttpRequest):
    recipes = Recipe.objects.filter(author=request.user.pk)
    context = {'recipes': recipes}
    return render(request, 'UserApp/profile.html', context)


@login_required
def profile_recipe_detail(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    cooking_steps = recipe.cookingstep_set.all()
    ingredients = recipe.ingredients_set.all()
    context = {'recipe': recipe, 'cooking_steps': cooking_steps, 'ingredients': ingredients}
    return render(request, 'UserApp/profile_recipe_detail.html', context)


class ChefLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'UserApp/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Chef
    template_name = 'UserApp/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователя успешно изменены'

    def setup(self, request: HttpRequest, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChefChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'UserApp/change_password.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль был успешно изменен'


class RegisterChefView(CreateView):
    model = Chef
    template_name = 'UserApp/register.html'
    form_class = RegisterChefForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'UserApp/register_done.html'


def user_activate(request: HttpRequest, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'UserApp/bad_signature.html')
    user = get_object_or_404(Chef, username=username)
    if user.is_activated:
        template = 'UserApp/user_is_activated.html'
    else:
        template = 'UserApp/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteChefView(LoginRequiredMixin, DeleteView):
    model = Chef
    template_name = 'UserApp/delete_user.html'
    success_url = reverse_lazy('main')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

