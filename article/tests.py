from django.test import TestCase
from models import Article, Category
from serializers import ArticleSerializer, CategorySerializer


# Test models.
class ArticleModelsTestCase(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="fiction")
        Article.objects.create(
            writer="tosin",
            title="things fall apart",
            content="A very, very, loooong story",
            category=cat,
            image="path/to/img.jpg")

    def tearDown(self):
        pass

    def test_article_is_created_properly(self):
        post = Article.objects.all().first()
        self.assertEqual(post.writer, "tosin")
        self.assertEqual(post.title, "things fall apart")

    def test_category_is_created_properly(self):
        cat = Category.objects.all().first()
        self.assertEqual(cat.name, "fiction")


# Test Serializers.
class ArticleSerializersTestCase(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="fiction")

    def tearDown(self):
        pass

    def test_category_serializer(self):
        data = {'name': 'food'}
        category_serializer = CategorySerializer(data=data)
        self.assertTrue(category_serializer.is_valid())
        category = category_serializer.save()

        self.assertEqual(category.name, data['name'])

    def test_article_serializer(self):
        data = {
            'writer': 'tosin',
            'title': 'how to cook',
            'content': 'boil water',
            'category': self.cat.id,
            'image': 'url/to/image'
        }

        article_serializer = ArticleSerializer(data=data)
        self.assertTrue(article_serializer.is_valid())
        article = article_serializer.save()

        self.assertEqual(article.writer, data['writer'])
        self.assertEqual(article.title, data['title'])
        self.assertEqual(article.content, data['content'])
        self.assertEqual(article.category.id, data['category'])
        self.assertEqual(article.image, data['image'])


# Test views.
class ArticleViewTestCase(TestCase):
    pass
