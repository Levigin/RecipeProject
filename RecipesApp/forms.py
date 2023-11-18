from django import forms
from RecipesApp.models import Category, Comment
from captcha.fields import CaptchaField


class CategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', required=True)

    class Meta:
        model = Category
        fields = ('title',)


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, label='', max_length=20)


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'recipe': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'recipe': forms.HiddenInput}
