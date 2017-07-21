from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.logreg, name='logreg'),
    url(r'^books', views.landing, name='landing'),
]
