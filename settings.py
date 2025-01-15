from customtkinter import *
from tkinter import messagebox
import os
from tkinter import font

app = CTk()
app.geometry("900x550")
app.title("Settings")
app.configure(fg_color="#2C2C2C")

def get_font(family, size=12, weight="normal"):
    available_fonts = font.families()
    if family in available_fonts:
        return font.Font(family=family, size=size, weight=weight)
    return font.Font(family="Inter", size=size, weight=weight)

def mudar_email():
    popup = CTkToplevel(app)
    popup.geometry("400x300")
    popup.title("Alterar E-mail")
    popup.configure(fg_color="#2C2C2C")

    def save_new_email():
        global user_data  # Para acessar a variável global user_data
        new_email = entry_new_email.get()

        if not new_email:
            messagebox.showerror("Erro", "Por favor, insira um novo e-mail!")
            return

        # Atualizar o email no logged_as.txt
        user_data[1] = new_email
        with open("logged_as.txt", "w", encoding="utf-8") as file:
            file.write("|".join(user_data))

        # Atualizar o email no utilizadores.txt
        try:
            with open("utilizadores.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                stored_data = line.strip().split("|")
                if stored_data[0] == user_data[0]:  # Se o nome de Utilizador for igual ao logado
                    stored_data[1] = new_email  # Atualiza o email
                updated_lines.append("|".join(stored_data))

            # Escrever as alterações de volta no arquivo
            with open("utilizadores.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(updated_lines))

        except FileNotFoundError:
            messagebox.showerror("Erro", "O arquivo utilizadores.txt não foi encontrado!")
            return

        # Atualizar o texto do label
        label_email.configure(text=f"Endereço de E-mail: {new_email}")
        messagebox.showinfo("Sucesso", "O e-mail foi atualizado com sucesso!")
        popup.destroy()


    # Rótulo e entrada para o novo email
    label_popup_title = CTkLabel(popup, text="Alterar E-mail", font=("Inter", 20), text_color="white")
    label_popup_title.pack(pady=20)

    label_new_email = CTkLabel(popup, text="Novo E-mail:", font=("Inter", 15), text_color="white")
    label_new_email.pack(pady=5)

    entry_new_email = CTkEntry(popup, font=("Inter", 15), width=300)
    entry_new_email.pack(pady=10)

    # Botão para guardar o novo email
    button_save_email = CTkButton(popup, text="Guardar", command=save_new_email, font=("Inter", 15), fg_color="#E6C614", text_color="black",hover_color="#776500")
    button_save_email.pack(pady=20)


def mudar_senha():
    popup = CTkToplevel(app)
    popup.geometry("400x350")
    popup.title("Alterar Senha")
    popup.configure(fg_color="#2C2C2C")

    def save_new_password():
        global user_data  # Torna user_data acessível dentro desta função
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()

        if not new_password or not confirm_password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Erro", "As senhas não correspondem!")
            return

        # Atualizar a senha no logged_as.txt
        user_data[5] = new_password
        with open("logged_as.txt", "w", encoding="utf-8") as file:
            file.write("|".join(user_data))

        # Atualizar a senha no utilizadores.txt
        try:
            with open("utilizadores.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                stored_data = line.strip().split("|")
                if stored_data[0] == user_data[0]:  # Verifica se é o Utilizador logado
                    stored_data[5] = new_password  # Atualiza a senha
                updated_lines.append("|".join(stored_data))

            # Escrever as alterações de volta no arquivo
            with open("utilizadores.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(updated_lines))

        except FileNotFoundError:
            messagebox.showerror("Erro", "O arquivo utilizadores.txt não foi encontrado!")

        messagebox.showinfo("Sucesso", "A senha foi atualizada com sucesso!")
        popup.destroy()


    # Rótulo e entrada para a nova senha
    label_popup_title = CTkLabel(popup, text="Alterar Senha", font=("Inter", 20), text_color="white")
    label_popup_title.pack(pady=20)

    label_new_password = CTkLabel(popup, text="Nova Senha:", font=("Inter", 15), text_color="white")
    label_new_password.pack(pady=5)

    entry_new_password = CTkEntry(popup, font=("Inter", 15), width=300, show="*")  # Campo de senha com caracteres ocultos
    entry_new_password.pack(pady=10)

    label_confirm_password = CTkLabel(popup, text="Confirmar Nova Senha:", font=("Inter", 15), text_color="white")
    label_confirm_password.pack(pady=5)

    entry_confirm_password = CTkEntry(popup, font=("Inter", 15), width=300, show="*")
    entry_confirm_password.pack(pady=10)

    # Botão para guardar a nova senha
    button_save_password = CTkButton(popup, text="Guardar", command=save_new_password, font=("Inter", 15), fg_color="#E6C614", text_color="black",hover_color="#776500")
    button_save_password.pack(pady=20)

try:
    with open("logged_as.txt", "r", encoding="utf-8") as file:
        dados = file.readlines()

    # Verificar se o nome de utilizador e senha correspondem
    for line in dados:
        user_data = line.strip().split("|")  # Dividir
        print(f"{user_data}")
except FileNotFoundError:
    messagebox.showerror("COMO???", "Não tem sessão iniciada!")
    app.destroy()

# Labels e Botões Principais
label_title = CTkLabel(app, text="Definições de utilizador", font=("Inter", 30), text_color="white")
label_title.pack(pady=20)

label_username = CTkLabel(app, text=f"Nome de Utilizador: {user_data[0]}", font=("Inter", 15), text_color="white")
label_username.pack(pady=5)

label_email = CTkLabel(app, text=f"Endereço de E-mail: {user_data[1]}", font=("Inter", 15), text_color="white")
label_email.pack(pady=5)

dia = user_data[2]
mes = user_data[3]
ano = user_data[4]
dataFormato = f"{str(dia).zfill(2)}/{str(mes).zfill(2)}/{ano}"

label_dataN = CTkLabel(app, text=f"Data de Nascimento: {dataFormato}", font=("Inter", 15), text_color="white")
label_dataN.pack(pady=5)

# Botão para abrir popup de alteração de email
button_change_email = CTkButton(app, text="Mudar E-mail", command=mudar_email, font=("Inter", 15), fg_color="#E6C614", text_color="black",hover_color="#776500")
button_change_email.pack(pady=20)

# Botão para abrir popup de alteração de senha
button_change_password = CTkButton(app, text="Mudar Senha", command=mudar_senha, font=("Inter", 15), fg_color="#E6C614", text_color="black",hover_color="#776500")
button_change_password.pack(pady=20)

app.mainloop()
