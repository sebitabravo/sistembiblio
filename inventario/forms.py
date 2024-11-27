from django import forms
from .models import Movimiento, MovimientoDetalle, Producto
from django.forms import modelformset_factory


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['bodega_origen', 'bodega_destino']
        widgets = {
            'bodega_origen': forms.Select(attrs={'class': 'form-control'}),
            'bodega_destino': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        bodega_origen = cleaned_data.get('bodega_origen')
        bodega_destino = cleaned_data.get('bodega_destino')

        if bodega_origen == bodega_destino:
            raise forms.ValidationError(
                "La bodega de origen y destino no pueden ser iguales."
            )
        return cleaned_data


class MovimientoDetalleForm(forms.ModelForm):
    class Meta:
        model = MovimientoDetalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        bodega_origen = kwargs.pop('bodega_origen', None)
        super().__init__(*args, **kwargs)
        # Si hay bodega de origen, filtra los productos, si no, muestra todos
        if bodega_origen:
            self.fields['producto'].queryset = Producto.objects.filter(
                bodega=bodega_origen)
        else:
            self.fields['producto'].queryset = Producto.objects.all()


MovimientoDetalleFormSet = modelformset_factory(
    MovimientoDetalle,
    form=MovimientoDetalleForm,
    extra=1,
)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['tipo', 'titulo', 'editorial',
                  'autores', 'descripcion', 'bodega']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.Select(attrs={'class': 'form-control'}),
            'autores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'bodega': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_bodega(self):
        bodega = self.cleaned_data.get('bodega')
        if not bodega:
            raise forms.ValidationError("Debes seleccionar una bodega.")
        return bodega
