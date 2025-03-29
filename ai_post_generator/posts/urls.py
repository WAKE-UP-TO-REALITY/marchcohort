from django.urls import path
from .views import GeneratePostAPIView, home
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
]