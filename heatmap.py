import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv("001epoques500clean.csv")

# Nettoyer / Filtrer
df_filtered = df[df["taux"] > 0.0]
norm_val = 1
sub_df = df_filtered[df_filtered["normalized"] == norm_val]

if sub_df.empty:
    print(f"Attention : Aucune donnée trouvée pour normalized = {norm_val}. Vérifiez votre CSV.")
else:
    # -------------------------------------------------------------------------
    # HEATMAP 1 : Précision finale (accAfter) - INCHANGÉE
    # -------------------------------------------------------------------------
    df_agg_acc = sub_df.groupby(["ratio", "taux"]).agg({
        "accAfter": "max",
        "FP": "mean",
        "FN": "mean"
    }).reset_index()

    metric_to_plot_1 = "accAfter"
    pivot_table_acc = df_agg_acc.pivot(index="ratio", columns="taux", values=metric_to_plot_1)

    plt.figure(figsize=(9, 6))
    sns.heatmap(pivot_table_acc, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5, cbar_kws={'label': metric_to_plot_1})
    plt.title(f"Heatmap de {metric_to_plot_1} selon le Taux et le Ratio (Normalisé = {norm_val})")
    plt.xlabel("Taux d'apprentissage")
    plt.ylabel("Ratio d'entraînement")
    plt.show()

    # -------------------------------------------------------------------------
    # HEATMAP 2 : Nombre de cycles (époques réelles) nécessaires
    # -------------------------------------------------------------------------
    # Utiliser "max" permet de récupérer l'époque réelle atteinte lors du run complet
    df_agg_epochs = sub_df.groupby(["ratio", "taux"]).agg({
        "epoques_reels": "max"
    }).reset_index()

    metric_to_plot_2 = "epoques_reels"
    pivot_table_epochs = df_agg_epochs.pivot(index="ratio", columns="taux", values=metric_to_plot_2)

    plt.figure(figsize=(9, 6))
    sns.heatmap(pivot_table_epochs, annot=True, cmap="Oranges", fmt=".0f", linewidths=.5, cbar_kws={'label': "Nombre d'époques"})
    plt.title(f"Vitesse de convergence : Époques nécessaires selon le Taux et le Ratio (Normalisé = {norm_val})")
    plt.xlabel("Taux d'apprentissage")
    plt.ylabel("Ratio d'entraînement")
    plt.show()