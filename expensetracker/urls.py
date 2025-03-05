from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from trackense.views import google_login, google_callback, signup  # Add this import



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trackense.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/google/', google_login, name='google_login'),
    path('auth/google/callback/', google_callback, name='google_callback'),
    path('signup/', signup, name='signup'),  # Add this URL pattern
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




