from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from .models import Producto, Bodega, Movimiento, MovimientoDetalle
from .forms import MovimientoForm, MovimientoDetalleFormSet


class ProductoListView(ListView):
    model = Producto
    template_name = 'productos_list.html'
    context_object_name = 'productos'


class ProductoCreateView(CreateView):
    model = Producto
    fields = ['tipo', 'titulo', 'editorial', 'autores', 'descripcion']
    template_name = 'producto_form.html'
    success_url = reverse_lazy('productos_list')


class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['tipo', 'titulo', 'editorial', 'autores', 'descripcion']
    template_name = 'producto_form.html'
    success_url = reverse_lazy('productos_list')


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto_confirm_delete.html'
    success_url = reverse_lazy('productos_list')


class BodegaListView(ListView):
    model = Bodega
    template_name = 'bodegas_list.html'
    context_object_name = 'bodegas'


class BodegaCreateView(CreateView):
    model = Bodega
    fields = ['nombre']
    template_name = 'bodega_form.html'
    success_url = reverse_lazy('bodegas_list')


class BodegaDeleteView(DeleteView):
    model = Bodega
    template_name = 'bodega_confirm_delete.html'
    success_url = reverse_lazy('bodegas_list')

    def form_valid(self, form):
        if self.object.productos_en_bodega().exists():
            messages.error(
                self.request, "No puedes eliminar bodegas con productos.")
            return self.render_to_response(self.get_context_data())
        return super().form_valid(form)


class MovimientoCreateView(View):
    def get(self, request, *args, **kwargs):
        form = MovimientoForm()
        productos_formset = MovimientoDetalleFormSet(
            queryset=MovimientoDetalle.objects.none())
        return render(request, 'movimiento_form.html', {'form': form, 'productos_formset': productos_formset})

    def post(self, request, *args, **kwargs):
        form = MovimientoForm(request.POST)
        productos_formset = MovimientoDetalleFormSet(request.POST)
        if form.is_valid() and productos_formset.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            productos_formset.instance = movimiento
            productos_formset.save()
            return redirect('movimientos_list')
        return render(request, 'movimiento_form.html', {'form': form, 'productos_formset': productos_formset})


class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'movimientos_list.html'
    context_object_name = 'movimientos'


@method_decorator(user_passes_test(lambda u: u.is_jefe_bodega), name='dispatch')
class InformeBodegaView(TemplateView):
    template_name = 'informe_bodega.html'
