from django.urls import path
from . import views

urlpatterns = [
    # Rutas para la gestión de productos
    path('productos/', views.ProductoListView.as_view(), name='productos_list'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(),
         name='productos_create'),
    path('productos/<int:pk>/editar/',
         views.ProductoUpdateView.as_view(), name='productos_update'),
    path('productos/<int:pk>/eliminar/',
         views.ProductoDeleteView.as_view(), name='productos_delete'),

    # Rutas para la gestión de bodegas
    path('bodegas/', views.BodegaListView.as_view(), name='bodegas_list'),
    path('bodegas/nueva/', views.BodegaCreateView.as_view(), name='bodegas_create'),
    path('bodegas/<int:pk>/eliminar/',
         views.BodegaDeleteView.as_view(), name='bodegas_delete'),

    # Rutas para la gestión de movimientos
    path('movimientos/', views.MovimientoListView.as_view(),
         name='movimientos_list'),
    path('movimientos/nuevo/', views.MovimientoCreateView.as_view(),
         name='movimientos_create'),

    # Rutas para la gestión de autores
    path('autores/', views.AutorListView.as_view(), name='autores_list'),
    path('autores/nuevo/', views.AutorCreateView.as_view(), name='autores_create'),
    path('autores/<int:pk>/editar/',
         views.AutorUpdateView.as_view(), name='autores_update'),
    path('autores/<int:pk>/eliminar/',
         views.AutorDeleteView.as_view(), name='autores_delete'),

    # Rutas para la gestión de editoriales
    path('editoriales/', views.EditorialListView.as_view(), name='editoriales_list'),
    path('editoriales/nueva/', views.EditorialCreateView.as_view(),
         name='editoriales_create'),
    path('editoriales/<int:pk>/editar/',
         views.EditorialUpdateView.as_view(), name='editoriales_update'),
    path('editoriales/<int:pk>/eliminar/',
         views.EditorialDeleteView.as_view(), name='editoriales_delete'),

    # Rutas para informes
    path('informes/bodega/', views.InformeBodegaView.as_view(),
         name='informe_bodega'),
    path('informes/movimientos/', views.InformeMovimientosView.as_view(),
         name='informe_movimientos'),
    path('informes/generales/', views.InformesGeneralesView.as_view(),
         name='informes_generales'),
]
