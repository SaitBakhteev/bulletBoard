from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/ads/')),  # перенаправление на ads
    path('ads/', include('ads.urls')),
    path('admin/', admin.site.urls),
    path('sign/', include('sign.urls')),
    path('account/', include('allauth.urls')),
    # path(('error/',)
]
