from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.home_view, name="index"),
]