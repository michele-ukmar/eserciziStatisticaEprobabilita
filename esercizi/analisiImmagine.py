import numpy as np
from skimage import io
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dir_path = os.path.dirname(os.path.realpath(__file__))
image = io.imread(os.path.join(dir_path, "ciccio.jpg"))
image = image.astype(np.uint8)
# Stampa l'immagine
io.imshow(image)
io.show()
if image.shape[-1] == 4: # Se ha un canale alpha, rimuovilo
    image = image[:, :, :3]
elif image.ndim == 2: # Se è in scala di grigi, converti a RGB
    image = np.stack([image, image, image], axis=-1)

red = image[:, :, 0]
green = image[:, :, 1]
blue = image[:, :, 2]

total_pixels = red.size

warm_pixels = np.sum((red > green) & (red > blue))
cold_pixels = np.sum((blue > red) & (blue > green))
neutral_pixels = total_pixels - (warm_pixels + cold_pixels)

freq_assoluta = {
"Toni Caldi": warm_pixels,
"Toni Freddi": cold_pixels,
"Toni Neutri": neutral_pixels
}
freq_relativa = {}
percentuale = {}
for tone in ["Toni Caldi", "Toni Freddi", "Toni Neutri"]:
    freq_relativa[tone] = freq_assoluta[tone] / total_pixels
    percentuale[tone] = (freq_assoluta[tone] / total_pixels) * 100

print("\n--- Tabella di Distribuzione di Frequenza dei Toni di Colore ---")
print("{:<15} {:<20} {:<20} {:<15}".format("Classe", "Freq. Assoluta", "Freq. Relativa", "Percentuale"))
print("-" * 70)
for tone in ["Toni Caldi", "Toni Freddi", "Toni Neutri"]:
    print("{:<15} {:<20} {:<20.4f} {:<15.2f}%".format(
        tone,
        freq_assoluta[tone],
        freq_relativa[tone],
        percentuale[tone]
    ))
print("-" * 70)
print("{:<15} {:<20} {:<20.4f} {:<15.2f}%".format(
"Totale",
sum(freq_assoluta.values()),
sum(freq_relativa.values()),
sum(percentuale.values())
))

statistiche = {}
for nome, canale in [('Rosso', red), ('Verde', green), ('Blu', blue)]:
    statistiche[nome] = {
    'media': np.mean(canale),
    'mediana': np.median(canale),
    'dev_std': np.std(canale)
    }
    print(f"\nCanale {nome}:")
    print(f" Media: {statistiche[nome]['media']:.2f}")
    print(f" Mediana: {statistiche[nome]['mediana']:.2f}")
    print(f" Deviazione Standard: {statistiche[nome]['dev_std']:.2f}")

# 4. Identificare il colore dominante
media_rgb = [statistiche['Rosso']['media'],
statistiche['Verde']['media'],
statistiche['Blu']['media']]
colore_dominante = ['Rosso', 'Verde', 'Blu'][np.argmax(media_rgb)]
print(f"\nColore dominante: {colore_dominante}")

# 5. Creare grafico a barre per la distribuzione
fig, axes = plt.subplots(3, 3, figsize=(12, 10))

# Visualizzare l'immagine originale
axes[0, 0].imshow(image)
axes[0, 0].set_title('Immagine Originale')
axes[0, 0].axis('off')

# Grafico a barre delle medie
canali = ['Rosso', 'Verde', 'Blu']
medie = [statistiche[c]['media'] for c in canali]
axes[0, 1].bar(canali, medie, color=['red', 'green', 'blue'], alpha=0.7)
axes[0, 1].set_title('Media dei Canali RGB')
axes[0, 1].set_ylabel('Valore Medio')
axes[0, 1].set_ylim(0, 255)

