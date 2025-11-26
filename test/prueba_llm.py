from openai import OpenAI
import json

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lmstudio"
)

# Ejemplos de llamadas a clasificar
llamadas_ejemplo = [
    "Ofrecer plan premium con descuento del 10%",
    "Guiar al cliente a reiniciar el módem de Claro",
    "Escalar a supervisor por tono alterado",
    "Enviar enlace de pago por WhatsApp",
    "Verificar cobertura en zona rural de Pitalito",
    "Registrar PQR y confirmar número de radicado",
    "Cerrar venta con oferta 2x1 en datos",
    "Solicitar captura de pantalla del error"
]

# Prompt para clasificación
prompt_clasificacion = """Eres un sistema experto en clasificación de llamadas de call center.

Tu tarea es clasificar cada llamada en una de estas tres categorías:
- "venta": Cuando la llamada involucra ofrecer productos, cerrar ventas, promociones, descuentos, ofertas comerciales
- "soporte": Cuando la llamada involucra resolver problemas técnicos, guiar al cliente, verificar servicios, solicitar información técnica
- "reclamo": Cuando la llamada involucra quejas, escalación a supervisor, registro de PQR, problemas que requieren seguimiento formal

IMPORTANTE: Debes responder ÚNICAMENTE con un objeto JSON válido en este formato exacto:
{
  "clasificacion": "venta"
}

O:
{
  "clasificacion": "soporte"
}

O:
{
  "clasificacion": "reclamo"
}

NO agregues texto adicional, explicaciones, ni nada más. Solo el JSON.

Clasifica la siguiente llamada:"""

# Función para clasificar una llamada
def clasificar_llamada(descripcion_llamada: str) -> dict:
    """
    Clasifica una llamada en una de las categorías: venta, soporte, reclamo.
    
    Args:
        descripcion_llamada: Descripción de la llamada a clasificar
        
    Returns:
        Diccionario con la clasificación
    """
    mensaje_completo = f"{prompt_clasificacion}\n\n{descripcion_llamada}"
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """Eres un clasificador de llamadas. Tu única tarea es responder con un objeto JSON válido.

FORMATO OBLIGATORIO (responde SOLO esto, sin texto adicional):
{
  "clasificacion": "venta"
}

O:
{
  "clasificacion": "soporte"
}

O:
{
  "clasificacion": "reclamo"
}

Categorías:
- "venta": ofertas, descuentos, cerrar ventas, promociones
- "soporte": problemas técnicos, guías, verificación de servicios
- "reclamo": quejas, escalación, PQR, problemas formales

NO agregues explicaciones. NO uses markdown. Solo el JSON puro."""
            },
            {
                "role": "user",
                "content": mensaje_completo
            }
        ],
        temperature=0.1  # Baja temperatura para respuestas más consistentes
    )
    
    respuesta = response.choices[0].message.content.strip()
    
    # Intentar parsear el JSON
    try:
        # Limpiar la respuesta por si tiene texto adicional
        if "```json" in respuesta:
            respuesta = respuesta.split("```json")[1].split("```")[0].strip()
        elif "```" in respuesta:
            respuesta = respuesta.split("```")[1].split("```")[0].strip()
        
        resultado = json.loads(respuesta)
        
        # Validar que tenga la estructura correcta
        if "clasificacion" not in resultado:
            raise ValueError("El JSON no contiene 'clasificacion'")
        
        # Validar que la categoría sea válida
        categoria = resultado["clasificacion"].lower()
        if categoria not in ["venta", "soporte", "reclamo"]:
            raise ValueError(f"Categoría inválida: {categoria}")
        
        # Normalizar a minúsculas
        resultado["clasificacion"] = categoria
        
        return resultado
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        print(f"Respuesta recibida: {respuesta}")
        return {"clasificacion": "soporte"}  # Valor por defecto
    except Exception as e:
        print(f"Error: {e}")
        return {"clasificacion": "soporte"}  # Valor por defecto


# Probar con los ejemplos
if __name__ == "__main__":
    print("=" * 60)
    print("CLASIFICACIÓN DE LLAMADAS")
    print("=" * 60)
    print()
    
    for i, llamada in enumerate(llamadas_ejemplo, 1):
        print(f"Llamada {i}: {llamada}")
        resultado = clasificar_llamada(llamada)
        print(f"Clasificación: {resultado['clasificacion']}")
        print(f"JSON: {json.dumps(resultado, ensure_ascii=False)}")
        print("-" * 60)
        print()
