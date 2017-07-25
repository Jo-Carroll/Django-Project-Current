from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import polls

urlpatterns = [
	url(r'^polls/', include('polls.urls')),
	url(r'^lookup/', include('lookup.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^status/', polls.views.status, name='status'),
    url(r'^rates/', polls.views.rates, name='rates'),
    url(r'^main/', polls.views.main, name='main'),
    url(r'^lan/', polls.views.lan, name='lan'),
    url(r'^package/', polls.views.package, name='package'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


