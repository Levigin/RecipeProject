from django.urls import path
from api.views import recipes, RecipeDetailView, comment


urlpatterns = [
    path('recipes/', recipes),
    path('recipes/<int:pk>', RecipeDetailView.as_view()),
    path('recipes/<int:pk>/comments/', comment)
]