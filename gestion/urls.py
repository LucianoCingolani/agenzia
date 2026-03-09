from django.urls import path
from .views import actualizar_stock_manual, dashboard_resumen, exportar_gastos_excel, gestion_gastos_generales, inventario_dashboard, procesar_stock_pdf, subir_factura, home
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Aquí pasamos directamente la función
    path('dashboard/', dashboard_resumen, name='dashboard'),
    path('subir/', subir_factura, name='subir_factura'),
    path('gastos/', gestion_gastos_generales, name='gastos_generales'),
    path('gastos/exportar/', exportar_gastos_excel, name='exportar_gastos_excel'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('inventario/', inventario_dashboard, name='inventario_dashboard'),
    path('inventario/procesar-pdf/', procesar_stock_pdf, name='procesar_stock_pdf'),
    path('inventario/actualizar/<int:producto_id>/', actualizar_stock_manual, name='actualizar_stock_manual'),
    path('', home, name='home'),
]