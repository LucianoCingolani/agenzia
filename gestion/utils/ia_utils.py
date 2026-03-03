import json
import fitz  # PyMuPDF
import os
from django.conf import settings
from openai import OpenAI

def extraer_texto_pdf(ruta_archivo):
    """Extrae el texto bruto de un archivo PDF."""
    texto = ""
    try:
        with fitz.open(ruta_archivo) as doc:
            for pagina in doc:
                texto += pagina.get_text()
    except Exception as e:
        print(f"Error al leer PDF: {e}")
    return texto

def procesar_con_ia(texto_factura):
    # Asegúrate de importar json y OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"De la siguiente factura, extrae el TOTAL (monto_facturado) como número decimal. Texto: {texto_factura}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        res = json.loads(response.choices[0].message.content)
        
        # Limpieza manual por si la IA manda basura
        monto = res.get('monto_facturado', 0)
        if isinstance(monto, str):
            monto = monto.replace('$', '').replace('.', '').replace(',', '.').strip()
        
        res['monto_facturado'] = float(monto)
        return res
    except Exception as e:
        print(f"ERROR CRÍTICO EN IA: {e}")
        return None