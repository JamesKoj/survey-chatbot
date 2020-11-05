from django.db import models


# Create your models here.
class Post(models.Model):
    qid = models.CharField(max_length=5)
    user_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qid