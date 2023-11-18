from django.urls import path
from UserApp.views import *

urlpatterns = [
    path('accounts/login/', ChefLoginView.as_view(), name='login'),
    path('accounts/logout/', ChefLogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/password/change/', ChefChangePasswordView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteChefView.as_view(), name='delete'),
    path('accounts/register/', RegisterChefView.as_view(), name='register'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/add/', add_recipe_profile, name='add_recipe_profile'),
    path('accounts/profile/add/ingredients/<int:pk>/', add_ingredient_profile, name='add_ingredient_profile'),
    path('accounts/profile/add/<int:pk>/cooking_steps/', add_cooking_step_profile, name='add_cooking_step_profile'),
    path('accounts/profile/recipe/change/<int:pk>', change_profile_recipe, name='change_profile_recipe'),
    path('accounts/profile/recipe/delete/<int:pk>', delete_profile_recipe, name='delete_profile_recipe'),
    path('accounts/profile/recipe/<int:pk>', profile_recipe_detail, name='profile_recipe_detail'),
]

