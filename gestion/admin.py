from django.contrib import admin
from .models import Operacion, GastoGeneral, Producto

@admin.register(Operacion)
class OperacionAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista
    list_display = ('fecha', 'tipo', 'descripcion', 'monto_total_real', 'monto_facturado', 'es_fiscal')
    
    # Filtros laterales para segmentar rápido
    list_filter = ('tipo', 'es_fiscal', 'fecha')
    
    # Buscador por descripción o cliente
    search_fields = ('descripcion',)
    
    # Orden por fecha descendente (lo más nuevo arriba)
    ordering = ('-fecha',)

    # Para que el campo 'monto_informal' (si lo creaste como propiedad) sea visible, 
    # podrías agregarlo aquí, pero por ahora mantengamos lo básico.

@admin.register(GastoGeneral)
class GastoGeneralAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'descripcion', 'categoria', 'tipo', 'monto')
    list_filter = ('categoria', 'tipo', 'fecha')
    search_fields = ('descripcion',)
    ordering = ('-fecha',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock_actual', 'umbral_minimo')
    search_fields = ('nombre',)