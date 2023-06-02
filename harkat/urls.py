from django.urls import path
from harkat import views
urlpatterns = [
    path('harkat/', views.harkat_page, name='harkat_page'),
    path('harkat/cat/<cid>', views.harkat_page, name='harkat_cat'),
    path('harkat/<jahadi>/<slug>/', views.harkat_single, name='harkat_single'),
]