from django.http import HttpRequest
from django.shortcuts import render
from api.serializers import RecipeSerializer, RecipeDetailSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from RecipesApp.models import Recipe, Comment
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@api_view(['GET'])
def recipes(request: HttpRequest):
    if request.method == 'GET':
        recipes = Recipe.objects.filter(is_active=True)[:10]
        serializers = RecipeSerializer(recipes, many=True)
        return Response(serializers.data)


class RecipeDetailView(RetrieveAPIView):
    queryset = Recipe.objects.filter(is_active=True)
    serializer_class = RecipeDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def comment(request: HttpRequest, pk: int):
    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, recipe=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
