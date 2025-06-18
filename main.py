import csv
from datetime import datetime

# File CSV di destinazione
file_csv = "bilancio_familiare.csv"
intestazioni = ["Data", "Categoria", "Descrizione", "Entrata", "Uscita", "Buoni Pasto"]

# Crea file con intestazioni se non esiste
try:
    with open(file_csv, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(intestazioni)
except FileExistsError:
    pass

# Funzione per aggiungere voce
def aggiungi_voce():
    print("\nAggiunta nuova voce")
    data = input("Inserisci la data (gg/mm/aaaa) [lascia vuoto per oggi]: ")
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")

    categoria = input("Categoria (es. Casa, Alimentari, ecc.): ")
    descrizione = input("Descrizione: ")

    try:
        entrata = float(input("Entrata (0 se non presente): "))
    except ValueError:
        entrata = 0.0

    try:
        uscita = float(input("Uscita (0 se non presente): "))
    except ValueError:
        uscita = 0.0

    try:
        buoni = float(input("Buoni pasto utilizzati (0 se non presenti): "))
    except ValueError:
        buoni = 0.0

    with open(file_csv, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data, categoria, descrizione, entrata, uscita, buoni])

    print("✅ Voce aggiunta correttamente!")
    
#funzione per analizzare il bilancio
import pandas as pd

def analizza_bilancio():
    try:
        df = pd.read_csv(file_csv)

        # Conversione valori a numerici (se ci sono errori)
        df["Entrata"] = pd.to_numeric(df["Entrata"], errors="coerce").fillna(0)
        df["Uscita"] = pd.to_numeric(df["Uscita"], errors="coerce").fillna(0)
        df["Buoni Pasto"] = pd.to_numeric(df["Buoni Pasto"], errors="coerce").fillna(0)

        print("\n📊 RIEPILOGO GENERALE")
        print(f"Totale entrate:  € {df['Entrata'].sum():.2f}")
        print(f"Totale uscite:   € {df['Uscita'].sum():.2f}")
        print(f"Totale buoni:    € {df['Buoni Pasto'].sum():.2f}")
        print(f"Saldo netto:     € {(df['Entrata'].sum() - df['Uscita'].sum()):.2f}")

        print("\n🗂️ Totale uscite per categoria:")
        print(df.groupby("Categoria")["Uscita"].sum().sort_values(ascending=False))

    except FileNotFoundError:
        print("❌ File CSV non trovato.")
    except pd.errors.EmptyDataError:
        print("❌ Il file è vuoto.")
if __name__ == "__main__":
    while True:
        print("\n--- MENU ---")
        print("1. Aggiungi voce")
        print("2. Visualizza bilancio")
        print("3. Esci")
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            aggiungi_voce()
        elif scelta == "2":
            analizza_bilancio()
        elif scelta == "3":
            print("Uscita dal programma.")
            break
        else:
            print("⚠️ Scelta non valida. Riprova.")

from collections import defaultdict


