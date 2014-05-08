from django.shortcuts import render_to_response
from django.template import RequestContext
from ventas.models import producto
from .forms import ContactForm, LoginForm, RegisterForm #si escribimos projecto.home.forms aunque no es necesario ya que es forms.py esta dentro de la misma app.s
from django.core.mail import EmailMultiAlternatives #Enviamos HTML
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from projecto.settings import URL_LOGIN
import django
import simplejson

def index_view(request):
    return render_to_response('home/index.html',context_instance=RequestContext(request))

@login_required(login_url=URL_LOGIN)
def about_view(request):
	version = django.get_version()
	mensaje = "Esto es un mensaje desde  mi vista"
	ctx={'msg':mensaje,'version':version}
	return render_to_response('home/about.html', ctx, context_instance=RequestContext(request))

def productos_view(request,pagina):
        if request.method=="POST":
                if "product_id" in request.POST:
                        try:
                                id_producto = request.POST['product_id']
                                p = producto.objects.get(pk=id_producto)
                                mensaje = {"status":"True","product_id":p.id}
                                p.delete() # Elinamos objeto de la base de datos
                                return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
                        except:
                                mensae = {"status":"False"}
                                return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
        lista_prod = producto.objects.filter(status=True) # Select * from ventas_productos where status = True
        paginator = Paginator(lista_prod,3) # Cuantos productos quieres por pagina? = 3
        try:
                page = int(pagina)
        except:
                page = 1
        try:
                productos = paginator.page(page)
        except (EmptyPage,InvalidPage):
                productos = paginator.page(paginator.num_pages)
        ctx = {'productos':productos}
        return render_to_response('home/productos.html',ctx,context_instance=RequestContext(request))


def singleProduct_view(request,id_prod):
    prod = producto.objects.get(id=id_prod)
    cats = prod.categorias.all()#obtiene la categoria de los productos
    ctx = {'producto':prod, 'categorias':cats}
    return render_to_response('home/singleProducto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url=URL_LOGIN)
def contacto_view(request):
	info_enviado = False # Definir la informacion si se envio o no se envio
	email=""
	titulo=""
	texto=""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email  = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto  = formulario.cleaned_data['Texto']
			#confguracion de envar el formulario al mail
			to_admin = 'abrwin21@gmail.com'
			html_content = 'informacion recibida [%s] <br><br><br>***Mensaje***<br><br><br>%s' %(email,texto)
			msg = EmailMultiAlternatives('Correo de contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content,'text/html')# Se define el contenido HTML
			msg.send()#envamiamos el contenido 
	else:
		formulario = ContactForm()
	ctx = {'form':formulario, 'email':email, 'titulo':titulo, 'texto':texto, 'info_enviado':info_enviado}
	return render_to_response('home/contact.html',ctx, context_instance=RequestContext(request))


def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				next = request.POST['next']				
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect(next)
				else:
					mensaje = "Usuario y/o password incorrecto"
		next = request.REQUEST.get('next')			    
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje,'next':next}
		return render_to_response('home/login.html',ctx, context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save() # Guardar el objeto
			return render_to_response('home/gracias_registro.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return 	render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))



