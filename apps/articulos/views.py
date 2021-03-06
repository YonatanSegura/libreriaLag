from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.articulos.models import Articulo
from apps.articulos.forms import ArticuloForm
from django.db.models import Q, F
import random


# ver articulos
from apps.ventas.models import detalle


def articulo(request):
    try:
        if request.session['ventaId']:
            ventaId = request.session['ventaId']
            notify = detalle.objects.filter(id_venta=ventaId).count()
            query = Articulo.objects.filter(is_activate=1).annotate(cant=F('stock') * F('stock_caja'))
            return render(request, 'productos/articulo.html', {'articulo': query, 'notify':notify})
        else:
            request.session['ventaId'] = ''
            query = Articulo.objects.filter(is_activate=1).annotate(cant=F('stock') * F('stock_caja'))
            return render(request, 'productos/articulo.html', {'articulo': query})
    except:
        request.session['ventaId'] = ''
        query = Articulo.objects.filter(is_activate=1).annotate(cant=F('stock') * F('stock_caja'))
        return render(request, 'productos/articulo.html', {'articulo': query})
# ver articulos
def articuloDetalle(request, pk):
    query = Articulo.objects.get(id=pk)
    if query.stock_caja:
        cant = (query.stock * query.stock_caja)
        precioCj = (query.stock * query.precio_unidad)
        return render(request, 'productos/articuloDetalle.html', {'articulo': query, 'cant': cant, 'precioCj': precioCj})
    return render(request, 'productos/articuloDetalle.html', {'articulo': query})

# crear articulos
class CrearArticulo(SuccessMessageMixin, CreateView):
    template_name = 'productos/productoModal.html'
    form_class = ArticuloForm

    def get_success_url(self):
        return reverse_lazy('articulo:articulo')

    success_message = 'Operacion Exitosa'

# Mostrar los productos sin stock


def inventario(request):
    # Articulos con estado activo, con stock mayor que 1 pero menores que 10
    query = Articulo.objects.filter(Q(stock__gt=0) & Q(stock__lt=11)).exclude(is_activate=0).order_by('stock')
    # Articulos con 0 existencias
    query_ar = Articulo.objects.filter(stock=0).exclude(is_activate=0).order_by('stock')
    # Todos los demás articulos mayores ue 10
    query_are = Articulo.objects.filter(stock__gt=10).exclude(is_activate=0).order_by('stock')

    return render(request, 'productos/inventario.html', {'inventario1': query, 'inventario': query_ar, 'inventariop': query_are})



    #Buscar Articulos
def buscar(request):
    buscar= request.GET.get('search','')
    queryset = Articulo.objects.filter(Q(nombre_articulo__contains=buscar)|Q(codigo_articulo__contains=buscar)).order_by('nombre_articulo')
    print(buscar)
    print(queryset)
    return render(request,'productos/articulo.html',{'articulo':queryset, 'busqueda':buscar}) 

def inicio(request):
    return render(request, 'productos/index.html')

def generador(request):
    try:
        evaluation = request.POST.get('evaluation', '')
        if evaluation:
            articulos = Articulo.objects.values_list('codigo_articulo', flat=True).order_by('pk')
            print(articulos)
            i = 0
            while i == 0:
                codigo = random.randrange(1000000, 99999999, 1)
                articulos = Articulo.objects.filter(codigo_articulo=codigo).count()
                print(articulos)
                if articulos == 0:
                    return render(request, 'productos/generador.html', {'codigo': codigo})
                else:
                    print("funciona")
        else:
            return render(request, 'productos/generador.html')
    except:
        return render(request, 'productos/generador.html')
