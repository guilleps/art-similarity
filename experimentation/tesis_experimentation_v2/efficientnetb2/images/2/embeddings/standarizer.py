import json

def scale_distance(d, min_val, max_val):
    sim = 1 - ((d - min_val) / (max_val - min_val))
    return max(0.0, min(1.0, round(sim, 4)))

# 👉 Cargar archivo original con métricas
with open("resultados_similitud.json", "r") as f:
    data = json.load(f)

# 👉 Inicializar acumuladores
metricas = ["cosine_similarity", "euclidean_distance", "manhattan_distance", "mahalanobis_distance"]
valores = {m: [] for m in metricas}

# 👉 Recolectar todos los valores por métrica
for resultado in data.values():
    for metrica in metricas:
        valor = resultado[metrica]
        if valor != "undefined":
            valores[metrica].append(float(valor))

# 👉 Calcular min y max por métrica
rangos = {m: {"min": min(valores[m]), "max": max(valores[m])} for m in metricas}

# 👉 Imprimir rangos
print("📌 RANGOS POR MÉTRICA:")
print(json.dumps(rangos, indent=4))

# 👉 Estandarizar los valores
valores_estandarizados = {}
for key, resultado in data.items():
    valores_estandarizados[key] = {}
    for metrica in metricas:
        valor = resultado[metrica]
        if valor == "undefined":
            valores_estandarizados[key][metrica] = "undefined"
        else:
            scaled = scale_distance(float(valor), rangos[metrica]["min"], rangos[metrica]["max"])
            valores_estandarizados[key][metrica] = scaled

# 👉 Imprimir resultados estandarizados
print("\n📊 VALORES ESTANDARIZADOS POR TRANSFORMACIÓN:\n")
for transformacion, metricas_dict in valores_estandarizados.items():
    print(f"🔹 {transformacion}")
    for metrica, valor in metricas_dict.items():
        print(f"  {metrica}: {valor}")
    print()

# # 👉 (Opcional) Guardar en un nuevo archivo
# with open("resultados_similitud_estandarizados.json", "w") as f:
#     json.dump(valores_estandarizados, f, indent=4)
