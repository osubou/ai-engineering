import boto3
import json

client = boto3.client(
    service_name="bedrock-runtime",
    region_name="eu-north-1"
)

response = client.invoke_model(
# Pruebas y aprendizaje
#"eu.anthropic.claude-haiku-4-5-20251001-v1:0"

# Proyectos reales (Fase 2 en adelante)
#"eu.anthropic.claude-sonnet-4-5-20251001-v1:0"
    modelId="eu.anthropic.claude-haiku-4-5-20251001-v1:0",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": "Di hola en español"}
        ]
    })
)

result = json.loads(response["body"].read())
print(result["content"][0]["text"])

usage = result["usage"]
input_tokens = usage["input_tokens"]
output_tokens = usage["output_tokens"]
coste = (input_tokens * 0.0000008) + (output_tokens * 0.000004)

print(f"\n--- Uso ---")
print(f"Input tokens:  {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Coste llamada: ${coste:.6f}")