bins = 50
max_freq = max(
    np.histogram(red.flatten(), bins=bins)[0].max(),
    np.histogram(green.flatten(), bins=bins)[0].max(),
    np.histogram(blue.flatten(), bins=bins)[0].max()
) * 1.1
# Istogrammi per ogni canale
for idx, (nome, canale, colore) in enumerate([
('Rosso', red, 'red'),
('Verde', green, 'green'),
('Blu', blue, 'blue')
]):
    if idx == 0:
        ax = axes[1, 0]
    elif idx == 1:
        ax = axes[1, 1]
    elif idx == 2:
        ax = axes[1, 2]
    else:
        # Aggiungere un terzo subplot
        ax = fig.add_subplot(3, 2, 6)  
    ax.hist(canale.flatten(), bins=50, color=colore, alpha=0.7)
    ax.set_title(f'Distribuzione Canale {nome}')
    ax.set_xlabel('Intensità')
    ax.set_ylabel('Frequenza')
    ax.set_xlim(0, 255)
    ax.set_ylim(0, max_freq)


# Istogrammi RGB sovrapposti
ax = axes[0, 2]
hist_r, bin_edges = np.histogram(red.flatten(), bins=bins, range=(0,255))
hist_g, _ = np.histogram(green.flatten(), bins=bins, range=(0,255))
hist_b, _ = np.histogram(blue.flatten(), bins=bins, range=(0,255))

bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

ax.plot(bin_centers, hist_r, color='red', label='Rosso')
ax.plot(bin_centers, hist_g, color='green', label='Verde')
ax.plot(bin_centers, hist_b, color='blue', label='Blu')
ax.set_title('Distribuzione Intensità RGB')
ax.set_xlabel('Intensità')
ax.set_ylabel('Frequenza')
ax.legend()


height, width, channels = image.shape
print(f"Dimensioni immagine: ({height}, {width}, {channels})")
print(f"Canale Rosso: Media: {statistiche['Rosso']['media']:.2f} Mediana: {statistiche['Rosso']['mediana']:.2f} Deviazione Standard: {statistiche['Rosso']['dev_std']:.2f}")
print(f"Canale Verde: Media: {statistiche['Verde']['media']:.2f} Mediana: {statistiche['Verde']['mediana']:.2f} Deviazione Standard: {statistiche['Verde']['dev_std']:.2f}")
print(f"Canale Blu: Media: {statistiche['Blu']['media']:.2f} Mediana: {statistiche['Blu']['mediana']:.2f} Deviazione Standard: {statistiche['Blu']['dev_std']:.2f}")



# Calcolare la covarianza tra i canali
covarianze = {
    "rosso - verde": np.cov(red.flatten(), green.flatten())[0, 1],
    "rosso - blu": np.cov(red.flatten(), blue.flatten())[0, 1],
    "verde - blu": np.cov(green.flatten(), blue.flatten())[0, 1]
}
print(f"\nCovarianza Canale Rosso-Verde: {covarianze['rosso - verde']:.2f}")
print(f"Covarianza Canale Rosso-Blu: {covarianze['rosso - blu']:.2f}")
print(f"Covarianza Canale Verde-Blu: {covarianze['verde - blu']:.2f}")
for coppia, valore in covarianze.items():
    print(f"{coppia}: {valore:.2f}")
    if valore > 0:
        print(" → I canali sono covarianti (variano concordemente).")
    elif valore < 0:
        print(" → I canali variano in modo discorde.")
    else:
        print(" → I canali non sono linearmente correlati.")
        
df = pd.DataFrame({
    'red': red.flatten(),
    'green': green.flatten(),
    'blue': blue.flatten()
})



for i, (colore, valori) in enumerate(df.items()):
    Q1 = df[f"{colore}"].quantile(0.25)
    Q2 = df[f"{colore}"].quantile(0.50)
    Q3 = df[f"{colore}"].quantile(0.75)
    print(f"\nPrimo Quartile (Q1): {Q1:.2f}")
    print(f"Secondo Quartile (Q2 - Mediana): {Q2:.2f}")
    print(f"Terzo Quartile (Q3): {Q3:.2f}")
    ax = axes[2, i]

    sns.boxplot(
        y=valori,
        ax=ax,
        color=colore.lower()
    )
    ax.set_title(f'Box Plot Canale {colore}')
    ax.set_ylabel('Intensità')
    ax.set_ylim(-25, 255 * 1.1)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
plt.tight_layout()
plt.show()
