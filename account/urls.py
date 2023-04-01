from django.urls import path
from . import views
urlpatterns = [
    path('auth/otp', views.OTPStart.as_view(), name='OTPStart'),
    path('auth/otp/validate', views.OTPValidate.as_view(), name='OTPValidate'),
    # path(r'', views.MainPage.as_view(), name="index"),
    # path('page/<slug>', views.page_view, name='page_view'),
]