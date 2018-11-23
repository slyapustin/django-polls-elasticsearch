from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('polls.urls')),
    path('search/', include('haystack.urls')),
    path('admin/', admin.site.urls),
]
