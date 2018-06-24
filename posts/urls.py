from django.conf.urls import url

from posts import views
from posts.token import CustomAuthToken

urlpatterns = [
    url(r'^posts/$', views.posts),
    url(r'^private/$', views.private_posts),
    url(r'^posts/(?P<id>[0-9]+)$', views.post_by_id),
    url(r'^vote/$', views.add_claps),
    url(r'^comments/(?P<id>[0-9]+)$', views.comments),
    url(r'^postimage/(?P<id>[0-9]+)$', views.loadImage),
    url(r'^auth/$', CustomAuthToken.as_view())
]