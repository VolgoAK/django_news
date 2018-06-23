from django.db import models


# Create your models here.
class Post(models.Model):
    body = models.CharField(max_length=3000)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)
    votes = models.IntegerField(default=0)


class Comment(models.Model):
    text = models.CharField(max_length=300)
    author_name = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date_published')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
