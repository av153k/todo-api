from django.urls import path
from .views import ProfileRetrieveApiView

app_name = 'profiles'
urlpatterns = [
    path('profile/<str:username>', ProfileRetrieveApiView.as_view()),
]
