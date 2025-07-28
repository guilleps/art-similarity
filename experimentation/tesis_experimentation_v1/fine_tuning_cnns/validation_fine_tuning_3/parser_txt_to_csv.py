import re
import pandas as pd

log_path = "training_log_efficientnetb0.txt"
with open(log_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Inicializar listas
data = []

# Patrón
epoch_pattern = re.compile(r"Epoch (\d+)/\d+")
metrics_pattern = re.compile(r"accuracy: ([\d.]+) - loss: ([\d.]+)(?: - val_accuracy: ([\d.]+) - val_loss: ([\d.]+))?(?: - learning_rate: ([\d.]+))?")
eval_pattern = re.compile(r"\[Epoch Eval\] Silhouette=([-\d.]+), P@5=([\d.]+)")

# Variables temporales
current_epoch = None
phase = 1
epoch_counter = 0
pending_eval = {}

for line in lines:
    if "Epoch" in line:
        match = epoch_pattern.search(line)
        if match:
            current_epoch = int(match.group(1))
            epoch_counter += 1
            phase = 1 + (epoch_counter - 1) // 5

    if metrics_pattern.search(line):
        m = metrics_pattern.search(line)
        acc = float(m.group(1))
        loss = float(m.group(2))
        val_acc = float(m.group(3)) if m.group(3) else None
        val_loss = float(m.group(4)) if m.group(4) else None
        lr = float(m.group(5)) if m.group(5) else None

        # Añadir fila con datos conocidos
        row = {
            "epoch": current_epoch,
            "train_accuracy": acc,
            "train_loss": loss,
            "val_accuracy": val_acc,
            "val_loss": val_loss,
            "learning_rate": lr,
            "silhouette": None,
            "p@5": None,
            "phase": phase
        }

        # Si hay evaluación pendiente, adjuntarla aquí
        if current_epoch in pending_eval:
            row["silhouette"] = pending_eval[current_epoch]["silhouette"]
            row["p@5"] = pending_eval[current_epoch]["p@5"]
            del pending_eval[current_epoch]

        data.append(row)

    if eval_pattern.search(line):
        m = eval_pattern.search(line)
        sil = float(m.group(1))
        p5 = float(m.group(2))
        # Guardar temporalmente la evaluación hasta encontrar la línea con epoch
        if current_epoch is not None:
            pending_eval[current_epoch] = {"silhouette": sil, "p@5": p5}

# Crear y mostrar el DataFrame
df = pd.DataFrame(data)
print(df.head())  # Verifica los primeros registros
df.to_csv("EfficientNetB0_Training_Metrics_FIXED.csv", index=False)
