from django.conf.urls import url
from .import views

urlpatterns = [
    #post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
#desc of above urlpatterns==>
#year requirs 4 digit ,simlry month and day
#posts can be composed with words and hyphens        

]
