from django.urls import path
from .views import *
urlpatterns = [
    path('madadkar/<user>', get_profile, name='get_profile'),
    path('register', UserCreate.as_view(), name='UserCreate'),
    path('register/activation/<uid>', user_active, name='user_active'),
]