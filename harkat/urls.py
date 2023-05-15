from django.urls import path
from harkat import views
urlpatterns = [
    path('harkat/<jahadi>/<slug>/', views.harkat_single, name='harkat_single'),
]