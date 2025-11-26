"""
Servicio para clasificación automática de llamadas usando IA.
"""

from openai import OpenAI
import json
import os
from typing import Dict

# Configuración del cliente OpenAI (LM Studio)
CLIENT = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "lmstudio")
)

MODELO = os.getenv("OPENAI_MODEL", "openai/gpt-oss-20b")

# Prompt del sistema para clasificación
PROMPT_SISTEMA = """Eres un clasificador de llamadas. Tu única tarea es responder con un objeto JSON válido.

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
- "venta": ofertas, descuentos, cerrar ventas, promociones, enlaces de pago, planes premium
- "soporte": problemas técnicos, guías, verificación de servicios, reiniciar equipos, capturas de pantalla
- "reclamo": quejas, escalación a supervisor, registro de PQR, tono alterado, problemas formales

NO agregues explicaciones. NO uses markdown. Solo el JSON puro."""

PROMPT_CLASIFICACION = """Eres un sistema experto en clasificación de llamadas de call center.

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


def clasificar_llamada_con_ia(
    tipo_llamada: str,
    resultado_llamada: str,
    numero_cliente: str = "",
    duracion_segundos: int = 0
) -> Dict[str, any]:
    """
    Clasifica una llamada usando IA basándose en sus características.
    
    Args:
        tipo_llamada: Tipo de la llamada (venta, soporte, reclamo)
        resultado_llamada: Resultado de la llamada (atendida, colgada, resuelta, escalada)
        numero_cliente: Número del cliente (opcional)
        duracion_segundos: Duración en segundos (opcional)
        
    Returns:
        Diccionario con la clasificación y confianza:
        {
            "categoria": "venta|soporte|reclamo",
            "confianza": 0.0-1.0,
            "recomendacion_agente": "texto opcional"
        }
    """
    # Construir descripción de la llamada para el LLM
    descripcion = f"Tipo de llamada: {tipo_llamada}. Resultado: {resultado_llamada}"
    if duracion_segundos > 0:
        descripcion += f". Duración: {duracion_segundos} segundos"
    
    mensaje_completo = f"{PROMPT_CLASIFICACION}\n\n{descripcion}"
    
    try:
        response = CLIENT.chat.completions.create(
            model=MODELO,
            messages=[
                {
                    "role": "system",
                    "content": PROMPT_SISTEMA
                },
                {
                    "role": "user",
                    "content": mensaje_completo
                }
            ],
            temperature=0.1  # Baja temperatura para respuestas más consistentes
        )
        
        respuesta = response.choices[0].message.content.strip()
        
        # Limpiar y parsear el JSON
        if "```json" in respuesta:
            respuesta = respuesta.split("```json")[1].split("```")[0].strip()
        elif "```" in respuesta:
            respuesta = respuesta.split("```")[1].split("```")[0].strip()
        
        resultado = json.loads(respuesta)
        
        # Validar estructura
        if "clasificacion" not in resultado:
            raise ValueError("El JSON no contiene 'clasificacion'")
        
        # Validar y normalizar categoría
        categoria = resultado["clasificacion"].lower()
        if categoria not in ["venta", "soporte", "reclamo"]:
            raise ValueError(f"Categoría inválida: {categoria}")
        
        # Calcular confianza basada en qué tan bien coincide con el tipo original
        confianza = 0.85  # Confianza base
        if categoria == tipo_llamada.lower():
            confianza = 0.95  # Alta confianza si coincide
        elif resultado_llamada.lower() == "escalada":
            if categoria == "reclamo":
                confianza = 0.90
        elif resultado_llamada.lower() == "resuelta":
            if categoria == "soporte":
                confianza = 0.90
        
        # Generar recomendación basada en la clasificación
        recomendacion = generar_recomendacion(categoria, resultado_llamada)
        
        return {
            "categoria": categoria,
            "confianza": round(confianza, 2),
            "recomendacion_agente": recomendacion
        }
        
    except json.JSONDecodeError as e:
        # Si falla el parsing, usar el tipo de llamada como fallback
        categoria_fallback = tipo_llamada.lower() if tipo_llamada.lower() in ["venta", "soporte", "reclamo"] else "soporte"
        return {
            "categoria": categoria_fallback,
            "confianza": 0.70,
            "recomendacion_agente": f"Clasificación automática falló. Usando tipo de llamada: {categoria_fallback}"
        }
    except Exception as e:
        # Error general, usar fallback
        categoria_fallback = tipo_llamada.lower() if tipo_llamada.lower() in ["venta", "soporte", "reclamo"] else "soporte"
        return {
            "categoria": categoria_fallback,
            "confianza": 0.60,
            "recomendacion_agente": f"Error en clasificación IA: {str(e)}"
        }


def clasificar_texto_llamada(descripcion_textual: str) -> Dict[str, any]:
    """
    Clasifica una llamada basándose únicamente en su descripción textual.
    
    Args:
        descripcion_textual: Descripción textual de la llamada a clasificar
        
    Returns:
        Diccionario con la clasificación:
        {
            "categoria": "venta|soporte|reclamo",
            "confianza": 0.0-1.0,
            "recomendacion_agente": "texto opcional"
        }
    """
    mensaje_completo = f"{PROMPT_CLASIFICACION}\n\n{descripcion_textual}"
    
    try:
        response = CLIENT.chat.completions.create(
            model=MODELO,
            messages=[
                {
                    "role": "system",
                    "content": PROMPT_SISTEMA
                },
                {
                    "role": "user",
                    "content": mensaje_completo
                }
            ],
            temperature=0.1  # Baja temperatura para respuestas más consistentes
        )
        
        respuesta = response.choices[0].message.content.strip()
        
        # Limpiar y parsear el JSON
        if "```json" in respuesta:
            respuesta = respuesta.split("```json")[1].split("```")[0].strip()
        elif "```" in respuesta:
            respuesta = respuesta.split("```")[1].split("```")[0].strip()
        
        resultado = json.loads(respuesta)
        
        # Validar estructura
        if "clasificacion" not in resultado:
            raise ValueError("El JSON no contiene 'clasificacion'")
        
        # Validar y normalizar categoría
        categoria = resultado["clasificacion"].lower()
        if categoria not in ["venta", "soporte", "reclamo"]:
            raise ValueError(f"Categoría inválida: {categoria}")
        
        # Calcular confianza (base alta para clasificación por texto)
        confianza = 0.80
        
        # Ajustar confianza según palabras clave en la descripción
        descripcion_lower = descripcion_textual.lower()
        
        if categoria == "venta":
            palabras_venta = ["oferta", "descuento", "plan", "premium", "venta", "promoción", "pago", "comprar"]
            if any(palabra in descripcion_lower for palabra in palabras_venta):
                confianza = 0.90
        elif categoria == "soporte":
            palabras_soporte = ["reiniciar", "módem", "error", "problema", "técnico", "verificar", "cobertura", "solicitar"]
            if any(palabra in descripcion_lower for palabra in palabras_soporte):
                confianza = 0.90
        elif categoria == "reclamo":
            palabras_reclamo = ["escalar", "supervisor", "pqr", "queja", "reclamo", "tono alterado", "radicado"]
            if any(palabra in descripcion_lower for palabra in palabras_reclamo):
                confianza = 0.90
        
        # Generar recomendación genérica basada en la categoría
        recomendacion = generar_recomendacion_generica(categoria)
        
        return {
            "categoria": categoria,
            "confianza": round(confianza, 2),
            "recomendacion_agente": recomendacion
        }
        
    except json.JSONDecodeError as e:
        # Si falla el parsing, usar fallback
        return {
            "categoria": "soporte",
            "confianza": 0.70,
            "recomendacion_agente": "Error al parsear respuesta de IA. Clasificación por defecto: soporte"
        }
    except Exception as e:
        # Error general, usar fallback
        return {
            "categoria": "soporte",
            "confianza": 0.60,
            "recomendacion_agente": f"Error en clasificación IA: {str(e)}"
        }


def generar_recomendacion_generica(categoria: str) -> str:
    """
    Genera una recomendación genérica para el agente basada en la categoría.
    
    Args:
        categoria: Categoría de la llamada
        
    Returns:
        Recomendación para el agente
    """
    recomendaciones = {
        "venta": "Enfocarse en presentar las ventajas del producto/servicio y cerrar la venta de manera efectiva.",
        "soporte": "Proporcionar asistencia técnica detallada y asegurar que el problema se resuelva completamente.",
        "reclamo": "Escuchar activamente, mostrar empatía y trabajar hacia una solución que satisfaga al cliente."
    }
    
    return recomendaciones.get(categoria, "Seguir protocolo estándar de atención.")


def generar_recomendacion(categoria: str, resultado: str) -> str:
    """
    Genera una recomendación para el agente basada en la clasificación.
    
    Args:
        categoria: Categoría de la llamada
        resultado: Resultado de la llamada
        
    Returns:
        Recomendación para el agente
    """
    recomendaciones = {
        "venta": {
            "atendida": "Seguir el proceso de venta y cerrar la oferta.",
            "resuelta": "Venta completada exitosamente. Registrar seguimiento.",
            "colgada": "Llamada interrumpida. Programar callback para continuar venta.",
            "escalada": "Escalar a supervisor de ventas para apoyo en cierre."
        },
        "soporte": {
            "atendida": "Proporcionar asistencia técnica detallada al cliente.",
            "resuelta": "Problema resuelto. Documentar solución para futuras referencias.",
            "colgada": "Llamada interrumpida. Verificar si el problema se resolvió.",
            "escalada": "Escalar a técnico especializado para resolución avanzada."
        },
        "reclamo": {
            "atendida": "Escuchar activamente y registrar todos los detalles del reclamo.",
            "resuelta": "Reclamo resuelto. Confirmar satisfacción del cliente.",
            "colgada": "Llamada interrumpida. Seguimiento urgente requerido.",
            "escalada": "Escalar inmediatamente a supervisor para manejo del reclamo."
        }
    }
    
    return recomendaciones.get(categoria, {}).get(resultado.lower(), "Seguir protocolo estándar de atención.")

