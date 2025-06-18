
import tkinter as tk
from tkinter import ttk, messagebox

class BilancioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Finanze Familiari")

        # Categorie fisse
        self.categorie = ["Spese Alimentari", "Spese Casa", "Varie", "Abbigliamento", "Auto", "Rifornimenti", "Sanità", "Uscite"]

        # Etichetta e menu categoria
        tk.Label(root, text="Categoria:").grid(row=0, column=0, padx=10, pady=10)
        self.categoria_var = tk.StringVar()
        self.categoria_menu = ttk.Combobox(root, textvariable=self.categoria_var, values=self.categorie, state="readonly")
        self.categoria_menu.grid(row=0, column=1)

        # Etichetta e campo descrizione
        tk.Label(root, text="Descrizione:").grid(row=1, column=0, padx=10, pady=10)
        self.descrizione_entry = tk.Entry(root)
        self.descrizione_entry.grid(row=1, column=1)

        # Etichetta e campo importo
        tk.Label(root, text="Importo (€):").grid(row=2, column=0, padx=10, pady=10)
        self.importo_entry = tk.Entry(root)
        self.importo_entry.grid(row=2, column=1)

        # Pulsante aggiungi
        self.aggiungi_btn = tk.Button(root, text="Aggiungi Spesa", command=self.aggiungi_spesa)
        self.aggiungi_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def aggiungi_spesa(self):
        categoria = self.categoria_var.get()
        descrizione = self.descrizione_entry.get()
        importo = self.importo_entry.get()
        try:
            importo = float(importo)
            messagebox.showinfo("Conferma", f"Aggiunto: {categoria} - {descrizione} - {importo:.2f} €")
            self.descrizione_entry.delete(0, tk.END)
            self.importo_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un importo valido!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BilancioApp(root)
    root.mainloop()
