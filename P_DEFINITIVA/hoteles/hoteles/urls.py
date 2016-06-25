"""hoteles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^template/(?P<path>.*)$','django.views.static.serve',
    	{'document_root': settings.STATIC2_URL}),
    url(r'^$', 'AlohaMadrid.views.pagina_principal'),
    url(r'^login$', 'AlohaMadrid.views.entrar'),
    url(r'^logout$', 'AlohaMadrid.views.salir'),
    url(r'^datos_usuario$', 'AlohaMadrid.views.datos_usuario'),
    url(r'^alojamientos$', 'AlohaMadrid.views.pagina_todos_alojamientos'),
    url(r'^alojamientos/(\d+)$', 'AlohaMadrid.views.pagina_alojamiento_id'),
    url(r'^poner_comentario/(\d+)$', 'AlohaMadrid.views.poner_comentario'),
    url(r'^(.*)/xml$', 'AlohaMadrid.views.pagina_usuario_xml'),
    url(r'^about$', 'AlohaMadrid.views.pagina_about'),
    url(r'^(.*)$', 'AlohaMadrid.views.pagina_usuario'),
]
