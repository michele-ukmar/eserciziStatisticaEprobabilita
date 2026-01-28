import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Generazione di dati di esempio
# Utilizziamo dati simili all'anzianità lavorativa trattata in precedenza
np.random.seed(42) # per riproducibilità
data = {'Anzianità Lavorativa': np.random.normal(loc=15, scale=7, size=100)}
df = pd.DataFrame(data)

print("Prime 5 righe del dataset:")
print(df.head())

# 2. Calcolo dei Percentili
# Calcoliamo il 25°, 50° (mediana), 75° e 95° percentile
percentili = df['Anzianità Lavorativa'].quantile([0.25, 0.5, 0.75, 0.95])
print("\nPercentili calcolati:")
print(percentili)

# 3. Calcolo dei Quartili specifici
Q1 = df['Anzianità Lavorativa'].quantile(0.25)
Q2 = df['Anzianità Lavorativa'].quantile(0.50) # La Mediana
Q3 = df['Anzianità Lavorativa'].quantile(0.75)
print(f"\nPrimo Quartile (Q1): {Q1:.2f}")
print(f"Secondo Quartile (Q2 - Mediana): {Q2:.2f}")
print(f"Terzo Quartile (Q3): {Q3:.2f}")

# 4. Visualizzazioni
# Save plots to files
plt.figure(figsize=(8, 6))
sns.boxplot(y=df['Anzianità Lavorativa'])
plt.title('Box Plot dell\'Anzianità Lavorativa')
plt.ylabel('Anzianità Lavorativa (Anni)')
plt.grid(axis='y', linestyle='--', alpha=0.7)


plt.figure(figsize=(10, 6))
sns.histplot(df['Anzianità Lavorativa'], kde=True, bins=10)
plt.title('Distribuzione dell\'Anzianità Lavorativa')
plt.xlabel('Anzianità Lavorativa (Anni)')
plt.ylabel('Frequenza')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
print("Plots saved as 'boxplot_anzianita.png' and 'histogram_anzianita.png'")