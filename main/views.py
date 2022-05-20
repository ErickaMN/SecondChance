from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Post, PostImage
from .serializer import PostSerializer, PostImageSerializer
from .serializer import CategorySerializer
# Create your views here.

# @api_view(['GET'])
# def categories(request):
#     categories =  Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response (serializer.data)
#
# class PostListView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         post = request.data
#         serializer = PostSerializer (data=post)
#         if serializer.is_valid(raise_exception=True):
#             post_saved = serializer.save()
#             return Response(serializer.data)
#
#
class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class = CategorySerializer

# class PostView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostDetailView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostUpdateView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostDeleteView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
