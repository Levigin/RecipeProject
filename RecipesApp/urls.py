from django.urls import path
from RecipesApp.views import *

urlpatterns = [
    path('', main, name='main'),
    path('<int:category_id>/<int:pk>', detail, name='detail'),
    path('<int:pk>/', get_category, name='get_category')
]
