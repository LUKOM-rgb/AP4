from customtkinter import *
from tkinter import messagebox
import subprocess

set_appearance_mode("dark")  # Modos: "System" (padrão), "Dark", "Light"
set_default_color_theme("blue")  # Temas: "blue" (padrão), "green", "dark-blue"

app = CTk()
app.geometry("900x550")
app.title("OLÁ GAMER")

# Labels e Entradas de texto
label_title = CTkLabel(app, text="OLÁ GAMER", font=("Arial", 30), text_color="white")
label_title.pack(pady=20)

label_username = CTkLabel(app, text="Nome de Utilizador:", font=("Arial", 15), text_color="white")
label_username.pack(pady=5)

entry_username = CTkEntry(app, width=300, placeholder_text="Digite o seu nome de utilizador", font=("Arial", 15))
entry_username.pack(pady=5)

label_email = CTkLabel(app, text="Endereço de E-mail:", font=("Arial", 15), text_color="white")
label_email.pack(pady=5)

entry_email = CTkEntry(app, width=300, placeholder_text="Digite o seu e-mail", font=("Arial", 15))
entry_email.pack(pady=5)

label_dataN = CTkLabel(app, text="Data de Nascimento:", font=("Arial", 15), text_color="white")
label_dataN.pack(pady=5)

entry_dataN = CTkEntry(app, width=300, placeholder_text="dd/mm/aaaa", font=("Arial", 15))
entry_dataN.pack(pady=5)

label_password = CTkLabel(app, text="Password:", font=("Arial", 15), text_color="white")
label_password.pack(pady=5)

entry_password = CTkEntry(app, width=300, placeholder_text="Digite a sua senha", font=("Arial", 15), show="*")
entry_password.pack(pady=5)

label_RepetirPassword = CTkLabel(app, text="Repita Password:", font=("Arial", 15), text_color="white")
label_RepetirPassword.pack(pady=5)

entry_RepetirPassword = CTkEntry(app, width=300, placeholder_text="Digite outra vez a sua senha", font=("Arial", 15), show="*")
entry_RepetirPassword.pack(pady=5)

# Função para criar a conta
def criar_conta():
    username = entry_username.get()
    email = entry_email.get()
    data_nascimento = entry_dataN.get()
    password = entry_password.get()
    repetir_password = entry_RepetirPassword.get()

    # Verificar se todos os campos foram preenchidos
    if not username or not email or not data_nascimento or not password or not repetir_password:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Verificar se as passwords coincidem
    if password != repetir_password:
        messagebox.showerror("Erro", "As passwords não coincidem.")
        return

    # Simular sucesso na criação de conta
    messagebox.showinfo("Sucesso", f"Conta criada para {username} com sucesso!")
    app.destroy()

# Botão para criar conta
button_criarConta = CTkButton(app, text="Criar Conta", width=150, height=40, font=("Arial", 15), command=criar_conta)
button_criarConta.pack(pady=20)

# Label para redirecionar para o login
label_login_account = CTkLabel(app, text="Já tem conta? Faça Login!", font=("Arial", 12), text_color="lightblue")
label_login_account.pack(pady=10)

# Tornar o label clicável
label_login_account.bind("<Button-1>", lambda e: open_login())

# Função para abrir a janela de login e fechar a atual
def open_login():
    try:
        app.destroy()  # Fecha a janela atual
        subprocess.Popen(["python", "login.py"])  # Substitui "login.py" pelo nome correto do ficheiro
    except FileNotFoundError:
        messagebox.showerror("Erro", "O ficheiro 'login.py' não foi encontrado!")

# Label para redirecionar para o login
label_login_account = CTkLabel(app, text="Já tem conta? Faça Login!", font=("Arial", 12), text_color="lightblue")
label_login_account.pack(pady=10)

# Tornar o label clicável
label_login_account.bind("<Button-1>", lambda e: open_login())

app.mainloop()

