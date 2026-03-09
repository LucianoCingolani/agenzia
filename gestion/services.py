import pdfplumber
import re
from .models import Producto

def procesar_pdf_stock(file_obj):
    creados = 0
    actualizados = 0

    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            # Extraemos la tabla
            table = page.extract_table()
            if not table:
                continue

            for row in table:
                # 1. Limpieza total de la fila: quitamos comillas, saltos de línea y espacios extras
                row = [str(cell).replace('"', '').replace('\n', ' ').strip() if cell else "" for cell in row]

                # 2. Validación de fila de datos
                # Debe tener al menos 5 columnas y la descripción (row[1]) no debe ser vacía ni el encabezado
                if len(row) < 5 or not row[1] or "Descripción" in row[1] or "Código" in row[0]:
                    continue

                try:
                    # row[1] es la Descripción (Nombre del producto)
                    nombre = row[1]
                    
                    # row[4] es el Stock (ejemplo: "282,2" o "112.")
                    stock_raw = row[4].replace(',', '.') # Cambiamos coma por punto para decimales
                    
                    # Usamos regex para extraer solo los números y el punto decimal
                    # Esto limpia casos como "112." (lo deja como "112") o "282.2"
                    match = re.search(r"(\d+\.?\d*)", stock_raw)
                    if not match:
                        continue
                    
                    # Convertimos a float y luego a int (o lo dejamos en float si preferís)
                    stock_valor = int(float(match.group(1)))

                    # Guardar o actualizar en la base de datos
                    obj, created = Producto.objects.update_or_create(
                        nombre=nombre,
                        defaults={'stock_actual': stock_valor}
                    )
                    
                    if created:
                        creados += 1
                    else:
                        actualizados += 1
                except (IndexError, ValueError, Exception):
                    continue
                    
    return creados, actualizados