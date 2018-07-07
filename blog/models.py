from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

#2
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset()\
                                           .filter(status='published')
#1
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager() #the default Manager
    published = PublishedManager() #our custom manager

    class Meta:
        ordering = ('-publish',) #sort the results by descending order(- sign)

    def __str__(self):
        return self.title

    def get_absolute_url(self): #we will use get absolute method in templates
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                              self.publish.strftime('%m'),
                              self.publish.strftime('%d'),
                              self.slug])

#for commentng purpose
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class meta:
        ordering = ('created')

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)
