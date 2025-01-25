from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow
import tkinter as tk
import subprocess
from tkinter import font
from datetime import datetime


app = CTk()
app.geometry("900x550")
app.title("OLÁ GAMER")
app.configure(fg_color="#2C2C2C")
app.iconphoto(False,tk.PhotoImage(file="favicon.png"))

def get_font(family, size=12, weight="normal"):
    available_fonts = font.families()
    if family in available_fonts:
        return font.Font(family=family, size=size, weight=weight)
    return font.Font(family="Inter", size=size, weight=weight)

# função para criar a conta
def criar_conta():
    username = entry_username.get().strip()
    email = entry_email.get().strip()

    # ter a certeza que a data é um número
    if not entry_diaN.get().strip().isdigit():
        messagebox.showerror("Erro", "O dia deve ser um número.")
        return
    if not entry_mesN.get().strip().isdigit():
        messagebox.showerror("Erro", "O mês deve ser um número.")
        return
    if not entry_anoN.get().strip().isdigit():
        messagebox.showerror("Erro", "O ano deve ser um número.")
        return

    dia = int(entry_diaN.get().strip())
    mes = int(entry_mesN.get().strip())
    ano = int(entry_anoN.get().strip())
    password = entry_password.get()
    repetir_password = entry_RepetirPassword.get()

    # verificar se todos os campos foram preenchidos
    if not username or not email or not dia or not mes or not ano or not password or not repetir_password:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    ### VALIDAÇÕES ###
    if "\\" in username or "|" in username:
        messagebox.showerror("Erro", "O nome de utilizador não pode conter '\\' ou '|'.")
        return

    if "\\" in email or "|" in email:
        messagebox.showerror("Erro", "O e-mail não pode conter '\\' ou '|'.")
        return

    if "\\" in password or "|" in password:
        messagebox.showerror("Erro", "A senha não pode conter '\\' ou '|'.")
        return

    ### DATA VÁLIDA? ###

    # cada 4 anos é bissexto
    # se o ano for divisível por 100 mas não por 400, não é bissexto
    bissexto = (ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0))

    if dia < 1: # Verificar se o dia é válido
        messagebox.showerror("Erro", "Dia menor que 1.")
        return
    if mes in {4, 6, 9, 11} and dia > 30: # Verificar se o dia 31 faz sentido
        messagebox.showerror("Erro", "O mês selecionado não tem 31 dias.")
        return
    elif dia > 31: # Verificar se o dia está 31 ou menor
        messagebox.showerror("Erro", "Dia superior a 31.")
        return

    if mes >= 13 or mes <= 0:  # Verificar se o mês é válido
        messagebox.showerror("Erro", f"o mês {mes} não é válido.\nPor favor insira apenas de 1 a 12")
        return

    if mes == 2 and ((bissexto and dia > 29) or (not bissexto and dia > 28)): # dia maior que o fevereiro deixa? erro
        messagebox.showerror("Erro", "este fevereiro não tem tantos dias.")
        return

    if ano >= datetime.now().year or ano <= datetime.now().year-120:  # verificar se o ano faz sentido (ninguém pode entrar se estiver impossivelmente novo ou velho)
        messagebox.showerror("Erro", f"{ano} não é um ano válido")
        return

    # verificar se as passwords coincidem

    #print(password)
    #print(repetir_password)
    if password != repetir_password:
        messagebox.showerror("Erro", "As passwords não coincidem.")
        return

    ### email VÁLIDO? ###

    arroba_pos = email.find("@")
    ponto_pos = email.find(".", arroba_pos)  # o ponto deve vir após o "@"
    #print(ponto_pos)

    # se não houver nada antes do arroba, erro
    # se não houver ponto ou arroba, erro
    # se houver pontos atrás do arroba, erro
    # se não houver nada entre o arroba e o ponto, erro
    # se o email acabar com ponto, erro
    # se tiver mais que um arroba, erro
    if arroba_pos == 0 or arroba_pos == -1 or ponto_pos == -1 or ponto_pos < arroba_pos or ponto_pos == (arroba_pos + 1) or email.endswith(".") or email.count("@") != 1:
        messagebox.showerror("Erro", "Email inválido.")
        return

    # Guardar os dados num ficheiro txt
    try:
        with open("utilizadores.txt", "r", encoding="utf-8") as file:
            dados = file.readlines()
            # Verificar se o nome de utilizador e senha correspondem
            for line in dados:
                user_data = line.strip().split("|") #dividir

                userCheck = user_data[0].strip()
                emailCheck = user_data[1].strip()

                if username == userCheck:
                    messagebox.showerror("Erro", "Utilizador com esse nome já existe!")
                    return
                if email == emailCheck:
                    messagebox.showerror("Erro", "Utilizador com esse e-mail já existe!")
                    return

        with open("utilizadores.txt", "a", encoding="utf-8") as file:
            file.write(f"{username}|{email}|{dia}|{mes}|{ano}|{password}|utilizador\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao guardar os dados: {e}")
        return

    # Simular sucesso na criação de conta
    messagebox.showinfo("Sucesso", f"Conta criada para {username} com sucesso!")
    subprocess.Popen(["python", "login.py"])
    app.destroy()

