from django.conf.urls import url
from .import views
from .feeds import LatestPostFeed

urlpatterns = [
    #post views

    url(r'^$', views.post_list, name='post_list'),
    #url(r'^$', views.PostListView.as_view(), name = 'post_list'), #url for class based view
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
#desc of above urlpatterns==>
#year requirs 4 digit ,simlry month and day
#posts can be composed with words and hyphens
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),

    #for tags
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'), #this will call view with a slug parameter

    url(r'^feed/$', LatestPostFeed(), name='post_feed'),

    url(r'^search/$', views.post_search, name='post_search'),

]
