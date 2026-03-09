import pdfplumber
import re
from .models import Producto

def procesar_pdf_solo_crear(file_obj):
    creados = 0
    ignorados = 0

    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            # Extraemos el texto crudo para no depender de si hay celdas o no
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                # Limpiamos comillas y espacios
                clean_line = line.replace('"', '').strip()

                # Tu PDF tiene este orden: Código, Descripción, Marca...
                # Si la línea empieza con un código o tiene una descripción válida:
                parts = clean_line.split(',')
                
                # Validamos que la línea tenga contenido y no sea el encabezado
                if len(parts) < 2 or "Descripción" in parts[1] or "Código" in parts[0]:
                    continue

                    # Tomamos la descripción (nombre del producto)
                nombre = parts[1].strip()
                
                if nombre:
                    # get_or_create: Crea el producto en 0 si no existe
                    obj, created = Producto.objects.get_or_create(
                        nombre=nombre,
                        defaults={'stock_actual': 0}
                    )
                    
                    if created:
                        creados += 1
                    else:
                        ignorados += 1
                    
    return creados, ignorados