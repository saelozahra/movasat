from django.urls import path
from madadyar import views
urlpatterns = [
    path('api/bohran/', views.BohranAPI.as_view(), name='BohranAPI'),
    path('api/aghlam/', views.AghlamAPI.as_view(), name='AghlamAPI'),
]