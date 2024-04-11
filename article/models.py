from django.db import models
from bs4 import BeautifulSoup


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
