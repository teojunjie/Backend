from django.contrib import admin
from django.urls import (
    path,
    include,
    re_path,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('user.urls')),
    re_path(r'^', include('category.urls')),
    re_path(r'^', include('places.urls'))
]
