import tkinter as tk
from winotify import Notification
import os
import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from tkinter import Menu  # Para criar a barra de menus
from PIL import Image, ImageTk  # Para trabalhar com imagens
import subprocess
from tkinter import font

# Função para exibir a notificação
def exibir_notificacao():
    notification = Notification(app_id="Código Python", title="Notificação", msg="Você clicou no botão!")
    notification.show()

# Outra função que será chamada
def adicionar_lista(self, jogo):
        if jogo not in self.lista:
            self.lista.append(jogo)
            messagebox.showinfo("Lista de desejos", f"{jogo} foi adicionado à sua lista de desejos!")
        else:
            messagebox.showinfo("Lista de desejos", f"{jogo} já está na sua lista de desejos!")

# Função que chama as duas
def executar_funcoes():
    exibir_notificacao()
    outra_funcao()

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Notificação com Botão")
janela.geometry("300x200")

# Botão que chama a função combinada
botao = tk.Button(janela, text="Executar Funções", command=executar_funcoes)
botao.pack(pady=20)

# Executa a interface gráfica
janela.mainloop()
