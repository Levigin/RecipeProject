from django.contrib.auth import password_validation
from django import forms
from django.core.exceptions import ValidationError
from UserApp.apps import user_registered
from RecipesApp.models import Recipe
from UserApp.models import Chef


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = Chef
        fields = ('username', 'email', 'last_name', 'first_name', 'send_messages')


class RegisterChefForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=' '.join(password_validation.password_validators_help_texts()))
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_activated = False
        user.is_active = False
        if commit:
            user.save()
        user_registered.send(RegisterChefForm, instance=user)
        return user

    class Meta:
        model = Chef
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages')


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}
