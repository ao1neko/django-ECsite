from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from . import settings

#プロジェクトURL
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecsitecore.urls')),
    path('accounts/', include('accounts.urls')),
]

# 開発サーバーでメディアを配信できるようにする設定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#debug toolbar用url
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

