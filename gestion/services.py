import pdfplumber
import re
from .models import Producto

def procesar_pdf_solo_crear(file_obj):
    creados = 0
    ignorados = 0

    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text: continue

            lines = text.split('\n')
            for line in lines:
                # 1. Limpieza de comillas y espacios
                clean_line = line.replace('"', '').strip()
                
                # 2. Separar por coma
                parts = clean_line.split(',')
                
                # VALIDACIÓN: Tu PDF tiene [Código, Descripción, Marca, Costo...]
                # Necesitamos que tenga al menos 2 partes y que no sea el encabezado
                if len(parts) < 2 or "Código" in parts[0] or "Descripción" in parts[1]:
                    continue

                # 3. ASIGNACIÓN CORRECTA:
                # parts[0] es el Código (79, 1793, etc.)
                # parts[1] es la Descripción (AC GRANEL, ACONDICIONADOR, etc.)
                nombre_real = parts[1].strip()

                if nombre_real:
                    # Usamos el nombre real para crear el producto
                    obj, created = Producto.objects.get_or_create(
                        nombre=nombre_real,
                        defaults={'stock_actual': 0}
                    )
                    
                    if created: creados += 1
                    else: ignorados += 1
                    
    return creados, ignorados