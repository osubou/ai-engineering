import boto3
import json

client = boto3.client(
    service_name="bedrock-runtime",
    region_name="eu-north-1"
)

def llamar_claude(prompt, max_tokens=200, temperature=None, top_p=None):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    # Solo añade el parámetro que se especifica
    if temperature is not None:
        body["temperature"] = temperature
    if top_p is not None:
        body["top_p"] = top_p

    response = client.invoke_model(
        modelId="eu.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    texto = result["content"][0]["text"]
    usage = result["usage"]
    coste = (usage["input_tokens"] * 0.0000008) + (usage["output_tokens"] * 0.000004)

    print(f"RESPUESTA: {texto}")
    print(f"Input tokens: {usage['input_tokens']} | Output tokens: {usage['output_tokens']} | Coste: ${coste:.6f}")
    print("-" * 60)
    return texto


# ─── EXPERIMENTO 1: max_tokens ───────────────────────────────
print("\n=== EXPERIMENTO 1: max_tokens ===")
print("--- max_tokens=20 (respuesta muy corta) ---")
llamar_claude("Explícame qué es un LLM", max_tokens=20)

print("--- max_tokens=200 (respuesta normal) ---")
llamar_claude("Explícame qué es un LLM", max_tokens=200)


# ─── EXPERIMENTO 2: temperature ──────────────────────────────
print("\n=== EXPERIMENTO 2: temperature ===")
print("--- temperature=0.0 (muy predecible) ---")
llamar_claude("Escribe un haiku sobre Python", temperature=0.0)

print("--- temperature=0.0 (misma llamada, misma respuesta) ---")
llamar_claude("Escribe un haiku sobre Python", temperature=0.0)

print("--- temperature=1.0 (creativo) ---")
llamar_claude("Escribe un haiku sobre Python", temperature=1.0)

print("--- temperature=1.0 (respuesta diferente) ---")
llamar_claude("Escribe un haiku sobre Python", temperature=1.0)


# ─── EXPERIMENTO 3: top_p ────────────────────────────────────
print("\n=== EXPERIMENTO 3: top_p ===")
print("--- top_p=0.1 (vocabulario conservador) ---")
llamar_claude("Describe el mar", top_p=0.1)

print("--- top_p=0.999 (vocabulario amplio) ---")
llamar_claude("Describe el mar", top_p=0.999)


# ─── EXPERIMENTO 4: combinaciones reales ─────────────────────
print("\n=== EXPERIMENTO 4: casos de uso reales ===")

print("--- Chatbot de soporte (preciso) ---")
llamar_claude("¿Cuál es la política de devoluciones?", temperature=0.0, max_tokens=150)

print("--- Generador de ideas (creativo) ---")
llamar_claude("Dame una idea de negocio original", temperature=1.0, max_tokens=200)

print("--- Resumen de documento (equilibrado) ---")
llamar_claude("Resume en 2 frases qué hace un Data Engineer", temperature=0.3, max_tokens=100)