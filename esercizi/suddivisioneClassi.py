"""fare la suddivisione in classi di:

14 23 74 27 56 45 67 45 42 21 20 23 36 45 67 64 53 24 34 29 17
38 64 58 43 38 8 45 42 38 45 57 28 12 19 28 34 11 15 16 23 24
16 18 9 29 17 11 15 64 58 24 16 23 38 27 78 82 54 34 36 45 45
57 34 34 37 39 56 34 34 34 37 39 16 23 18 9 82

e poi calcolare valore centrale, frequenza assoluta e frequenza relativa e frequenza relativa in precentuale

"""
import pandas as pd

if __name__ == "__main__":
    dati = [
    14, 23, 74, 27, 56, 45, 67, 45, 42, 21, 20, 23, 36, 45, 67, 64, 53, 24, 34, 29, 17,
    38, 64, 58, 43, 38, 8, 45, 42, 38, 45, 57, 28, 12, 19, 28, 34, 11, 15, 16, 23, 24,
    16, 18, 9, 29, 17, 11, 15, 64, 58, 24, 16, 23, 38, 27, 78, 82, 54, 34, 36, 45, 45,
    57, 34, 34, 37, 39, 56, 34, 34, 34, 37, 39, 16, 23, 18, 9, 82
    ]
    classi = [0,12,18,50,70,100]
    df = pd.DataFrame(dati, columns=['Valore'])
    df['Classe'] = pd.cut(df['Valore'], bins=classi, right=False)


    tabella = df['Classe'].value_counts().sort_index().reset_index()
    tabella.columns = ['Classe', 'Freq_Assoluta']


    tabella['Valore_Centrale'] = tabella['Classe'].apply(lambda x: x.mid)

    totale = tabella['Freq_Assoluta'].sum()
    tabella['Freq_Relativa'] = tabella['Freq_Assoluta'] / totale


    tabella['Freq_Percentuale'] = tabella['Freq_Relativa'] * 100


    print(tabella[['Classe', 'Valore_Centrale', 'Freq_Assoluta', 'Freq_Relativa', 'Freq_Percentuale']])