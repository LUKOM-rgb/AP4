# Lucas Silva
# 40240224

import customtkinter
from tkinter import ttk, messagebox  # Treeview e mensagens
from PIL import Image, ImageTk
import os

# Caminho do ficheiro  meses
ficheiro_meses = ".\\files\\meses.txt"

# Função para ler o ficheiro  meses
def ler_ficheiro_meses():
    if not os.path.exists(ficheiro_meses):
        return []
    with open(ficheiro_meses, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f.readlines()]

# Função para carregar as despesas de um mês
def carregar_despesas(mes):
    ficheiro_despesas = f".\\files\\{mes}.txt"
    if not os.path.exists(ficheiro_despesas):
        return None
    with open(ficheiro_despesas, "r", encoding="utf-8") as f:
        despesas = [linha.strip().split(";") for linha in f.readlines()]
    return despesas

# Função para configurar a janela principal
def renderWindow(app, appWidth, appHeight, appTitle):
    app.title(appTitle)
    screenWidth = app.winfo_screenwidth()
    screenHeight = app.winfo_screenheight()
    x = (screenWidth // 2) - (appWidth // 2)
    y = (screenHeight // 2) - (appHeight // 2)
    app.geometry(f"{appWidth}x{appHeight}+{x}+{y}")
    app.resizable(False, False)

# Callback para o botão Consultar
def consultar():
    # Limpar o anterior
    for item in tree.get_children():
        tree.delete(item)

    mes_selecionado = mes.get()
    tipo_selecionado = rbState.get()

    if not mes_selecionado:
        messagebox.showwarning("Aviso", "Não selecionou um mês")
        return

    despesas = carregar_despesas(mes_selecionado)

    if despesas is None:
        messagebox.showerror("Erro", "Não existem despesas para este mês .")
        return

    despesas_filtradas = [
        despesa for despesa in despesas
        if tipo_selecionado == "Todas" or despesa[2] == tipo_selecionado
    ]

    for despesa in despesas_filtradas:
        tree.insert("", "end", values=despesa)

    # Calcular o total das despesas
    total_despesas = len(despesas_filtradas)
    valor_total = sum(float(despesa[1]) for despesa in despesas_filtradas)

    lblNumDespesas.configure(text=str(total_despesas))
    lblValorTotal.configure(text=f"{valor_total:n}")


app = customtkinter.CTk()
renderWindow(app, 450, 550, "DespesasApp")

# Frame 1 
frame1 = customtkinter.CTkFrame(app, width=430, height=170, fg_color="gray")
frame1.place(x=10, y=10)

labelMes = customtkinter.CTkLabel(frame1, text="Mês de Consulta de Despesas:")
labelMes.place(x=20, y=10)

mes = customtkinter.StringVar()
comboboxMes = customtkinter.CTkComboBox(
    frame1, values=ler_ficheiro_meses(), height=12, variable=mes)
comboboxMes.place(x=250, y=10)

rbState = customtkinter.StringVar(value="Todas")  # Opção padrão
rb1 = customtkinter.CTkRadioButton(frame1, text="Dinheiro", variable=rbState, value="Dinheiro")
rb2 = customtkinter.CTkRadioButton(frame1, text="Crédito", variable=rbState, value="Credito")
rb3 = customtkinter.CTkRadioButton(frame1, text="Todas", variable=rbState, value="Todas")
rb1.place(x=20, y=60)
rb2.place(x=20, y=90)
rb3.place(x=20, y=120)

# imagem da lupa
lupa_image = Image.open(".\\images\\lupa.png").resize((60, 60))
lupa_photo = ImageTk.PhotoImage(lupa_image)

btnConsultar = customtkinter.CTkButton(frame1, width=150, height=70, text="Consultar", text_color="cyan", image=lupa_photo, compound="right", command=consultar)
btnConsultar.place(x=235, y=70)

# Frame 2 
frame2 = customtkinter.CTkFrame(app, width=430, height=320)
frame2.place(x=10, y=200)

tree = ttk.Treeview(frame2, columns=("Descrição", "Valor", "Estado"), show="headings", height=17)
tree.column("Descrição", width=240, anchor="w")
tree.column("Valor", width=130, anchor="c")
tree.column("Estado", width=130, anchor="c")
tree.heading("Descrição", text="Descrição")
tree.heading("Valor", text="Valor")
tree.heading("Estado", text="Estado")
tree.place(x=17, y=15)

# texto para os Número de Despesas e Valor Total
lblDespesas = customtkinter.CTkLabel(app, text="Nº de Despesas:")
lblTotal = customtkinter.CTkLabel(app, text="Valor Total:")
lblDespesas.place(x=50, y=520)
lblTotal.place(x=250, y=520)

lblNumDespesas = customtkinter.CTkLabel(app, text="")
lblNumDespesas.place(x=150, y=520)

lblValorTotal = customtkinter.CTkLabel(app, text="")
lblValorTotal.place(x=350, y=520)


app.mainloop()
