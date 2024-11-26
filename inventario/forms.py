from django import forms
from .models import Movimiento, MovimientoDetalle
from django.forms import modelformset_factory


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['bodega_origen', 'bodega_destino']


MovimientoDetalleFormSet = modelformset_factory(
    MovimientoDetalle,
    fields=('producto', 'cantidad'),
    extra=1
)
