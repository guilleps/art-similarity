import pandas as pd
import matplotlib.pyplot as plt

# Leer el CSV con la columna 'phase'
df = pd.read_csv("EfficientNetB2_Training_Metrics.csv")

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
plt.savefig("accuracy_by_phase_b2.png")
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
plt.savefig("loss_by_phase_b2.png")
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
    plt.savefig("silhouette_by_phase_b2.png")
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
    plt.savefig("p_at_5_by_phase_b2.png")
    plt.close()

print("✅ Gráficos generados por fase correctamente.")
