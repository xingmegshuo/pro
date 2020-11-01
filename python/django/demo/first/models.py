from django.db import models


# Create your models here.

class Article(models.Model):
    title = models.TextField()
    content_url = models.URLField()
    p_date = models.DateField()
    read_num = models.IntegerField()
    like_num = models.IntegerField()
    comment_num = models.IntegerField()
    reward_num = models.IntegerField()
    author = models.TextField()
    source_url = models.URLField()
    content = models.TextField()


class login(models.Model):
    account = models.CharField(max_length=50)
    password = models.CharField(max_length=50)