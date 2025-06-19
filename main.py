import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Intestazioni CSV
INTESTAZIONI = ["ID", "DataVoce", "MeseRif", "Tipo", "Categoria", "Descrizione", "Importo", "BuoniPasto", "Fissa"]

# Categorie predefinite
CATEGORIE = {
    "entrata": ["Stipendio", "Rimborso", "Altro"],
    "uscita": ["Alimentari", "Casa", "Salute", "Trasporti", "Svago", "Mutuo", "Bollette", "Altro"]
}

# File CSV scelto
file_csv = None

def crea_nuovo_file():
    global file_csv
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if path:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(INTESTAZIONI)
        file_csv = path
        finestra_selezione.destroy()
        avvia_gui_principale()

def apri_file_esistente():
    global file_csv
    path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if path:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            intestazioni = next(reader, None)
            if intestazioni != INTESTAZIONI:
                messagebox.showerror("Errore", "Il file selezionato non ha il formato corretto.")
                return
        file_csv = path
        finestra_selezione.destroy()
        avvia_gui_principale()

def get_prossimo_id():
    try:
        with open(file_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            righe = list(reader)
            if not righe:
                return 1
            ultimo_id = max(int(r["ID"]) for r in righe)
            return ultimo_id + 1
    except:
        return 1

# === GUI Principale ===

def avvia_gui_principale():
    def salva_voce():
        tipo = tipo_var.get()
        categoria = categoria_var.get()
        descrizione = descrizione_entry.get()
        importo = importo_entry.get()
        buoni = buoni_entry.get() if tipo == "uscita" else ""
        fissa = "sì" if fissa_var.get() else "no"

        if not (mese_var.get() and tipo and categoria and importo):
            messagebox.showerror("Errore", "Compila tutti i campi obbligatori.")
            return

        try:
            importo = float(importo)
            if tipo == "uscita" and buoni:
                buoni = float(buoni)
            else:
                buoni = ""
        except ValueError:
            messagebox.showerror("Errore", "Importo o Buoni non validi.")
            return

        id_voce = get_prossimo_id()
        data_voce = datetime.now().strftime("%d/%m/%Y")
        riga = [id_voce, data_voce, mese_var.get(), tipo, categoria, descrizione, importo, buoni, fissa]

        with open(file_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(riga)

        messagebox.showinfo("Successo", "Voce salvata correttamente!")
        descrizione_entry.delete(0, tk.END)
        importo_entry.delete(0, tk.END)
        buoni_entry.delete(0, tk.END)
        categoria_var.set("")
        tipo_var.set("")
        fissa_var.set(False)

    def aggiorna_categorie(*args):
        tipo = tipo_var.get()
        categoria_menu['menu'].delete(0, 'end')
        if tipo in CATEGORIE:
            for cat in CATEGORIE[tipo]:
                categoria_menu['menu'].add_command(label=cat, command=tk._setit(categoria_var, cat))

    root = tk.Tk()
    root.title("Gestione Bilancio Familiare")

    # Mese
    tk.Label(root, text="📅 Mese di riferimento (es. 06):").grid(row=0, column=0, sticky="w")
    global mese_var
    mese_var = tk.StringVar()
    tk.Entry(root, textvariable=mese_var, width=5).grid(row=0, column=1)

    # Tipo
    tk.Label(root, text="Tipo:").grid(row=1, column=0, sticky="w")
    tipo_var = tk.StringVar()
    tipo_menu = ttk.OptionMenu(root, tipo_var, "", "entrata", "uscita", command=aggiorna_categorie)
    tipo_menu.grid(row=1, column=1)

    # Categoria
    tk.Label(root, text="Categoria:").grid(row=2, column=0, sticky="w")
    categoria_var = tk.StringVar()
    categoria_menu = ttk.OptionMenu(root, categoria_var, "")
    categoria_menu.grid(row=2, column=1)

    # Descrizione
    tk.Label(root, text="Descrizione:").grid(row=3, column=0, sticky="w")
    descrizione_entry = tk.Entry(root, width=30)
    descrizione_entry.grid(row=3, column=1)

    # Importo
    tk.Label(root, text="Importo (€):").grid(row=4, column=0, sticky="w")
    importo_entry = tk.Entry(root, width=15)
    importo_entry.grid(row=4, column=1)

    # Buoni pasto
    tk.Label(root, text="Buoni pasto (se usati):").grid(row=5, column=0, sticky="w")
    buoni_entry = tk.Entry(root, width=10)
    buoni_entry.grid(row=5, column=1)

    # Spesa fissa
    fissa_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Spesa fissa?", variable=fissa_var).grid(row=6, column=0, sticky="w")

    # Bottone aggiunta
    tk.Button(root, text="➕ Aggiungi Voce", command=salva_voce).grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()

# === FINESTRA INIZIALE SELEZIONE FILE ===
finestra_selezione = tk.Tk()
finestra_selezione.title("Apri o crea file CSV")

tk.Label(finestra_selezione, text="Benvenuto! Seleziona un file bilancio da usare:").pack(pady=10)

tk.Button(finestra_selezione, text="📂 Apri file esistente", width=25, command=apri_file_esistente).pack(pady=5)
tk.Button(finestra_selezione, text="🆕 Crea nuovo file", width=25, command=crea_nuovo_file).pack(pady=5)

finestra_selezione.mainloop()
