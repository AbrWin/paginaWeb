from django.contrib import admin
from .models import cliente, producto, categoriaProducto

# class productoAdmin(admin.ModelAdmin):
# 	list_display = ('nombre','precio','stock')
# 	list_filter = ('nombre','precio')

class productoAdmin(admin.ModelAdmin):
	list_display = ('nombre','precio','stock','thumbnail')
	list_filter = ('nombre','precio')
	search_fields = ['nombre','precio']
	fields = ('nombre','descripcion',('precio','stock' , 'categorias' ,'status'),'imagen')


admin.site.register(cliente)
admin.site.register(producto, productoAdmin)
admin.site.register(categoriaProducto)



