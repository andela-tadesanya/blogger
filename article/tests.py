from django.test import TestCase
from models import Article, Category


# Create your tests here.
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
