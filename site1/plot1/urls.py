from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ex1/$', views.ex1, name="ex1"),
    url(r'^ex2/$', views.ex2, name="ex2"),
    url(r'^ex3/$', views.ex3, name="ex3"),
]
