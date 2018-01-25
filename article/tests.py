from django.test import TestCase
from models import Article, Category
from serializers import ArticleSerializer, CategorySerializer
from rest_framework.test import APIClient
from django.contrib.auth.models import User


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
        self.assertEqual(post.content, "A very, very, loooong story")
        self.assertEqual(post.category.name, "fiction")
        self.assertEqual(post.image, "path/to/img.jpg")

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
    def setUp(self):
        self.cat = Category.objects.create(name="fiction")
        Category.objects.create(name="programming")
        Article.objects.create(
            writer="tosin",
            title="things fall apart",
            content="A very, very, loooong story",
            category=self.cat,
            image="path/to/img.jpg")

        # Create a user
        self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.save()

    def tearDown(self):
        pass

    def test_user_can_view_articles_without_logging_in(self):
        client = APIClient()
        response = client.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_post_article_without_logging_in(self):
        client = APIClient()
        payload = {
            'writer': 'tosin',
            'title': 'how to cook',
            'content': 'boil water',
            'category': self.cat.id,
            'image': 'url/to/image'
        }
        response = client.post('/articles/', payload, format='json')
        self.assertEqual(response.status_code, 403)

    def test_user_can_post_articles_when_logged_in(self):
        client = APIClient()
        client.login(username='admin', password='pass')
        payload = {
            'writer': 'tosin',
            'title': 'how to cook',
            'content': 'boil water',
            'category': self.cat.id,
            'image': 'url/to/image'
        }
        response = client.post('/articles/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        client.logout()

    def test_user_can_update_article_when_logged_in(self):
        client = APIClient()
        client.login(username='admin', password='pass')
        payload = {
            'writer': 'john doe',
            'title': 'how to cook',
            'content': 'boil water',
            'category': self.cat.id,
            'image': 'url/to/image'
        }
        article_id = Article.objects.all().first().id
        url = '/articles/{}/'.format(article_id)
        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['writer'], payload['writer'])
        client.logout()

    def test_user_can_delete_article_when_logged_in(self):
        client = APIClient()
        client.login(username='admin', password='pass')

        article_id = Article.objects.all().first().id
        url = '/articles/{}/'.format(article_id)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)
        client.logout()

    def test_user_can_view_category_without_logging_in(self):
        client = APIClient()
        response = client.get('/categories/')
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_post_category_without_logging_in(self):
        client = APIClient()
        payload = {
            'name': 'sports'
        }
        response = client.post('/categories/', payload, format='json')
        self.assertEqual(response.status_code, 403)

    def test_user_can_post_category_when_logged_in(self):
        client = APIClient()
        client.login(username='admin', password='pass')
        payload = {
            'name': 'sports'
        }
        response = client.post('/categories/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        client.logout()

    def test_user_can_update_category_when_logged_in(self):
        client = APIClient()
        client.login(username='admin', password='pass')
        payload = {
            'name': 'non-fiction'
        }
        cat = Category.objects.all().first()
        url = '/categories/{}/'.format(cat.id)
        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'non-fiction')
        client.logout()

    def test_user_can_delete_category_when_logged_in(self):
        client = APIClient()
        client.login(username='admin', password='pass')

        cat = Category.objects.all().first()
        url = '/categories/{}/'.format(cat.id)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)
        client.logout()