import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv("resultats_grid_search.csv")

# Nettoyer / Filtrer
df_filtered = df[df["taux"] > 0.0]

# Mettez la valeur présente dans votre CSV (0 d'après vos exemples)
norm_val = 1
sub_df = df_filtered[df_filtered["normalized"] == norm_val]

# Vérifier qu'il y a bien des données avant de tracer
if sub_df.empty:
    print(f"Attention : Aucune donnée trouvée pour normalized = {norm_val}. Vérifiez votre CSV.")
else:
    # Agréger
    df_agg = sub_df.groupby(["ratio", "taux"]).agg({
        "accAfter": "max",
        "FP": "mean",
        "FN": "mean"
    }).reset_index()

    metric_to_plot = "accAfter" # Ou "FP" / "FN"
    pivot_table = df_agg.pivot(index="ratio", columns="taux", values=metric_to_plot)

    # Affichage de la Heatmap
    plt.figure(figsize=(9, 6))
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5, cbar_kws={'label': metric_to_plot})

    plt.title(f"Heatmap de {metric_to_plot} selon le Taux et le Ratio (Normalisé = {norm_val})")
    plt.xlabel("Taux d'apprentissage")
    plt.ylabel("Ratio d'entraînement")
    plt.show()