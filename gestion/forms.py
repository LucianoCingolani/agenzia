from django import forms
from .models import Operacion

class FacturaUploadForm(forms.ModelForm):
    class Meta:
        model = Operacion
        fields = ['descripcion', 'monto_total_real', 'archivo_factura']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Compra Bidones'}),
            'monto_total_real': forms.NumberInput(attrs={'class': 'form-control'}),
            'archivo_factura': forms.FileInput(attrs={'class': 'form-control'}),
        }
