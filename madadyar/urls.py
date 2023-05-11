from django.urls import path
from madadyar import views
urlpatterns = [
    # path('auth/otp', views.OTPStart.as_view(), name='OTPStart'),
    path('aghlam/all/', views.AghlamAPI.as_view(), name='AghlamAPI'),
]