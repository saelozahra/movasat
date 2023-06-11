from django.urls import path
from . import views

urlpatterns = [
    path('challenge/<fid>', views.show_forum, name='show_forum'),
]