# Função para abrir a janela de login e fechar a atual
def open_login():
    try:
        app.destroy()  # Fecha a janela atual
        subprocess.Popen(["python", "login.py"])  # Substitui "login.py" pelo nome correto do ficheiro
    except FileNotFoundError:
        messagebox.showerror("Erro", "O ficheiro 'login.py' não foi encontrado!")

# Labels e Entradas de texto
label_title = CTkLabel(app, text="OLÁ GAMER", font=("Arial", 30), text_color="white")
label_title.pack(pady=20)

label_username = CTkLabel(app, text="Nome de Utilizador:", font=("Inter", 15), text_color="white")
label_username.pack(pady=5)

entry_username = CTkEntry(app, width=300, placeholder_text="Introduza o seu nome de utilizador", font=("Inter", 15))
entry_username.pack(pady=5)

label_email = CTkLabel(app, text="Endereço de E-mail:", font=("Inter", 15), text_color="white")
label_email.pack(pady=5)

entry_email = CTkEntry(app, width=300, placeholder_text="Introduza o seu e-mail", font=("Inter", 15))
entry_email.pack(pady=5)

label_dataN = CTkLabel(app, text="Data de Nascimento:", font=("Inter", 15), text_color="white")
label_dataN.pack(pady=5)

# Frame para organizar os campos de data horizontalmente
frame_dataN = CTkFrame(app, fg_color="transparent")
frame_dataN.pack(pady=5)

entry_diaN = CTkEntry(frame_dataN, width=80, placeholder_text="DIA", font=("Inter", 15))
entry_diaN.grid(row=0, column=0, padx=5)

entry_mesN = CTkEntry(frame_dataN, width=80, placeholder_text="MÊS", font=("Inter", 15))
entry_mesN.grid(row=0, column=2, padx=5)

entry_anoN = CTkEntry(frame_dataN, width=100, placeholder_text="ANO", font=("Inter", 15))
entry_anoN.grid(row=0, column=4, padx=5)

label_password = CTkLabel(app, text="Password:", font=("Inter", 15), text_color="white")
label_password.pack(pady=5)

entry_password = CTkEntry(app, width=300, placeholder_text="Introduza a sua senha", font=("Inter", 15), show="*")
entry_password.pack(pady=5)

label_RepetirPassword = CTkLabel(app, text="Repita Password:", font=("Inter", 15), text_color="white")
label_RepetirPassword.pack(pady=5)

entry_RepetirPassword = CTkEntry(app, width=300, placeholder_text="Introduza outra vez a sua senha", font=("Inter", 15), show="*")
entry_RepetirPassword.pack(pady=5)

# Botão para criar conta
button_criarConta = CTkButton(app, text="Criar Conta", width=150, height=40, font=("Inter", 15), command=criar_conta, fg_color="#E6C614", text_color="black", hover_color="#776500")
button_criarConta.pack(pady=10)

# Label para redirecionar para o login
label_login_account = CTkLabel(app, text="Já tem conta? FAÇA LOGIN!", font=("Inter", 12, "bold"), text_color="white")
label_login_account.pack(pady=5)

# Tornar o label clicável
label_login_account.bind("<Button-1>", lambda e: open_login())

app.mainloop()
