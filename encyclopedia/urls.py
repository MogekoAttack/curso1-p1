from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.get_page, name="encyclopedia_get_page"),
]
