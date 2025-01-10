from customtkinter import *
from tkinter import messagebox
import subprocess

app = CTk()
app.geometry("1440x1032")
app.title("OLÁ GAMER")
app.configure(fg_color="black")

# Criar os labels
label_title = CTkLabel(app, text="OLÁ GAMER", font=("Inter", 30), text_color="white")
label_title.pack(pady=20)  # Adiciona o label à interface

label_username = CTkLabel(app, text="Nome de Utilizador:", font=("Arial", 15), text_color="white")
label_username.pack(pady=5)  # Adiciona o label à interface

entry_username = CTkEntry(app, width=300, placeholder_text="Digite o seu nome de utilizador", font=("Inter", 15))
entry_username.pack(pady=5)  # Adiciona o entry à interface

label_password = CTkLabel(app, text="Password:", font=("Inter", 15), text_color="white")
label_password.pack(pady=5)  # Adiciona o label à interface

entry_password = CTkEntry(app, width=300, placeholder_text="Digite a sua senha", font=("Inter", 15), show="*")
entry_password.pack(pady=5)  # Adiciona o entry à interface

# Criar o botão de login
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Verificar se o nome de utilizador e a senha estão corretos
    if username == "admin" and password == "12345":
        messagebox.showinfo("Login", "Login bem-sucedido!")
        app.destroy()  # Fecha a janela atual
        subprocess.Popen(["python", "projeto.py"])

    else:
        messagebox.showerror("Login", "Nome de usuário ou senha inválidos!")

button_login = CTkButton(app, text="Login", width=150, height=40, font=("Inter", 15), command=login, fg_color="#E6C614", text_color="black")
button_login.pack(pady=20)

# Função para abrir outro ficheiro Python e fechar a janela atual
def open_create_account():
    try:
        app.destroy()  # Fecha a janela atual
        subprocess.Popen(["python", "criar_conta.py"])  # Substitui "criar_conta.py" pelo nome do ficheiro
    except FileNotFoundError:
        messagebox.showerror("Erro", "O ficheiro 'criar_conta.py' não foi encontrado!")

# Criar um label clicável
label_create_account = CTkLabel(app, text="Não tem uma conta? Crie uma!", font=("Arial", 12), text_color="white")
label_create_account.pack(pady=10)

# Tornar a parte "Crie uma!" clicável
label_create_account.bind("<Button-1>", lambda e: open_create_account())  # Deteta o clique no label

app.mainloop()
