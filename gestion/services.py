import pdfplumber
import re
from .models import Producto

def procesar_pdf_stock(file_obj):
    creados = 0
    actualizados = 0

    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            # Extraemos la tabla del PDF
            table = page.extract_table()
            if not table:
                continue

            for row in table:
                # 1. Limpiamos cada celda de saltos de línea y espacios
                row = [str(c).replace('\n', ' ').strip() if c else "" for c in row]

                # 2. Ignoramos encabezados o filas vacías
                if not row or "Descripción" in row[1] or not row[1]:
                    continue

                try:
                    # row[1] es la Descripción del producto
                    nombre = row[1] 
                    
                    # row[4] es el Stock. Limpiamos puntos finales y comas
                    stock_raw = row[4].replace(',', '.')
                    # Usamos regex para quedarnos solo con el número (ej: de "112." a "112")
                    match = re.search(r"(\d+)", stock_raw)
                    if not match:
                        continue
                    
                    stock_valor = int(match.group(1))

                    # Actualizamos si existe, creamos si no
                    obj, created = Producto.objects.update_or_create(
                        nombre=nombre,
                        defaults={'stock_actual': stock_valor}
                    )
                    
                    if created: creados += 1
                    else: actualizados += 1
                except (IndexError, ValueError):
                    continue
                    
    return creados, actualizados