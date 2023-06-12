from django.urls import path
from . import views

urlpatterns = [
    path('challenge/<fid>', views.show_forum, name='show_forum'),
    # path('challenge/tag/<c_cat_slug>', views.show_challenge_cat, name='show_challenge_cat'),
]