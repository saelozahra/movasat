from django.urls import path
from . import views

urlpatterns = [
    path('challenge/', views.all_challenges, name='all_challenges'),
    path('challenge/<fid>', views.ForumView.as_view(), name='show_forum'),
    path('challenge/tag/<c_cat_slug>', views.show_challenge_cat, name='show_challenge_cat'),
    path('divar/<did>', views.DivarView.as_view(), name='show_forum'),
]