from django.urls import path
from .views import GeneratePostAPIView, home
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('generate/', GeneratePostAPIView.as_view(), name="generate_post"), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)