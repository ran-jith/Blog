from django import template
from django.db.models import Count

#create a simple tag to retrieve total posts published in the blog
register = template.Library()

from ..models import Post

@register.simple_tag #or @register.simple_tag(name='my_tag')
def total_posts():
    return Post.published.count()#return No.Of  posts published so far

#a tag to display latest posts
#in template tag we can use like this ({% show_latest_posts 3 %})
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

#assingment tag to display most commented posts
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
