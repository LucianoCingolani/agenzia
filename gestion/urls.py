from django.urls import path
from .views import dashboard_resumen, exportar_gastos_excel, gestion_gastos_generales, subir_factura

urlpatterns = [
    # Aquí pasamos directamente la función
    path('dashboard/', dashboard_resumen, name='dashboard'),
    path('subir/', subir_factura, name='subir_factura'),
    path('gastos/', gestion_gastos_generales, name='gastos_generales'),
    path('gastos/exportar/', exportar_gastos_excel, name='exportar_gastos_excel'),
]