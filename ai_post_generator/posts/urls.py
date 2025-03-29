from django.urls import path
from .views import GeneratePostAPIView, home
from .views import SocialMediaShareView, home
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('generate/', GeneratePostAPIView.as_view(), name="generate_post"), 
     path('share/<str:platform>/', SocialMediaShareView.as_view(), name="social_share"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)