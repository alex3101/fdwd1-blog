from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

# Create your models here.
# create class for Post

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Post(TimeStampedModel):
    STATUSES = (
        (0, 'Draft'),
        (1, 'Published'),
    )

    title = models.CharField(max_length=200)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts', blank=True, null=True)

    def __str__(self):
        return self.title


    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)
