from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    writer = models.CharField(max_length=100)
    title = models.CharField(max_length=25)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    image = models.CharField(max_length=50)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
