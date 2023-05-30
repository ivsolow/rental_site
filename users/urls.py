from django.urls import include, path, re_path


urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),          # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # http://127.0.0.1:8000/auth/token/login (or logout)
]
