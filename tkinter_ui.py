import tkinter as tk
from tkinter import messagebox
from lexer_logic import procesar_entrada

def procesar():
    entrada = entry.get()
    try:
        token_counts = procesar_entrada(entrada)
        text_area.delete('1.0', tk.END)
        for token_type, count in token_counts.items():
            text_area.insert(tk.END, f"Token: {token_type}, Conteo: {count}\n")
    except Exception as e:
        messagebox.showerror("Error de análisis", str(e))

root = tk.Tk()
root.title("Lyra: Analizador Léxico")

entry = tk.Entry(root, width=100)
entry.pack(padx=10, pady=10)

boton_procesar = tk.Button(root, text="PROCESAR", command=procesar)
boton_procesar.pack(padx=10, pady=10)

text_area = tk.Text(root, height=15, width=150)
text_area.pack(padx=10, pady=10)

root.mainloop()