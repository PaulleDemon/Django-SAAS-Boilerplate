from django.db import models
from django.template.defaultfilters import slugify

from user.models import User
from utils.common import generate_uniqueid


def generate_id():
    # table =  apps.get_model('blog', 'Blog')
    return generate_uniqueid(Blog, 'blog_id')


class Blog(models.Model):

    blog_id = models.CharField(max_length=20, unique=True, blank=True, default=generate_id)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    thumbnail = models.ImageField(null=True, blank=True, upload_to='blogs/')

    slug = models.SlugField(blank=True, unique=True)

    title = models.CharField(max_length=200, default="", unique=True)  
    body = models.TextField(null=True, blank=True)

    draft = models.BooleanField(default=True, blank=True)
    datetime = models.DateTimeField(auto_now=True) # stays at last updated

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class BlogImage(models.Model):

    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/')

    def __str__(self) -> str:
        return f'{self.image.url}'