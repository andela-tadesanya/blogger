from models import Article, Category
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(required=False, allow_null=True)

    class Meta:
        model = Article
        fields = ('writer', 'title', 'content', 'category', 'image')
