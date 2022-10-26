from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import home_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("allauth.urls")),
    path("", home_view, name="home-view"),
    path("profiles/", include("profiles.urls")),
    path("posts/", include("posts.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
