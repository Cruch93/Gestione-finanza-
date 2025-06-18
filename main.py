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
        print("2. Esci")
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            aggiungi_voce()
        elif scelta == "2":
            print("Uscita dal programma.")
            break
        else:
            print("⚠️ Scelta non valida. Riprova.")
