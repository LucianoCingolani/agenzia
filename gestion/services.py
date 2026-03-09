import pdfplumber
import re
from .models import Producto

def procesar_pdf_stock(file_path):
    productos_creados = 0
    productos_actualizados = 0

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue
            
            # Saltamos el encabezado si es la primera página
            for row in table[1:]:
                # Según tu PDF: [Código, Descripción, Marca, Costo, Stock, St. Valorizado]
                # Usamos la descripción como nombre del producto
                nombre_raw = row[1]
                stock_raw = row[4]

                if nombre_raw and stock_raw:
                    # Limpiamos el nombre y convertimos el stock a número
                    nombre = nombre_raw.strip().replace('\n', ' ')
                    
                    try:
                        # Limpiamos caracteres no numéricos del stock (como comas o puntos de miles)
                        stock_limpio = re.sub(r'[^\d.]', '', stock_raw.replace(',', '.'))
                        stock = int(float(stock_limpio))
                    except (ValueError, TypeError):
                        continue

                    # Lógica de Django: Buscar por nombre, si no existe lo crea
                    obj, created = Producto.objects.update_or_create(
                        nombre=nombre,
                        defaults={'stock_actual': stock}
                    )

                    if created:
                        productos_creados += 1
                    else:
                        productos_actualizados += 1
    
    return productos_creados, productos_actualizados