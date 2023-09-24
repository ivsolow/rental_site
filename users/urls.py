from django.urls import include, path, re_path

from .views import UserProfileView


urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/profile/', UserProfileView.as_view(), name='user_profile'),
]
