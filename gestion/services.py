import openpyxl
from .models import Producto

def procesar_excel_stock_limpio(file_obj):
    # Cargamos el libro de trabajo de Excel
    wb = openpyxl.load_workbook(file_obj)
    sheet = wb.active # Toma la hoja activa
    
    creados = 0
    actualizados = 0

    # Iteramos desde la fila 1 (o 2 si dejaste el encabezado)
    for row in sheet.iter_rows(values_only=True):
        # Según tus archivos: row[0] es Descripción, row[1] es Stock
        nombre_raw = row[0]
        stock_raw = row[1]

        # Validamos que no sea una fila vacía o el encabezado
        if not nombre_raw or str(nombre_raw).strip().lower() == 'descripción':
            continue

        nombre = str(nombre_raw).strip()
        
        try:
            # Convertimos el stock a número (manejando posibles decimales como 282.2)
            stock_valor = int(float(str(stock_raw)))
        except (ValueError, TypeError):
            stock_valor = 0

        # update_or_create: busca por nombre, si no está lo crea, si está lo actualiza
        obj, created = Producto.objects.update_or_create(
            nombre=nombre,
            defaults={'stock_actual': stock_valor}
        )

        if created:
            creados += 1
        else:
            actualizados += 1

    return creados, actualizados