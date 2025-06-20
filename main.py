import csv
import os
import pandas as pd
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

def apri_finestra_bilancio():
    def aggiorna_riepilogo(*args):
        mese = mese_var.get()
        if not mese:
            return

        try:
            df = pd.read_csv(file_csv)
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile leggere il file: {e}")
            return

        df = df[df["MeseRif"].astype(str) == mese]

        for row in tree.get_children():
            tree.delete(row)

        for _, riga in df.iterrows():
            tree.insert("", "end", values=list(riga[["ID", "DataVoce", "Tipo", "Categoria", "Descrizione", "Importo", "BuoniPasto", "Fissa"]]))

        entrate = df[df["Tipo"] == "entrata"]["Importo"].sum()
        uscite = df[df["Tipo"] == "uscita"]["Importo"].sum()
        buoni = df["BuoniPasto"].fillna(0).sum()
        saldo = entrate - uscite

        label_totali.config(text=(
            f"Entrate: € {entrate:.2f} | "
            f"Uscite: € {uscite:.2f} | "
            f"Buoni Pasto: € {buoni:.2f} | "
            f"Saldo: € {saldo:.2f}"
        ))

        riepilogo = df[df["Tipo"] == "uscita"].groupby("Categoria")["Importo"].sum().sort_values(ascending=False)
        txt = "\n".join([f"{cat}: € {imp:.2f}" for cat, imp in riepilogo.items()])
        text_categorie.delete("1.0", tk.END)
        text_categorie.insert(tk.END, txt)

    win = tk.Toplevel()
    win.title("📊 Riepilogo Bilancio Mensile")

    tk.Label(win, text="Seleziona mese (es. 06):").grid(row=0, column=0, sticky="w")
    mese_var = tk.StringVar()
    mese_entry = tk.Entry(win, textvariable=mese_var, width=5)
    mese_entry.grid(row=0, column=1, sticky="w")
    mese_var.trace("w", aggiorna_riepilogo)

    cols = ["ID", "DataVoce", "Tipo", "Categoria", "Descrizione", "Importo", "BuoniPasto", "Fissa"]
    tree = ttk.Treeview(win, columns=cols, show="headings", height=10)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    label_totali = tk.Label(win, text="Totali...", font=("Arial", 10, "bold"))
    label_totali.grid(row=2, column=0, columnspan=3, pady=5)

    tk.Label(win, text="Uscite per categoria:").grid(row=3, column=0, sticky="w")
    text_categorie = tk.Text(win, height=8, width=40)
    text_categorie.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

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

    tk.Label(root, text="📅 Mese di riferimento (es. 06):").grid(row=0, column=0, sticky="w")
    global mese_var
    mese_var = tk.StringVar()
    tk.Entry(root, textvariable=mese_var, width=5).grid(row=0, column=1)

    tk.Label(root, text="Tipo:").grid(row=1, column=0, sticky="w")
    tipo_var = tk.StringVar()
    tipo_menu = ttk.OptionMenu(root, tipo_var, "", "entrata", "uscita", command=aggiorna_categorie)
    tipo_menu.grid(row=1, column=1)

    tk.Label(root, text="Categoria:").grid(row=2, column=0, sticky="w")
    categoria_var = tk.StringVar()
    categoria_menu = ttk.OptionMenu(root, categoria_var, "")
    categoria_menu.grid(row=2, column=1)

    tk.Label(root, text="Descrizione:").grid(row=3, column=0, sticky="w")
    descrizione_entry = tk.Entry(root, width=30)
    descrizione_entry.grid(row=3, column=1)

    tk.Label(root, text="Importo (€):").grid(row=4, column=0, sticky="w")
    importo_entry = tk.Entry(root, width=15)
    importo_entry.grid(row=4, column=1)

    tk.Label(root, text="Buoni pasto (se usati):").grid(row=5, column=0, sticky="w")
    buoni_entry = tk.Entry(root, width=10)
    buoni_entry.grid(row=5, column=1)

    fissa_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Spesa fissa?", variable=fissa_var).grid(row=6, column=0, sticky="w")

    tk.Button(root, text="➕ Aggiungi Voce", command=salva_voce).grid(row=7, column=0, columnspan=2, pady=10)
    tk.Button(root, text="📊 Visualizza bilancio", command=apri_finestra_bilancio).grid(row=8, column=0, columnspan=2, pady=5)

    root.mainloop()

# === FINESTRA INIZIALE SELEZIONE FILE ===
finestra_selezione = tk.Tk()
finestra_selezione.title("Apri o crea file CSV")

tk.Label(finestra_selezione, text="Benvenuto! Seleziona un file bilancio da usare:").pack(pady=10)

tk.Button(finestra_selezione, text="📂 Apri file esistente", width=25, command=apri_file_esistente).pack(pady=5)
tk.Button(finestra_selezione, text="🆕 Crea nuovo file", width=25, command=crea_nuovo_file).pack(pady=5)

finestra_selezione.mainloop()
