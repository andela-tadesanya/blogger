from models import Article, Category
from rest_framework import viewsets
from serializers import ArticleSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows category to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
