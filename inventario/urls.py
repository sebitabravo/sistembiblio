from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.ProductoListView.as_view(), name='productos_list'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(),
         name='productos_create'),
    path('productos/<int:pk>/editar/',
         views.ProductoUpdateView.as_view(), name='productos_update'),
    path('productos/<int:pk>/eliminar/',
         views.ProductoDeleteView.as_view(), name='productos_delete'),
    path('bodegas/', views.BodegaListView.as_view(), name='bodegas_list'),
    path('bodegas/nueva/', views.BodegaCreateView.as_view(), name='bodegas_create'),
    path('bodegas/<int:pk>/eliminar/',
         views.BodegaDeleteView.as_view(), name='bodegas_delete'),
    path('movimientos/', views.MovimientoListView.as_view(),
         name='movimientos_list'),
    path('movimientos/nuevo/', views.MovimientoCreateView.as_view(),
         name='movimientos_create'),
]
