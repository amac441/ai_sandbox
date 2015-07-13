from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ex1/$', views.ex1, name="ex1"),
]
