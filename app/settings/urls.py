import debug_toolbar

from django.views.generic import (
    TemplateView,
)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    path('__debug__/', include(debug_toolbar.urls)),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('currency/', include('currency.urls')),
    path('account/', include('account.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# /media/ -> static_content/media
