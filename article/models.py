from django.db import models
from bs4 import BeautifulSoup
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])
