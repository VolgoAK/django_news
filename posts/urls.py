from django.conf.urls import url

from posts import views

urlpatterns = [
    url(r'^posts/$', views.posts),
    url(r'^posts/(?P<id>[0-9]+)$', views.post_by_id),
    url(r'^vote/$', views.add_claps),
    url(r'^comments/(?P<id>[0-9]+)$', views.comments),
    url(r'^postimage/(?P<id>[0-9]+)$', views.loadImage)
]