import pdfplumber
import re
from .models import Producto

def procesar_pdf_solo_crear(file_obj):
    creados = 0
    ignorados = 0

    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue

            for row in table:
                # Limpieza de celdas (quitamos comillas y saltos de línea)
                row = [str(cell).replace('"', '').replace('\n', ' ').strip() if cell else "" for cell in row]

                # Validación: Saltamos si no hay descripción o es el encabezado
                if len(row) < 2 or not row[1] or "Descripción" in row[1] or "Código" in row[0]:
                    continue

                nombre = row[1]

                # get_or_create: 
                # Si el nombre no existe, crea el producto con los defaults.
                # Si el nombre existe, simplemente lo trae y 'created' será False.
                obj, created = Producto.objects.get_or_create(
                    nombre=nombre,
                    defaults={'stock_actual': 0} # Se crea con stock 0 como pediste
                )
                
                if created:
                    creados += 1
                else:
                    ignorados += 1
                    
    return creados, ignorados