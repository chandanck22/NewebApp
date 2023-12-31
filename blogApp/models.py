from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        name = str(self.first_name)
        if self.last_name:
            name += ' ' + str(self.last_name)
        return name

class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')

    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='article', default='placeholder.png')
    body = RichTextUploadingField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    slug = models.SlugField(max_length=200, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=options, default='draft')

    objects = models.Manager()
    articlemanager = ArticleManager()

    def get_absolute_url(self):
        return reverse('blogApp:article', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.headline