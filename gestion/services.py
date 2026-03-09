import openpyxl
from .models import Producto

def procesar_excel_stock_completo(file_obj):
    wb = openpyxl.load_workbook(file_obj)
    creados = 0
    actualizados = 0

    # RECORRE TODAS LAS HOJAS (las 11 páginas)
    for sheet in wb.worksheets:
        # Iteramos las filas de cada hoja
        for row in sheet.iter_rows(values_only=True):
            # row[0] = Descripción, row[1] = Stock
            nombre_raw = row[0]
            stock_raw = row[1]

            # Validamos que la fila tenga datos y no sea un encabezado
            if not nombre_raw or str(nombre_raw).strip().lower() in ['descripción', 'descripcion', 'nombre']:
                continue

            nombre = str(nombre_raw).strip()
            
            try:
                # Convertimos el stock (limpiando posibles puntos o comas)
                stock_valor = int(float(str(stock_raw).replace(',', '.')))
            except (ValueError, TypeError):
                stock_valor = 0

            # Guardamos o actualizamos
            obj, created = Producto.objects.update_or_create(
                nombre=nombre,
                defaults={'stock_actual': stock_valor}
            )

            if created:
                creados += 1
            else:
                actualizados += 1

    return creados, actualizados