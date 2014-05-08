from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import addProductForm #tambien puede ser ventas.forms
from .models import producto #Lo utilizo de esta manera ya que estamos en la misma app 
from django.http import HttpResponseRedirect


def edit_product_view(request,id_prod):
	info = 'Iniciado'
	prod = producto.objects.get(pk=id_prod)
	if request.method == 'POST':
		form = addProductForm(request.POST, request.FILES,instance=prod)
		if form.is_valid():
			edit_prod = form.save(commit=False)
			form.save_m2m()
			edit_prod.status= True
			edit_prod.save()#Guardamos la edicion del producto
			info = "Guardado satisfactoriamente >.<"
			return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
	else:
		form = addProductForm(instance=prod)
	ctx = {'form':form,'informacion':info}
	return render_to_response('ventas/editProducto.html',ctx,context_instance=RequestContext(request))


def add_product_view(request):
	info = "Iniciado"
	if request.method == "POST":
		form = addProductForm(request.POST, request.FILES)
		if form.is_valid():
			add = form.save(commit=False)
			add.status = True
			add.status= True
			add.save() # Guardamos la informacion
			form.save_m2m() # Guarda las relaciones manyToMany
			info = "Guardado satisfactoriamente >.<"
			return HttpResponseRedirect('/producto/%s/'%add.id)
	else:
		form = addProductForm()
	ctx = {'form':form,'informacion':info}
	return render_to_response('ventas/addProducto.html',ctx,context_instance=RequestContext(request))



"""def add_product_view(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			form = addProductForm(request.POST, request.FILES)
			info = "inicializando"
			if form.is_valid():
				nombre = form.cleaned_data['nombre']
				descripcion = form.cleaned_data['descripcion']
				imagen = form.cleaned_data['imagen']#Esto se optiene con el request.FILES
				precio = form.cleaned_data['precio']
				stock  = form.cleaned_data['stock']				
				p = producto()
				if imagen:#Generamos la validacion de imagen
					p.imagen = imagen
				p.nombre = nombre
				p.descripcion = descripcion
				p.precio = precio
				p.stock = stock
				p.status = True
				p.save() #guardas la informacion
				info ="Se guardo satisfactoriamente!"
			else:
				info = "Informacion con datos incorrectos"
			form = addProductForm()
			ctx = {'form':form, 'informacion':info}
			return render_to_response('ventas/addProducto.html',ctx,context_instance=RequestContext(request))

		else: #Si es GET obtenemos un formulario en blanco
			form = addProductForm()
			ctx = {'form':form}
			return render_to_response('ventas/addProducto.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')"""

"""def edit_product_view(request,id_prod):
	p = producto.objects.get(id=id_prod)
	if request.method == "POST":
		form = addProductForm(request.POST, request.FILES)
		if form.is_valid():
			nombre = form.cleaned_data['nombre']
			descripcion = form.cleaned_data['descripcion']
			imagen = form.cleaned_data['imagen']
			precio = form.cleaned_data['precio']
			stock = form.cleaned_data['stock']
			p.nombre = nombre
			p.descripcion = descripcion			
			p.precio = precio
			p.stock = stock
			if imagen:#Con esto verificamos si existe la imagen
				p.imagen = imagen
			p.save()#Guardamos el modelo de manera EDITADA}
			info = "Se guardo satisfactoriamente!!!!!"
			return HttpResponseRedirect("/producto/%s"%p.id)

	if request.method == "GET":
		form = addProductForm(initial={
			'nombre':p.nombre,
			'descripcion':p.descripcion,
			'precio':p.precio,
			'stock':p.stock,
			})
	ctx = {'form':form, 'producto':p}
	return render_to_response('ventas/editProducto.html',ctx,context_instance=RequestContext(request))"""

