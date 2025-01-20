import os
import customtkinter
import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from tkinter import Menu  # Para criar a barra de menus
from tkinter import filedialog
from PIL import Image, ImageTk  # Para trabalhar com imagens
import subprocess
from tkinter import font
from winotify import Notification
import shutil

def get_font(family, size=12, weight="normal"):
    available_fonts = font.families()
    if family in available_fonts:
        return font.Font(family=family, size=size, weight=weight)
    return font.Font(family="Inter", size=size, weight=weight)

try:
    with open("logged_as.txt", "r", encoding="utf-8") as file:
        dados = file.readlines()

    # Verificar se o nome de utilizador e senha correspondem
    for line in dados:
        user_data = line.strip().split("|")  # Dividir
        print(f"{user_data}")
except FileNotFoundError:
    messagebox.showerror("COMO???", "Não tem sessão iniciada!")

class jogostoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Games Store")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#2C2C2C")

        # Lista de desejos
        self.lista = []
        self.carregar_lista_desejos()
        
        # Dados dos jogos, incluindo os caminhos das capas
        self.jogos_data = []
        caminho_base = "jogos"

        for pasta in os.listdir(caminho_base):
            pasta_caminho = os.path.join(caminho_base, pasta)

            # Verificar se é uma pasta
            if os.path.isdir(pasta_caminho):
                # Caminho do ficheiro "data.txt" dentro da pasta
                data_file = os.path.join(pasta_caminho, "data.txt")

                # Verificar a imagem de capa (png, jpg, jpeg)
                capa = None
                for ext in [".png", ".jpeg", ".jpg"]:
                    imagem_caminho = os.path.join(pasta_caminho, f"imagem{ext}")
                    if os.path.exists(imagem_caminho):
                        capa = imagem_caminho
                        break

                # Verificar se "data.txt" existe
                if os.path.exists(data_file):
                    try:
                        with open(data_file, "r", encoding="utf-8") as file:
                            linhas = file.readlines()

                            # Verificar se existem ao menos 3 linhas no ficheiro
                            if len(linhas) >= 2:
                                genero = linhas[1].strip()
                            if len(linhas) >= 3:
                                dicadescr = linhas[2].strip()
                                # Adicionar a entrada na lista
                                self.jogos_data.append({"name": pasta,"Género": genero,"Capa": capa, "Descrição Dica": dicadescr})
                    except Exception as e:
                        print(f"Erro ao processar '{data_file}': {e}")

        """self.jogos_data = [
            {"name": "Grand Theft Auto V", "Género": "Ação", "Capa": "jogos/Grand Theft Auto V/imagem.png"},
            {"name": "The Crew", "Género": "Simulação", "Capa": "jogos/The Crew/imagem.jpg"},
            {"name": "Grand Theft Auto VI", "Género": "Ação", "Capa": "jogos/Grand Theft Auto VI/imagem.jpg"},
            {"name": "Manor Lords", "Género": "Simulação", "Capa": "jogos/Manor Lords/imagem.jpg"},
            {"name": "EAFC 25", "Género": "Desporto", "Capa": "jogos/EAFC 25/imagem.png"},
            {"name": "Bus Simulator 21", "Género": "Simulação", "Capa": "jogos/Bus Simulator 21/imagem.jpg"},
            {"name": "Minecraft", "Género": "Aventura", "Capa": "jogos/Minecraft/imagem.jpeg"},
            {"name": "Rainbow Six Siege", "Género": "Ação", "Capa": "jogos/Rainbow Six Siege/imagem.jpg"}
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
            "Rainbow Six Siege": "Participe de intensas batalhas táticas em equipa."
        }"""

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
        Button(self.filter_frame, text="Lista de Desejos", font=("Inter", 12, "bold"), bg="#E6C614", fg="#FFFFFF",activebackground="#776500",
               command=self.abrir_lista).pack(fill=tk.X, pady=20)

        # Botão para abrir dicas
        Button(self.filter_frame, text="Dicas", font=("Inter", 12, "bold"), bg="#E6C614", fg="#FFFFFF",activebackground="#776500",
               command=self.abrir_dicas).pack(fill=tk.X, pady=20)

        # Botão para abrir ADMIN
        if user_data[6] == "admin":
            Button(self.filter_frame, text="ADMIN", font=("Inter", 12, "bold"), bg="#1814E6", fg="#FFFFFF",
                command=self.abrir_admin).pack(fill=tk.X, pady=20)

        # Frame para exibição de jogos
        self.jogo_display_frame = Frame(self.root, bg="#2C2C2C")
        self.jogo_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.display_jogos(self.jogos_data)

    def barra_menu(self):
    # Criar barra de menus com cor personalizada
        self.menu_bar = Menu(self.root, bg="#E6C614", fg="#FFFFFF")  # Cor de fundo e texto

    # Menu Principal
        file_menu = Menu(self.menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF",activebackground="#776500",)  # Cor personalizada para o submenu

        file_menu.add_command(label="Sign up", command=self.open_create_account)
        file_menu.add_command(label="Home", command=self.home)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        self.menu_bar.add_cascade(label="Principal", menu=file_menu)

    # Menu Definições
        help_menu = Menu(self.menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF",activebackground="#776500",)
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

        Button(card_frame, text="Lista de Desejos",bg="#E6C614",fg="#FFFFFF", activebackground="#776500",command=lambda g=jogo["name"]: self.adicionar_lista(g)).pack(pady=5)

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
            dica = jogo["Descrição Dica"]
            self.criar_capa_dica(lista_window, jogo_name, dica)

    def abrir_admin(self):
        lista_window = tk.Toplevel(self.root)
        lista_window.title("ADMIN")
        lista_window.geometry("800x700")
        lista_window.configure(bg="#2C2C2C")


        Label(lista_window, text="PAINEL DE ADMINISTRADOR", font=("Inter", 16, "bold"),
              bg="#1814E6", fg="#FFFFFF").pack(pady=10)

        # Exibir data e hora do último login
        try:
            with open("logged_as.txt", "r") as file:
                dados = file.readlines()

                for line in dados:
                    user_data = line.strip().split("|")
                Label(lista_window, text=f"ligado como: {user_data[0]} ({user_data[1]})", bg="#2C2C2C", fg="#FFFFFF").pack(pady=5)
        except FileNotFoundError:
            Label(lista_window, text="Nenhum login..?", bg="#2C2C2C", fg="#FFFFFF").pack(pady=5)

        # Campo para o nome de jogo
        Label(lista_window, text="Insira o nome do jogo que deseja adicionar:", bg="#2C2C2C", fg="#FFFFFF").pack(pady=10)
        self.entry_jogo_nome = tk.Entry(lista_window, width=30)
        self.entry_jogo_nome.pack(pady=5)

        # Campo para o género do jogo
        Label(lista_window, text="Insira o género do jogo que deseja adicionar:", bg="#2C2C2C", fg="#FFFFFF").pack(pady=10)
        self.entry_jogo_genero = tk.Entry(lista_window, width=30)
        self.entry_jogo_genero.pack(pady=5)

        # Campo para a capa do jogo
        # Campo para a capa do jogo
        Label(lista_window, text="Selecione a imagem para a capa do jogo que quer adicionar:", bg="#2C2C2C", fg="#FFFFFF").pack(pady=10)
        self.entry_jogo_capa = tk.Entry(lista_window, width=30)
        self.entry_jogo_capa.pack(pady=5)
        self.capaImagem = Button(lista_window, width=20, text="Imagem", command=self.escolherCapa)
        self.capaImagem.pack(pady=5)

        # Botão para adicionar jogo
        Button(lista_window, text="Adicionar Jogo", command=self.adicionar_jogo).pack(pady=10)

        Label(lista_window, text="Escreva o jogo que quer remover:", bg="#2C2C2C", fg="#FFFFFF").pack(pady=10)
        self.entry_jogo_remover = tk.Entry(lista_window, width=30)
        self.entry_jogo_remover.pack(pady=5)

        self.removerJogo = Button(lista_window, text="Remover Jogo", command=self.remover_jogo)
        self.removerJogo.pack(pady=10)

        # Campo para remover conta
        Label(lista_window, text=f"{"-" * 70}\nInsira um nome do utilizador:", bg="#2C2C2C", fg="#FFFFFF").pack(pady=5)
        self.entry_utilizador_rem = tk.Entry(lista_window, width=30)
        self.entry_utilizador_rem.pack(pady=5)

        # Botão para remover conta
        btn_frame = tk.Frame(lista_window,bg="#2C2C2C")
        btn_frame.pack(pady=10)
        Button(btn_frame, text="(Des)promover Conta", command=self.promover_conta, bg="#2CCC2C").pack(side="left", padx=5)
        Button(btn_frame, text="Remover Conta", command=self.remover_conta, bg="#CC2C2C").pack(side="left", padx=5)

        # Exibir número de contas
        self.exibir_numero_contas(lista_window)

    def remover_conta(self):
        username_to_remove = self.entry_utilizador_rem.get().strip()

        if not username_to_remove:
            messagebox.showerror("Erro", "Por favor, insira um nome de utilizador válido.")
            return

        # Verificar se a conta existe
        contas = []
        try:
            with open("utilizadores.txt", "r", encoding="utf-8") as file:
                contas = file.readlines()

            # Verificar se o utilizador está na lista
            user_found = False
            for conta in contas:
                user_data = conta.strip().split("|")
                if user_data[0].strip() == username_to_remove:
                    user_found = True
                    break

            if not user_found:
                messagebox.showerror("Erro", "Utilizador não encontrado.")
                return

        except FileNotFoundError:
            messagebox.showerror("Erro", "O ficheiro 'utilizadores.txt' não foi encontrado!")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aceder ao ficheiro: {e}")
            return

        # Perguntar confirmação
        confirmar = messagebox.askyesno(
            "Confirmação",
            f"Tem a certeza de que deseja remover a conta '{username_to_remove}'?"
        )
        if not confirmar:
            return
        else:
    # Remover a conta
            try:
                with open("utilizadores.txt", "w", encoding="utf-8") as file:
                    for conta in contas:
                        user_data = conta.strip().split("|")
                        if user_data[0].strip() != username_to_remove:
                            file.write(conta)  # Escrever de volta apenas as contas que não são a removida

                messagebox.showinfo("Sucesso", f"Conta '{username_to_remove}' removida com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover a conta: {e}")

    def promover_conta(self):
        username_to_alter = self.entry_utilizador_rem.get().strip()

        if not username_to_alter:
            messagebox.showerror("Erro", "Por favor, insira um nome de utilizador válido.")
            return

        # Verificar se a conta existe
        contas = []
        try:
            with open("utilizadores.txt", "r", encoding="utf-8") as file:
                contas = file.readlines()

            # Verificar se o utilizador está na lista
            user_found = False
            novas_contas = []
            for conta in contas:
                user_data = conta.strip().split("|")
                if user_data[0].strip() == username_to_alter:
                    user_found = True
                    # Alterar "utilizador" para "admin" e vice-versa
                    if user_data[6].strip() == "utilizador":
                        user_data[6] = "admin"
                    elif user_data[6].strip() == "admin":
                        user_data[6] = "utilizador"

                    # Recriar a linha alterada
                    novas_contas.append("|".join(user_data) + "\n")
                else:
                    novas_contas.append(conta)  # Manter as outras linhas inalteradas

            if not user_found:
                messagebox.showerror("Erro", "Utilizador não encontrado.")
                return

        except FileNotFoundError:
            messagebox.showerror("Erro", "O ficheiro 'utilizadores.txt' não foi encontrado!")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aceder ao ficheiro: {e}")
            return

        # Perguntar confirmação
        confirmar = messagebox.askyesno(
            "Confirmação",
            f"Tem a certeza de que deseja alterar o papel da conta '{username_to_alter}' para {user_data[6]}?"
        )
        if not confirmar:
            return

        # Escrever as alterações de volta ao ficheiro
        try:
            with open("utilizadores.txt", "w", encoding="utf-8") as file:
                file.writelines(novas_contas)

            messagebox.showinfo(
                "Sucesso",
                f"O papel da conta '{username_to_alter}' foi alterado com sucesso!"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar as alterações: {e}")

    def escolherCapa(self):
        caminho_imagem = filedialog.askopenfilename(title="Selecione uma imagem",
                                                filetypes=(("png files", "*.png"), ("all files", "*.*")))
        if caminho_imagem:
            # Copiar a imagem para a pasta "imagens"
            nome_imagem = os.path.basename(caminho_imagem)
            destino = os.path.join("imagens", nome_imagem)
            shutil.copy(caminho_imagem, destino)
            self.entry_jogo_capa.delete(0, tk.END)  # Limpar o campo de entrada
            self.entry_jogo_capa.insert(0, destino)  # Inserir o caminho da imagem

    def adicionar_jogo(self):
        # Coletar dados do jogo
        jogo_nome_a = self.entry_jogo_nome.get().strip()  # Nome do jogo
        jogo_genero = self.entry_jogo_genero.get().strip()  # Gênero do jogo
        jogo_capa = self.entry_jogo_capa.get().strip()  # Caminho da imagem da capa

        # Validações
        if not jogo_nome_a or not jogo_genero or not jogo_capa:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos para adicionar um novo jogo")
            return

        # Verificar se o jogo já existe na lista
        for jogo in self.jogos_data:
            if jogo["name"].lower() == jogo_nome_a.lower():  # Comparação sem diferenciar maiúsculas e minúsculas
                messagebox.showerror("Erro", "Jogo já existe!")
                return

        # Adicionar o novo jogo à lista interna
        self.jogos_data.append({"name": jogo_nome_a, "Género": jogo_genero, "Capa": jogo_capa})

        # Atualizar a exibição de jogos
        self.display_jogos(self.jogos_data)

        messagebox.showinfo("Sucesso", f"Jogo '{jogo_nome_a}' adicionado com sucesso!")

    def remover_jogo(self):
        jogo_remover = self.entry_jogo_remover.get().strip()  # Obter o nome do jogo a ser removido
        # Verificar se o jogo existe na lista
        for jogo in self.jogos_data:
            if jogo["name"].lower() == jogo_remover.lower():  # Comparação sem diferenciar maiúsculas e minúsculas
                self.jogos_data.remove(jogo)  # Remove o jogo da lista
                messagebox.showinfo("Sucesso", f"Jogo '{jogo_remover}' removido com sucesso!")
                self.display_jogos(self.jogos_data)  # Atualiza a exibição de jogos
                return

        # Se o jogo não for encontrado
        messagebox.showerror("Erro", f"Jogo '{jogo_remover}' não encontrado na lista.")

    def exibir_numero_contas(self, parent):
        try:
            with open("utilizadores.txt", "r", encoding="utf-8") as file:
                contas = file.readlines()
                numero_contas = len(contas)
                Label(parent, text=f"Número de Contas: {numero_contas}\nReabra o painel para atualizar papeis.", bg="#2C2C2C", fg="#FFFFFF").pack(pady=5)
                for conta in contas:
                    dados = conta.strip().split("|")
                    Label(parent, text=f"Utilizador: {dados[0]}, Email: {dados[1]}, Papel: {dados[6]}", bg="#2C2C2C", fg="#FFFFFF").pack(pady=2)
        except FileNotFoundError:
            Label(parent, text="Arquivo de contas não encontrado.", bg="#2C2C2C", fg="#FFFFFF").pack(pady=5)

    def criar_capa_dica(self, parent, jogo_name, dica):
        card_frame = Frame(parent, bg="#FFFFFF", relief="sunken", borderwidth=1, padx=10, pady=10)
        card_frame.pack(pady=5, fill=tk.X)

        Label(card_frame, text=jogo_name, font=("Inter", 15, "bold"), bg="white").pack(side=tk.LEFT, padx=5)
        Label(card_frame, text=dica, font=("Inter", 14), bg="white").pack(side=tk.LEFT, padx=5)
        Button(card_frame, text="Ver dicas", bg="#E6C614", fg="#FFFFFF", activebackground="#776500", command=lambda: self.ver_dicas(jogo_name)).pack(side=tk.RIGHT, padx=5)

    def abrir_jogo(self, jogo_name): # Tenta abrir o arquivo do jogo com o mesmo nome
        print(f"A abrir: {jogo_name}") # print de debug
        if os.path.exists(f"jogos/{jogo_name}"):
            subprocess.Popen(["python", "jogo.py", jogo_name])  # Abre o ficheiro de python correspondente
        else: # dar erro se a pasta nao existe
            messagebox.showerror(
                "Erro",
                f"O jogo \"{jogo_name}\" não existe!"
            )


    def exibir_notificacao(self):
        notification = Notification(
            app_id="Games Store",
            title="Jogo Adicionado",
            msg="Você adicionou um jogo à sua lista de desejos!"
        )
        notification.show()

    def adicionar_lista(self, jogo):
        if not jogo.strip():
            messagebox.showerror("Erro", "O nome do jogo não pode estar vazio!")
            return
        if jogo not in self.lista:
            self.lista.append(jogo)
            self.exibir_notificacao()
            self.salvar_lista_desejos()  # Salvar após adicionar
        else:
            messagebox.showinfo("Lista de desejos", f"{jogo} já está na lista!")




    def abrir_lista(self):
        lista_window = tk.Toplevel(self.root)
        lista_window.title("Lista de Desejos")
        lista_window.geometry("600x400")
        lista_window.configure(bg="#2C2C2C")

        Label(lista_window, text="A Sua Lista de Desejos", font=("Inter", 16, "bold"),
             bg="#2C2C2C", fg="#E6C614").pack(pady=10)

        if not self.lista:
            Label(lista_window, text="A lista está vazia.", bg="#2C2C2C", fg="#FFFFFF",
              font=("Inter", 12)).pack(pady=20)
        else:
            for jogo in self.lista:
                self.criar_capa(lista_window, jogo)

        Button(lista_window, text="Remover Todos", bg="#FF0000", fg="#FFFFFF",
           command=lambda: self.limpar_lista(lista_window)).pack(pady=10)

    def criar_capa(self, parent, jogo_name):
        card_frame = Frame(parent, bg="#FFFFFF", relief="sunken", borderwidth=1, padx=10, pady=10)
        card_frame.pack(pady=5, fill=tk.X)

        Label(card_frame, text=jogo_name, font=("Inter", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=5)

        remove_button = Button(card_frame, text="Remover",
                               command=lambda: self.remover_da_lista(jogo_name, card_frame))
        remove_button.pack(side=tk.RIGHT, padx=5)

    def salvar_lista_desejos(self):
        try:
            with open("lista_desejos.txt", "w", encoding="utf-8") as file:
                for jogo in self.lista:
                    file.write(f"{jogo}\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a lista: {e}")

    def carregar_lista_desejos(self):
        try:
            with open("lista_desejos.txt", "r", encoding="utf-8") as file:
                self.lista = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.lista = []
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a lista: {e}")
            self.lista = []


    def remover_da_lista(self, jogo, frame):
        if jogo in self.lista:
            self.lista.remove(jogo)
            self.salvar_lista_desejos()
            frame.destroy()
            messagebox.showinfo("Lista", f"{jogo} foi removido da sua lista.")

    def limpar_lista(self, lista_window):
        self.lista.clear()
        self.salvar_lista_desejos()
        for widget in lista_window.winfo_children():
            widget.destroy()
        Label(lista_window, text="A Sua Lista de Desejos está vazia.", bg="#2C2C2C", fg="#FFFFFF",
              font=("Inter", 12)).pack(pady=20)

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