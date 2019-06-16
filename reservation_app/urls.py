from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts2/', include('accounts2.urls')),
    path('blog/', include('blog.urls')),
    path('', include('membership.urls')),
    path('todo/', include('todo.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('bestlec/', include('bestlec.urls')),
    path('management/', include('management.urls')),
    path('wm/', include('wm.urls')),
    path('challenge/', include('challenge.urls')),
    path('pm/', include('pm.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
