from django.db import models

# Create your models here.
from django.db import models
class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200,null=True)
    author=models.CharField(max_length=50)
    chapter = models.TextField()
    pub_date = models.DateTimeField()
    content = models.TextField()
    

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
