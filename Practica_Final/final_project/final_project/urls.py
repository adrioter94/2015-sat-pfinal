from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from actividades_madrid.feeds import RssUsuarios, RssPrincipal



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'final_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'actividades_madrid.views.pagina_principal'),  
    url(r'^ayuda/$', 'actividades_madrid.views.ayuda'),
    url(r'^registrarse/$', 'actividades_madrid.views.usuario_nuevo'),
    url(r'^logout/$', 'actividades_madrid.views.logout'),
    url(r'^css/imagenes/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL3}),
    url(r'^css/(.*)$', 'actividades_madrid.views.plantillaCss'),
    url(r'^actividades/(\d*)/$', 'actividades_madrid.views.actividades_id'),
    url(r'^todas/$', 'actividades_madrid.views.todas'),
    url(r'^principal/rss/$', RssPrincipal()),   
    url(r'^(.*)/rss/$', RssUsuarios()),
    url(r'^(.*)/$', 'actividades_madrid.views.pagina_usuario'),
    
    #url(r'^actividades/stylesheet/imagenes/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL2}),
    #url(r'^actividades/stylesheet/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
)
