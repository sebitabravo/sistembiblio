from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
# Importar models para usar funciones de agregación como Count
from django.db import models

from .models import Producto, Bodega, Movimiento, MovimientoDetalle, Autor, Editorial
from .forms import MovimientoForm, MovimientoDetalleFormSet

# -----------------------------------
# Vistas de Productos
# -----------------------------------


class ProductoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Producto
    template_name = 'productos_list.html'
    context_object_name = 'productos'

    def test_func(self):
        return self.request.user.is_jefe_bodega or self.request.user.is_bodeguero


class ProductoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Producto
    fields = ['tipo', 'titulo', 'editorial', 'autores',
              'descripcion', 'bodega', 'cantidad']
    template_name = 'producto_form.html'
    success_url = reverse_lazy('productos_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


class ProductoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Producto
    fields = ['tipo', 'titulo', 'editorial',
              'autores', 'descripcion', 'bodega', 'cantidad']
    template_name = 'producto_form.html'
    success_url = reverse_lazy('productos_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


class ProductoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Producto
    template_name = 'producto_confirm_delete.html'
    success_url = reverse_lazy('productos_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega

    def form_valid(self, form):
        if MovimientoDetalle.objects.filter(producto=self.object).exists():
            messages.error(
                self.request, "No puedes eliminar productos que ya están en una bodega."
            )
            return self.render_to_response(self.get_context_data())
        return super().form_valid(form)


# -----------------------------------
# Vistas de Bodegas
# -----------------------------------

class BodegaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Bodega
    template_name = 'bodegas_list.html'
    context_object_name = 'bodegas'

    def test_func(self):
        return self.request.user.is_bodeguero or self.request.user.is_jefe_bodega


class BodegaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Bodega
    fields = ['nombre']
    template_name = 'bodega_form.html'
    success_url = reverse_lazy('bodegas_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


class BodegaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bodega
    template_name = 'bodega_confirm_delete.html'
    success_url = reverse_lazy('bodegas_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega

    def form_valid(self, form):
        if self.object.productos_en_bodega().exists():
            messages.error(
                self.request, "No puedes eliminar bodegas que contienen productos."
            )
            return self.render_to_response(self.get_context_data())
        return super().form_valid(form)


# -----------------------------------
# Vistas de Movimientos
# -----------------------------------

class MovimientoCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_bodeguero

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
            movimiento.save()  # Guardar el movimiento primero

            for detalle_form in productos_formset:
                if detalle_form.cleaned_data:  # Ignorar formularios vacíos
                    detalle = detalle_form.save(commit=False)
                    detalle.movimiento = movimiento  # Asignar el movimiento
                    detalle.save()

            messages.success(request, "Movimiento registrado correctamente.")
            return redirect('movimientos_list')

        return render(request, 'movimiento_form.html', {'form': form, 'productos_formset': productos_formset})


class MovimientoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Movimiento
    template_name = 'movimientos_list.html'
    context_object_name = 'movimientos'

    def test_func(self):
        return self.request.user.is_bodeguero


# -----------------------------------
# Vistas de Autores
# -----------------------------------

class AutorListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Autor
    template_name = 'autores_list.html'
    context_object_name = 'autores'

    def test_func(self):
        return self.request.user.is_jefe_bodega


class AutorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Autor
    fields = ['nombre']
    template_name = 'autor_form.html'
    success_url = reverse_lazy('autores_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


class AutorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Autor
    template_name = 'autor_confirm_delete.html'
    success_url = reverse_lazy('autores_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


class AutorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Autor
    fields = ['nombre']
    template_name = 'autor_form.html'
    success_url = reverse_lazy('autores_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


# -----------------------------------
# Vistas de Editoriales
# -----------------------------------

class EditorialListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Editorial
    template_name = 'editoriales_list.html'
    context_object_name = 'editoriales'

    def test_func(self):
        return self.request.user.is_jefe_bodega


class EditorialCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Editorial
    fields = ['nombre']
    template_name = 'editorial_form.html'
    success_url = reverse_lazy('editoriales_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


class EditorialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Editorial
    template_name = 'editorial_confirm_delete.html'
    success_url = reverse_lazy('editoriales_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


class EditorialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Editorial
    fields = ['nombre']
    template_name = 'editorial_form.html'
    success_url = reverse_lazy('editoriales_list')

    def test_func(self):
        return self.request.user.is_jefe_bodega


# -----------------------------------
# Informes
# -----------------------------------

class InformeMovimientosView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'informe_movimientos.html'

    def test_func(self):
        return self.request.user.is_jefe_bodega

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimientos'] = Movimiento.objects.all()
        return context


class InformesGeneralesView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'informes_generales.html'

    def test_func(self):
        return self.request.user.is_jefe_bodega

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Cantidad de productos por bodega basado en los productos asignados actualmente
        context['productos_por_bodega'] = [
            {
                'nombre': bodega.nombre,
                'cantidad': Producto.objects.filter(bodega=bodega).count()
            }
            for bodega in Bodega.objects.all()
        ]

        # Tipos de productos por editorial
        context['productos_por_editorial'] = [
            {
                'editorial': editorial.nombre,
                'libros': Producto.objects.filter(editorial=editorial, tipo='libro').count(),
                'revistas': Producto.objects.filter(editorial=editorial, tipo='revista').count(),
                'enciclopedias': Producto.objects.filter(editorial=editorial, tipo='enciclopedia').count(),
            }
            for editorial in Editorial.objects.all()
        ]

        # Movimientos recientes
        context['movimientos_recientes'] = Movimiento.objects.order_by(
            '-fecha')[:10]

        return context


class InformeBodegaView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'informe_bodega.html'

    def test_func(self):
        return self.request.user.is_jefe_bodega


# -----------------------------------
# Autenticación
# -----------------------------------

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_bodeguero:
            return reverse_lazy('bodegas_list')
        elif self.request.user.is_jefe_bodega:
            return reverse_lazy('productos_list')
        else:
            return reverse_lazy('home')
