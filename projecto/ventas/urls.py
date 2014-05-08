from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ventas.views',
	url(r'^add/producto/$','add_product_view', name='vista_addProducto'),
	url(r'^edit/producto/(?P<id_prod>.*)/$','edit_product_view', name='vista_edit_producto'),
)