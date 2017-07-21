from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.logreg, name='logreg'),
    url(r'^books/$', views.landing, name='landing'),
    url(r'^books/add', views.add_all, name='add_all'),
    url(r'^books/(?P<id>\d+)$', views.show_book, name='book'),
    url(r'^user/(?P<id>\d+)$', views.show_user, name='user_profile'),
]
