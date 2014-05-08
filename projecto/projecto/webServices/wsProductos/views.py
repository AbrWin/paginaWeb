from django.http import HttpResponse
from ventas.models import producto
from django.core import serializers#Integramos la serializacion de los objetos

def wsProductos_view(request):
	data = serializers.serialize("json",producto.objects.filter(status=True))
	#Retorna la informacion en formato Json, puedo cambiarlo a Json
	return HttpResponse(data,mimetype='application/json')
