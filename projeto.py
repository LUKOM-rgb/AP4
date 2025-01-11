import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from tkinter import Menu  # Para criar a barra de menus
from PIL import Image, ImageTk  # Para trabalhar com imagens
import subprocess
from tkinter import font

def get_font(family, size=12, weight="normal"):
    available_fonts = font.families()
    if family in available_fonts:
        return font.Font(family=family, size=size, weight=weight)
    return font.Font(family="Arial", size=size, weight=weight)


class jogostoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Games Store")
        self.root.geometry("1440x2000")
        self.root.configure(bg="#2C2C2C")

        # Lista de desejos
        self.lista = []

        # Dados dos jogos, incluindo os caminhos das capas
        self.jogos_data = [
            {"name": "Grand Theft Auto V", "Genero": "Ação", "Capa": "imagens/gta.png"},
            {"name": "The Crew", "Genero": "Simulação", "Capa": "imagens/Crew.jpg"},
            {"name": "Grand Theft Auto Online", "Genero": "Ação", "Capa": "imagens/gta6.jpg"},
            {"name": "Manor Lords", "Genero": "Simulação", "Capa": "imagens/lords.jpg"},
            {"name": "EAFC 25", "Genero": "Desporto", "Capa": "imagens/fc_25.png"},
            {"name": "Bus Simulator 21", "Genero": "Simulação", "Capa": "imagens/bus.jpg"},
            {"name": "Minecraft", "Genero": "Aventura", "Capa": "imagens/mine.jpeg"},
            {"name": "Rainbow Six Siege", "Genero": "Ação", "Capa": "imagens/R6.jpg"}
        ]
        inter_font = get_font("Inter", size=12)

        
        # Criar barra de menus
        self.barra_menu()

        # Frame para filtros
        self.filter_frame = Frame(self.root, bg="#2C2C2C", width=150)
        self.filter_frame.pack(side=tk.RIGHT, fill=tk.Y)

        Label(self.filter_frame, text="Filtros", bg="#2C2C2C", font=("Inter", 14, "bold"), fg="#E6C614").pack(pady=10)

        # Adicionar filtros como labels interativos
        filtros = ["Ação", "Aventura", "Simulação", "Desporto", "todos"]
        for filtro in filtros:
            filtro_label = Label(self.filter_frame, text=filtro.capitalize(), font=("Inter", 12), bg="#2C2C2C", fg="#FFFFFF", cursor="hand2")
            filtro_label.pack(fill=tk.X, pady=5)
            filtro_label.bind("<Button-1>", lambda event, g=filtro: self.filtrar_jogos(g))

        # Botão para abrir lista de desejos
        Button(self.filter_frame, text="Lista de Desejos", font=("Inter", 12, "bold"), bg="#E6C614", fg="#FFFFFF",
               command=self.abrir_lista).pack(fill=tk.X, pady=20)

        # Frame para exibição de jogos
        self.jogo_display_frame = Frame(self.root, bg="#2C2C2C")
        self.jogo_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.display_jogos(self.jogos_data)

    def barra_menu(self):
        # Criar barra de menus
        self.menu_bar = Menu(self.root)

        # Menu Arquivo
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Sign up", command=self.open_create_account)
        file_menu.add_command(label="Abrir", command=self.abrir)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        self.menu_bar.add_cascade(label="Arquivo", menu=file_menu)

        # Menu Ajuda
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self.sobre)
        self.menu_bar.add_cascade(label="Ajuda", menu=help_menu)

        # Adicionar a barra de menus na janela principal
        self.root.config(menu=self.menu_bar)

    def open_create_account(self):
        try:
            subprocess.Popen(["python", "login.py"])
        except FileNotFoundError:
            messagebox.showerror("Erro", "O ficheiro 'login.py' não foi encontrado!")

    def novo(self):
        messagebox.showinfo("Novo", "Opção 'Novo' selecionada!")

    def abrir(self):
        messagebox.showinfo("Abrir", "Opção 'Abrir' selecionada!")

    def sobre(self):
        messagebox.showinfo("Sobre", "Games Store App v1.0\nDesenvolvido por [Seu Nome]")

    def display_jogos(self, jogos):
        # Limpar o frame de exibição
        for widget in self.jogo_display_frame.winfo_children():
            widget.destroy()

        
        canvas = tk.Canvas(self.jogo_display_frame, bg="#2C2C2C")
        scroll_y = tk.Scrollbar(self.jogo_display_frame, orient="vertical", command=canvas.yview)
        scroll_frame = Frame(canvas, bg="#2C2C2C")

        scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
         )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        if not jogos:
            Label(self.jogo_display_frame, text="Não há jogos disponíveis", font=("Inter", 14), bg="#FFFFFF", fg="#FFFFFF").pack(pady=20)
            return

        row_frame = None
        for index, jogo in enumerate(jogos):
            if index % 4 == 0:  # Novo row_frame a cada 4 jogos
                row_frame = Frame(scroll_frame, bg="#2C2C2C")
                row_frame.pack(fill=tk.X, pady=10)
            self.Capa_jogos(row_frame, jogo)

    def Capa_jogos(self, parent, jogo):
        card_frame = Frame(parent, bg="#FFFFFF", relief="sunken", borderwidth=1, padx=10, pady=10)
        card_frame.pack(side=tk.LEFT, padx=10)

        # Carregar imagem da capa
        try:
            img = Image.open(jogo["Capa"])
            img = img.resize((230, 341))  # Redimensiona a capa
            photo = ImageTk.PhotoImage(img)
            img_label = Label(card_frame, image=photo, bg="white")
            img_label.image = photo  # Mantém uma referência para a imagem
            img_label.pack(pady=5)
        except Exception:
            Label(card_frame, text="Capa não disponível", bg="white", font=("Inter", 10)).pack(pady=5)

        Label(card_frame, text=jogo["name"], font=("Inter", 12, "bold",), bg="white").pack(pady=5)


        Button(card_frame, text="Adicionar à lista",bg="#E6C614", fg="#FFFFFF" , command=lambda g=jogo["name"]: self.adicionar_lista(g)).pack(pady=5)

    def adicionar_lista(self, jogo):
        if jogo not in self.lista:
            self.lista.append(jogo)
            messagebox.showinfo("Lista de desejos", f"{jogo} foi adicionado à sua lista de desejos!")
        else:
            messagebox.showinfo("Lista de desejos", f"{jogo} já está na sua lista de desejos!")

    def abrir_lista(self):
        lista_window = tk.Toplevel(self.root)
        lista_window.title("Lista de Desejos")
        lista_window.geometry("600x400")
        lista_window.configure(bg="#2C2C2C")

        Label(lista_window, text="Sua Lista de Desejos", font=("Inter", 16, "bold"), 
          bg="#2C2C2C", fg="#E6C614").pack(pady=10)

    # Exibição dos itens da lista de desejos
        for jogo in self.lista:
         self.criar_capa(lista_window, jogo)

    # Botão "Remover Todos"
        Button(lista_window, text="Remover Todos", bg="#FF0000", fg="#FFFFFF", 
           command=lambda: self.Limpar_lista(lista_window)).pack(pady=10)
    
    def criar_capa(self, parent, jogo_name):
        card_frame = Frame(parent, bg="#FFFFFF", relief="sunken", borderwidth=1, padx=10, pady=10)
        card_frame.pack(pady=5, fill=tk.X)

        Label(card_frame, text=jogo_name, font=("Inter", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=5)

        remove_button = Button(card_frame, text="Remover", 
                           command=lambda g=jogo_name: self.remover_da_lista(g, card_frame))
        remove_button.pack(side=tk.RIGHT, padx=5)


        Label(card_frame, text=jogo_name, font=("Inter", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=5)

        remove_button = Button(card_frame, text="Remover", command=lambda g=jogo_name: self.remover_da_lista(g, card_frame))
        remove_button.pack(side=tk.RIGHT, padx=5)

    def remover_da_lista(self, jogo, frame):
        if jogo in self.lista:
            self.lista.remove(jogo)
            frame.destroy()
            messagebox.showinfo("Lista", f"{jogo} foi removido da sua lista.")

    def Limpar_lista(self, lista_window):
        self.lista.clear()
        for widget in lista_window.winfo_children():
            widget.destroy()
        Label(lista_window, text="Sua Lista de Desejos está vazia.", bg="#2C2C2C", fg="#FFFFFF", font=("Inter", 12)).pack(pady=20)

    def filtrar_jogos(self, Genero):
        if Genero == "todos":
            Filtro_jogos = self.jogos_data
        else:
            Filtro_jogos = [jogo for jogo in self.jogos_data if jogo["Genero"] == Genero]

        self.display_jogos(Filtro_jogos)

if __name__ == "__main__":
    root = tk.Tk()
    app = jogostoreApp(root)
    root.mainloop()
