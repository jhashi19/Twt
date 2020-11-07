from django.contrib import admin
from django.urls import path, include
from tweet.views import IndexView
from django.conf import settings
from django.conf.urls.static import static

# 画像を表示するためにstaticメソッドの部分を追加。
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),  # Django標準のログイン機能を使用
    path('tweet/', include('tweet.urls')),
    path('', IndexView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
