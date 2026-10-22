import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
df = pd.read_csv("001epoques500.csv")

# Filtrer pour une configuration spécifique si vous le souhaitez (ex: normalized = 1 et un ratio fixe)
norm_val = 1
fixed_ratio = 0.8  # Vous pouvez changer le ratio à observer
sub_df = df[(df["normalized"] == norm_val) & (df["ratio"] == fixed_ratio)]

if sub_df.empty:
    print("Aucune donnée trouvée pour ces filtres.")
else:
    plt.figure(figsize=(10, 6))
    
    # On sélectionne quelques taux d'apprentissage intéressants à comparer pour ne pas surcharger le graphe
    taux_to_plot = [0.01, 0.03, 0.05, 0.08, 0.1]
    filtered_taux = sub_df[sub_df["taux"].isin(taux_to_plot)]

    # Tracer l'accuracy en fonction des époques réelles pour chaque taux
    sns.lineplot(
        data=filtered_taux, 
        x="epoques_demandes", # ou epoques_reels
        y="accAfter", 
        hue="taux", 
        palette="viridis", 
        linewidth=2.5
    )

    plt.title(f"Progression de l'Accuracy selon les Époques (Ratio = {fixed_ratio}, Norm = {norm_val})")
    plt.xlabel("Nombre d'époques")
    plt.ylabel("Accuracy après entraînement (accAfter)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(title="Taux d'apprentissage")
    plt.show()