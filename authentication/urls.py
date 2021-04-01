from django.urls import path

from .views import RegistrationApiView, LoginApiView, UserRetrieveUpdateApiView

app_name = "authentication"
urlpatterns = [
    path('user/register/', RegistrationApiView.as_view()),
    path('user/login/', LoginApiView.as_view()),
    path('user/', UserRetrieveUpdateApiView.as_view()),
]
