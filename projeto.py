import os
import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from tkinter import Menu  # Para criar a barra de menus
from PIL import Image, ImageTk  # Para trabalhar com imagens
import subprocess
from tkinter import font
from winotify import Notification


def get_font(family, size=12, weight="normal"):
    available_fonts = font.families()
    if family in available_fonts:
        return font.Font(family=family, size=size, weight=weight)
    return font.Font(family="Inter", size=size, weight=weight)


class jogostoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Games Store")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#2C2C2C")

        # Lista de desejos
        self.lista = []

        # Dados dos jogos, incluindo os caminhos das capas
        self.jogos_data = [
            {"name": "Grand Theft Auto V", "Género": "Ação", "Capa": "imagens/gta.png"},
            {"name": "The Crew", "Género": "Simulação", "Capa": "imagens/Crew.jpg"},
            {"name": "Grand Theft Auto VI", "Género": "Ação", "Capa": "imagens/gta6.jpg"},
            {"name": "Manor Lords", "Género": "Simulação", "Capa": "imagens/lords.jpg"},
            {"name": "EAFC 25", "Género": "Desporto", "Capa": "imagens/fc_25.png"},
            {"name": "Bus Simulator 21", "Género": "Simulação", "Capa": "imagens/bus.jpg"},
            {"name": "Minecraft", "Género": "Aventura", "Capa": "imagens/mine.jpeg"},
            {"name": "Rainbow Six Siege", "Género": "Ação", "Capa": "imagens/R6.jpg"}
        ]

        # Descrição
        self.dicas_descr = {
            "Grand Theft Auto V": "Explore a cidade de Los Santos e complete missões emocionantes.",
            "The Crew": "Junte-se a outros jogadores e participe de corridas num mundo aberto.",
            "Grand Theft Auto VI": "BREVEMENTE",
            "Manor Lords": "Construa e gerencie a sua própria cidade medieval.",
            "EAFC 25": "Participe de partidas emocionantes e conquiste o campeonato.",
            "Bus Simulator 21": "Conduza um autocarro numa cidade realista e cumpra horários.",
            "Minecraft": "Explore, construa e sobreviva num mundo de blocos.",
            "Rainbow Six Siege": "Participe de intensas batalhas táticas em equipe."
        }

        # Dicas para os jogos
        self.asdicas_dados = {
            "Grand Theft Auto V": ["1# Aumente seu Dinheiro Facilmente (Modo História)",
"Invista no Mercado de Ações:* - Complete as missões de assassinato do Lester estrategicamente:", "Participe de atividades online."],
            "The Crew": ["Junte-se a outros jogadores.", "Participe de corridas num mundo aberto.", "Personalize seu carro."],
            "Grand Theft Auto VI": ["Entre no modo online.", "Jogue com amigos.", "Complete missões em equipe."],
            "Manor Lords": ["Construa sua própria cidade.", "Gerencie recursos.", "Participe de batalhas."],
            "EAFC 25": ["Participe de partidas emocionantes.", "Conquiste o campeonato.", "Jogue com amigos."],
            "Bus Simulator 21": ["Conduza um autocarro numa cidade realista.", "Cumpra horários .", "Explore diferentes rotas."],
            "Minecraft": ["Explore o mundo de blocos.", "Construa estruturas incríveis.", "Sobreviva a criaturas."],
            "Rainbow Six Siege": ["Participe de batalhas táticas.", "Trabalhe em equipe.", "Use estratégias para vencer."]
        }

        inter_font = get_font("Inter", size=12)

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

        # Botão para abrir dicas
        Button(self.filter_frame, text="Dicas", font=("Inter", 12, "bold"), bg="#E6C614", fg="#FFFFFF",
               command=self.abrir_dicas).pack(fill=tk.X, pady=20)

        # Frame para exibição de jogos
        self.jogo_display_frame = Frame(self.root, bg="#2C2C2C")
        self.jogo_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.display_jogos(self.jogos_data)

    def barra_menu(self):
    # Criar barra de menus com cor personalizada
        self.menu_bar = Menu(self.root, bg="#E6C614", fg="#FFFFFF")  # Cor de fundo e texto

    # Menu Arquivo
        file_menu = Menu(self.menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF")  # Cor personalizada para o submenu
        file_menu.add_command(label="Sign up", command=self.open_create_account)
        file_menu.add_command(label="Home", command=self.home)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        self.menu_bar.add_cascade(label="Principal", menu=file_menu)

    # Menu Ajuda
        help_menu = Menu(self.menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF")
        help_menu.add_command(label="Utilizador", command=self.utilizador)
        help_menu.add_command(label="Sobre", command=self.sobre)
        self.menu_bar.add_cascade(label="Definições", menu=help_menu)

    # Adicionar a barra de menus na janela principal
        self.root.config(menu=self.menu_bar)

    def open_create_account(self):
        try:
            subprocess.Popen(["python", "login.py"])
        except FileNotFoundError:
            messagebox.showerror("Erro", "O ficheiro 'login.py' não foi encontrado!")

    def novo(self):
        messagebox.showinfo("Novo", "Opção 'Novo' selecionada!")

    def home(self):
        try:
            subprocess.Popen(["python", "Main.py"])
            root.destroy()
        except FileNotFoundError:
            print("Erro ao abrir o arquivo 'Main.py'")

    def sobre(self):
        messagebox.showinfo("Sobre", "Games Store App v1.0\nDesenvolvido por [Seu Nome]")

    def utilizador(self):
        try:
            subprocess.Popen(["python", "settings.py"])
            root.destroy()
        except FileNotFoundError:
            print("Erro ao abrir o arquivo 'settings.py'")

    def display_jogos(self, jogos):
        # Limpar o frame de exibição
        for widget in self.jogo_display_frame.winfo_children():
            widget.destroy()


        canvas = tk.Canvas(self.jogo_display_frame, bg="#2C2C2C")
        scroll_y = tk.Scrollbar(self.jogo_display_frame, orient="vertical", command=canvas.yview)
        scroll_frame = Frame(canvas, bg="#2C2C2C")

        scroll_frame.bind( "<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        if not jogos:
            Label(self.jogo_display_frame, text="Não há jogos disponíveis", font=("Inter", 14), bg="#FFFFFF", fg="#FFFFFF").pack(pady=20)
            return

        row_frame = None
        for index, jogo in enumerate(jogos):
            if index % 6 == 0:  # Novo row_frame a cada 6 jogos
                row_frame = Frame(scroll_frame, bg="#2C2C2C")
                row_frame.pack(fill=tk.X, pady=10,)
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

        Button(card_frame, text=jogo["name"], font=("Inter", 12, "bold",), bg="white", relief="raised",
                command=lambda: self.abrir_jogo(jogo["name"])).pack(pady=5)

        Label(card_frame, text=f"Género: {jogo['Género']}", font=("Helvetica", 10), bg="white").pack(pady=5)

        Button(card_frame, text="Adicionar à lista",bg="#E6C614", fg="#FFFFFF" , command=lambda g=jogo["name"]: self.adicionar_lista(g)).pack(pady=5)

    def ver_dicas(self, jogo_name):
        # Criar a janela de dicas
        dicas_window = tk.Toplevel(self.root)
        dicas_window.title(f"Dicas para {jogo_name}")
        dicas_window.geometry("1920x1080")
        dicas_window.configure(bg="#2C2C2C")

        # Frame esquerdo para as dicas
        left_frame = Frame(dicas_window, bg="#2C2C2C")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        Label(left_frame, text="DICAS", font=("Inter", 16, "bold"), bg="#2C2C2C", fg="#E6C614").pack(pady=10)

        # Exibir dicas específicas do jogo
        with open("dicas.txt", "r", encoding="utf-8") as file:
            dicas = file.read()
        # Separar o conteúdo por jogos
        jogos_dicas = dicas.split("!")
        for jogo_dicas in jogos_dicas:
            if jogo_name in jogo_dicas:
                dicas_texto = jogo_dicas.strip().replace(f"{jogo_name}\n", "")
                Label(left_frame, text=dicas_texto, font=("Inter", 12), bg="#2C2C2C", fg="#FFFFFF", justify="left", wraplength=1100).pack(anchor="w", pady=5)

        # Frame direito para exibição da imagem
        right_frame = Frame(dicas_window, bg="#2C2C2C")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Carregar e exibir a imagem do jogo
        try:
            jogo = next(j for j in self.jogos_data if j["name"] == jogo_name)
            img = Image.open(jogo["Capa"])
            img = img.resize((300, 500))  # Ajustar tamanho da imagem
            photo = ImageTk.PhotoImage(img)
            img_label = Label(right_frame, image=photo, bg="#2C2C2C")
            img_label.image = photo
            img_label.pack(pady=10)
        except StopIteration:
            Label(right_frame, text="Imagem não disponível", font=("Inter", 14), bg="#2C2C2C", fg="#E6C614").pack(pady=10)

        dicas_window.mainloop()

    def abrir_dicas(self):
        lista_window = tk.Toplevel(self.root)
        lista_window.title("Dicas")
        lista_window.geometry("1920x1080")
        lista_window.configure(bg="#2C2C2C")

        Label(lista_window, text="DICAS", font=("Inter", 16, "bold"),
              bg="#2C2C2C", fg="#E6C614").pack(pady=10)

        # Exibição das dicas para cada jogo
        for jogo in self.jogos_data:
            jogo_name = jogo["name"]
            dica = self.dicas_descr.get(jogo_name, "Sem dicas disponíveis.")
            self.criar_capa_dica(lista_window, jogo_name, dica)

    def criar_capa_dica(self, parent, jogo_name, dica):
        card_frame = Frame(parent, bg="#FFFFFF", relief="sunken", borderwidth=1, padx=10, pady=10)
        card_frame.pack(pady=5, fill=tk.X)

        Label(card_frame, text=jogo_name, font=("Inter", 15, "bold"), bg="white").pack(side=tk.LEFT, padx=5)
        Label(card_frame, text=dica, font=("Inter", 14), bg="white").pack(side=tk.LEFT, padx=5)
        Button(card_frame, text="Ver dicas", bg="#E6C614", fg="#FFFFFF", command=lambda: self.ver_dicas(jogo_name)).pack(side=tk.RIGHT, padx=5)

    def abrir_jogo(self, jogo_name): # Tenta abrir o arquivo do jogo com o mesmo nome
        print(f"A abrir: {jogo_name}") # print de debug
        if os.path.exists(f"jogos/{jogo_name}"):
            subprocess.Popen(["python", "jogo.py", jogo_name])  # Abre o ficheiro de python correspondente
        else: # dar erro se a pasta nao existe
            messagebox.showerror(
                "Erro",
                f"O jogo \"{jogo_name}\" não existe!"
            )


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
    def executar_funcoes(exibir_notificacao,adicionar_lista):
        exibir_notificacao()
        adicionar_lista()

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

    def filtrar_jogos(self, Género):
        if Género == "todos":
            Filtro_jogos = self.jogos_data
        else:
            Filtro_jogos = [jogo for jogo in self.jogos_data if jogo["Género"] == Género]

        self.display_jogos(Filtro_jogos)

if __name__ == "__main__":
    root = tk.Tk()
    app = jogostoreApp(root)
    root.mainloop()
