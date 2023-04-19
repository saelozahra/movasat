from django.urls import path
from .views import *

urlpatterns = [
    path('harekat', harekat_main),
    path('harekat/<id>', harekat_id),
]
