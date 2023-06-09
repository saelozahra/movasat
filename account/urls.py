from django.urls import path
from .views import *
urlpatterns = [
    path('auth/otp', OTPStart.as_view(), name='OTPStart'),
    path('auth/otp/validate', OTPValidate.as_view(), name='OTPValidate'),
    # path(r'', views.MainPage.as_view(), name="index"),
    # path('page/<slug>', views.page_view, name='page_view'),
    path('madadkar/<user>', get_profile, name='get_profile')
]