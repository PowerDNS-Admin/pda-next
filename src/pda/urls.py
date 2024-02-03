from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
  path('', include('apps.dashboard.urls')),
  path('account', include('apps.account.urls')),
  path('admin', admin.site.urls),
  path('notifications', include('apps.notifications.urls')),
  path('user', include('apps.user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
