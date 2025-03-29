from django.urls import path
from .views import GeneratePostAPIView, home
from .views import (GeneratePostAPIView,
home, 
SocialMediaShareView, 
RegenerateImageView
)
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('generate/', GeneratePostAPIView.as_view(), name="generate_post"),
    path('regenerate-image/', RegenerateImageView.as_view(), name="regenerate_image"),
     path('share/<str:platform>/', SocialMediaShareView.as_view(), name="social_share"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    