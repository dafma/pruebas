from django.conf.urls import url
from django.contrib import admin
from .views import enforma, retrasos


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', enforma, name='endorma'),
    url(r'^retrasos/$', retrasos, name='retrasos')

]
