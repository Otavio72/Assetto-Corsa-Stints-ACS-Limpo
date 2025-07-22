import os
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext, messagebox

PASTA_CSV = "DEMO/demo_stints"  # sua pasta com os CSVs

def mostrar_arquivo(nome_arquivo):
    caminho = os.path.join(PASTA_CSV, nome_arquivo)
    try:
        df = pd.read_csv(caminho, sep='\t')
    except Exception as e:
        messagebox.showerror("Erro ao abrir arquivo", f"Erro ao abrir {nome_arquivo}:\n{e}")
        return
    
    # Criar janela para mostrar dados
    janela_dados = tk.Toplevel()
    janela_dados.title(f"Conteúdo: {nome_arquivo}")
    janela_dados.geometry("600x400")

    texto = scrolledtext.ScrolledText(janela_dados)
    texto.pack(fill=tk.BOTH, expand=True)

    texto.insert(tk.END, df.head(20).to_string())  # mostra as 20 primeiras linhas
    texto.config(state=tk.DISABLED)

def criar_menu():
    root = tk.Tk()
    root.title("Menu de arquivos CSV")
    root.geometry("300x400")

    arquivos = [f for f in os.listdir(PASTA_CSV) if f.endswith(".csv")]

    label = tk.Label(root, text="Selecione um arquivo para abrir:")
    label.pack(pady=10)

    frame_botoes = tk.Frame(root)
    frame_botoes.pack(fill=tk.BOTH, expand=True)

    for arquivo in arquivos:
        btn = tk.Button(frame_botoes, text=arquivo, command=lambda a=arquivo: mostrar_arquivo(a))
        btn.pack(fill=tk.X, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    criar_menu()
