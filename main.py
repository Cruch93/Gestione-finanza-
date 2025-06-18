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

# Menu principale
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

def analizza_bilancio():
    try:
        with open(file_csv, "r", newline="") as f:
            reader = csv.DictReader(f)
            tot_entrate = 0.0
            tot_uscite = 0.0
            tot_buoni = 0.0
            spese_per_categoria = defaultdict(float)

            for riga in reader:
                tot_entrate += float(riga["Entrata"] or 0)
                tot_uscite += float(riga["Uscita"] or 0)
                tot_buoni += float(riga["Buoni Pasto"] or 0)
                if riga["Categoria"]:
                    spese_per_categoria[riga["Categoria"]] += float(riga["Uscita"] or 0)

            print("\n📊 RIEPILOGO BILANCIO 📊")
            print(f"Totale entrate:  € {tot_entrate:.2f}")
            print(f"Totale uscite:   € {tot_uscite:.2f}")
            print(f"Buoni pasto:     € {tot_buoni:.2f}")
            print(f"Saldo netto:     € {tot_entrate - tot_uscite:.2f}")

            print("\n🗂️ Spese per categoria:")
            for cat, valore in spese_per_categoria.items():
                print(f"- {cat}: € {valore:.2f}")

    except FileNotFoundError:
        print("❌ File CSV non trovato. Inserisci almeno una voce prima.")
