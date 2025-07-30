import pandas as pd
import matplotlib.pyplot as plt

# Leer el CSV con la columna 'phase'
df = pd.read_csv("EfficientNetB0_Training_Metrics.csv")

# Agrupar por fase y época tomando el último valor de cada métrica por época
df_grouped = df.groupby(["phase", "epoch"]).last().reset_index()

# Colores por fase para consistencia visual
colors = {1: "blue", 2: "orange", 3: "green"}

# --- Accuracy ---
plt.figure(figsize=(10, 6))
for phase in sorted(df_grouped["phase"].unique()):
    subset = df_grouped[df_grouped["phase"] == phase]
    plt.plot(subset["epoch"], subset["train_accuracy"], label=f"Fase {phase} - Train", marker="o", color=colors[phase])
    if "val_accuracy" in subset.columns and subset["val_accuracy"].notna().any():
        plt.plot(subset["epoch"], subset["val_accuracy"], label=f"Fase {phase} - Val", marker="o", linestyle="--", color=colors[phase])
plt.title("Accuracy por Fase y Época")
plt.xlabel("Época")
plt.ylabel("Precisión")
plt.legend()
plt.grid(True)
plt.savefig("accuracy_by_phase_b0.png")
plt.close()

# --- Loss ---
plt.figure(figsize=(10, 6))
for phase in sorted(df_grouped["phase"].unique()):
    subset = df_grouped[df_grouped["phase"] == phase]
    plt.plot(subset["epoch"], subset["train_loss"], label=f"Fase {phase} - Train", marker="o", color=colors[phase])
    if "val_loss" in subset.columns and subset["val_loss"].notna().any():
        plt.plot(subset["epoch"], subset["val_loss"], label=f"Fase {phase} - Val", marker="o", linestyle="--", color=colors[phase])
plt.title("Loss por Fase y Época")
plt.xlabel("Época")
plt.ylabel("Pérdida")
plt.legend()
plt.grid(True)
plt.savefig("loss_by_phase_b0.png")
plt.close()

# --- Silhouette ---
if "silhouette" in df_grouped.columns and df_grouped["silhouette"].notna().any():
    plt.figure(figsize=(10, 6))
    for phase in sorted(df_grouped["phase"].unique()):
        subset = df_grouped[df_grouped["phase"] == phase]
        plt.plot(subset["epoch"], subset["silhouette"], label=f"Fase {phase}", marker="o", color=colors[phase])
    plt.title("Silhouette por Fase y Época")
    plt.xlabel("Época")
    plt.ylabel("Silhouette")
    plt.grid(True)
    plt.legend()
    plt.savefig("silhouette_by_phase_b0.png")
    plt.close()

# --- P@5 ---
if "p@5" in df_grouped.columns and df_grouped["p@5"].notna().any():
    plt.figure(figsize=(10, 6))
    for phase in sorted(df_grouped["phase"].unique()):
        subset = df_grouped[df_grouped["phase"] == phase]
        plt.plot(subset["epoch"], subset["p@5"], label=f"Fase {phase}", marker="o", color=colors[phase])
    plt.title("P@5 por Fase y Época")
    plt.xlabel("Época")
    plt.ylabel("Precisión en Top 5")
    plt.grid(True)
    plt.legend()
    plt.savefig("p_at_5_by_phase_b0.png")
    plt.close()

print("✅ Gráficos generados por fase correctamente.")

# Filtrar solo Fase 3
df_fase3 = df_grouped[df_grouped["phase"] == 3]

# Eliminar filas con NaN en las métricas clave
df_fase3_valid = df_fase3.dropna(subset=["val_loss", "val_accuracy", "p@5"])

# Verifica si quedó alguna fila válida
if not df_fase3_valid.empty:
    # Tomar la última época válida
    fila_final = df_fase3_valid[df_fase3_valid["epoch"] == df_fase3_valid["epoch"].max()]
    
    val_loss_final = fila_final["val_loss"].values[0]
    val_accuracy_final = fila_final["val_accuracy"].values[0]
    p_at_5_final = fila_final["p@5"].values[0]

    print("\n--- MÉTRICAS EXTRAÍDAS PARA INDICADORES ---")
    print(f"Val Loss (Fase 3): {val_loss_final:.4f}")
    print(f"Val Accuracy (Fase 3): {val_accuracy_final:.4f}")
    print(f"P@5 (Fase 3): {p_at_5_final:.4f}")
else:
    print("⚠️ No se encontraron datos válidos para Fase 3 con métricas completas.")
