from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dev/', admin.site.urls),
    path('', include('SIMS_.urls', namespace='sims')),
    path('auth/', include('SIMS_Authentication.urls', namespace='sims_auth')),
    path('admin/', include('SIMS_Admin.urls', namespace='sims_admin')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)