from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('projecto.webServices.wsProductos.views',
	url(r'^ws/productos/$','wsProductos_view', name='ws_producto_url'),
)