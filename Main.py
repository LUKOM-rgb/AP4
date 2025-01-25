import tkinter as tk
from tkinter import Button, Label, Menu, Canvas, Scrollbar, Frame, messagebox
from PIL import Image, ImageTk  # Import Pillow
import os
import subprocess
from notifypy import Notify
import sys

def main():
    categoria = sys.argv[1] if len(sys.argv) > 1 else None
    # Lógica para exibir a categoria específica
    if categoria:
        print(f"Exibindo jogos da categoria: {categoria}")
        # Adicione aqui a lógica para mostrar os jogos dessa categoria


def mostrar_notificacao(categoria):
    notification = Notify()
    notification.title = "Mais Jogos Disponíveis!"
    notification.message = f"Existem mais jogos na categoria: {categoria}. Clique para ver."
    notification.icon_path = "caminho/para/o/icon.png"  # Substitua pelo caminho do seu ícone
    notification.send()

    # Quando a notificação é clicada, chama a função para abrir a main.py
    notification.bind("<Button-1>", lambda e: abrir_main(categoria))

def abrir_main(categoria):
    # Aqui você pode adicionar a lógica para abrir a main.py
    subprocess.Popen(["python", "main.py", categoria])  # Passa a categoria como argumento




def create_interface():
    root = tk.Tk()
    root.title("Game Store")
    root.geometry("1440x1032")
    root.configure(bg="#1a1a1a")
    root.iconphoto(False,tk.PhotoImage(file="favicon.png"))

    # Menu bar
    def barra_menu():
        # Criar barra de menus com cor personalizada
        menu_bar = Menu(root, bg="#E6C614", fg="#FFFFFF")  # Cor de fundo e texto

        # Menu Principal
        file_menu = Menu(menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF", activebackground="#776500")  # Cor personalizada para o submenu

        # Verificar se uma conta está logada
        try:
            with open("logged_as.txt", "r", encoding="utf-8") as file:
                dados = file.readlines()
                if dados:
                    user_data = dados[0].strip().split("|")
                    username = user_data[0]  # Nome do utilizador logado
                    file_menu.add_command(label=f"Login como: {username}", state="disabled")  # Exibir nome do utilizador
                else:
                    file_menu.add_command(label="Sign up", command=open_create_account)
        except FileNotFoundError:
            file_menu.add_command(label="Sign up", command=open_create_account)

        file_menu.add_command(label="Home", command=filtro)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)
        menu_bar.add_cascade(label="Principal", menu=file_menu)

        # Menu Definições
        help_menu = Menu(menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF", activebackground="#776500")
        help_menu.add_command(label="Utilizador", command=utilizador)
        help_menu.add_command(label="Sobre", command=sobre)
        menu_bar.add_cascade(label="Definições", menu=help_menu)

        # Adicionar a barra de menus na janela principal
        root.config(menu=menu_bar)

    # Open create account page
    def open_create_account():
        try:
            subprocess.Popen(["python", "login.py"])
        except FileNotFoundError:
            messagebox.showerror("Erro", "O ficheiro 'login.py' não foi encontrado!")

    # Go back to filtro
    def filtro():
        try:
            subprocess.Popen(["python", "projeto.py"])
            root.destroy()
        except FileNotFoundError:
            print("Erro ao abrir o arquivo 'projeto.py'")

    # Show about
    def sobre():
        print("Sobre a aplicação Game Store")

    def utilizador():
        try:
            subprocess.Popen(["python", "settings.py"])
        except FileNotFoundError:
            print("Erro ao abrir o arquivo 'settings.py'")

    barra_menu()

    # Canvas and scrollbar setup
    canvas = Canvas(root, bg="#1a1a1a")
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#1a1a1a")

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Main Frame inside the canvas
    main_frame = Frame(scrollable_frame, bg="#1a1a1a")
    main_frame.pack(side="top", fill="both", expand=True)

    trending_label = Label(main_frame, text="Trending", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    trending_label.pack(anchor="w", padx=20, pady=(10, 0))

    trending_frame = Frame(main_frame, bg="#1a1a1a")
    trending_frame.pack(anchor="w", padx=20, pady=10)

    # Function to load and resize images
    def load_image(image_path, width, height):
        try:
            image = Image.open(image_path)
            image = image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Erro ao carregar a imagem {image_path}: {e}")
            return None

    def criar_bind(img_label, jogo_name):
            img_label.bind("<Button-1>", lambda e: abrir_jogo(jogo_name))

    trending_images = ["jogos/Ghost of Yotei/imagem.png", "jogos/Grand Theft Auto VI/imagem.jpg", "jogos/Little Nightmares 3/imagem.jpg"]
    for image_path in trending_images:
        image = load_image(image_path, 399, 245)
        if image:
            trending_item = Frame(trending_frame, bg="#1a1a1a", width=200, height=150)
            trending_item.pack(side="left", padx=10)

            img_label = Label(trending_item, image=image, bg="#1a1a1a")
            img_label.image = image
            img_label.pack()

            jogo_name = os.path.basename(os.path.dirname(image_path)) # Extrai o nome da pasta
            criar_bind(img_label, jogo_name) # chama "criar_bind" para ficar correto em cada

    top_sellers_label = Label(main_frame, text="Top sellers", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    top_sellers_label.pack(anchor="w", padx=20, pady=(20, 0))

    top_sellers_frame = Frame(main_frame, bg="#1a1a1a")
    top_sellers_frame.pack(anchor="w", padx=20, pady=10)

    top_sellers_images = [
        "jogos/Manor Lords/imagem.jpg",
        "jogos/EAFC 25/imagem.png",
        "jogos/Bus Simulator 21/imagem.jpg",
        "jogos/Minecraft/imagem.jpeg",
        "jogos/Rainbow Six Siege/imagem.jpg",
    ]

    for image_path in top_sellers_images:
        image = load_image(image_path, 230, 341)
        if image:
            seller_item = Frame(top_sellers_frame, bg="#1a1a1a", width=230, height=341)
            seller_item.pack(side="left", padx=10)

            img_label = Label(seller_item, image=image, bg="#1a1a1a")
            img_label.image = image
            img_label.pack()

            jogo_name = os.path.basename(os.path.dirname(image_path)) # Extrai o nome da pasta
            criar_bind(img_label, jogo_name) # chama "criar_bind" para ficar correto em cada

    # Additional categories
    categories = [
        {"name": "Ação", "images": ["jogos/Call of Duty Ghosts/imagem.jpg", "jogos/Delta Force/imagem.jpg", "jogos/Mortal Kombat 11/imagem.png", "jogos/Red Dead Redemption/imagem.png", "jogos/Red Dead Redemption 2/imagem.jpg"]},
        {"name": "Aventura", "images": ["jogos/Dark Souls/imagem.jpg", "jogos/Final Fantasy 8/imagem.png", "jogos/Subnautica/imagem.jpg", "jogos/Uncharted 4/imagem.jpg", "jogos/Tomb Raider/imagem.jpg"]},
        {"name": "Simulação", "images": ["jogos/Euro Truck Simulator 2/imagem.jpg", "jogos/Farming Simulator 25/imagem.jpg", "jogos/Planet Zoo/imagem.jpg", "jogos/Spore/imagem.jpg", "jogos/House Flipper 2/imagem.jpg"]},
        {"name": "Desporto", "images": ["jogos/Dakar/imagem.png", "jogos/Descenders/imagem.jpg", "jogos/Football Manager 23/imagem.jpg", "jogos/NBA2K22/imagem.jpg", "jogos/PES2008/imagem.jpg"]},
    ]

    for category in categories:
        category_label = Label(main_frame, text=category["name"], font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
        category_label.pack(anchor="w", padx=20, pady=(20, 0))

        category_frame = Frame(main_frame, bg="#1a1a1a")
        category_frame.pack(anchor="w", padx=20, pady=10)

        for image_path in category["images"]:
            image = load_image(image_path, 230, 341)
            if image:
                category_item = Frame(category_frame, bg="#1a1a1a", width=150, height=200)
                category_item.pack(side="left", padx=10)

                img_label = Label(category_item, image=image, bg="#1a1a1a")
                img_label.image = image
                img_label.pack()

                jogo_name = os.path.basename(os.path.dirname(image_path)) # Extrai o nome da pasta
                criar_bind(img_label, jogo_name) # chama "criar_bind" para ficar correto em cada

    def abrir_jogo(jogo_name):
        print(f"A abrir: {jogo_name}")
        if os.path.exists(f"jogos/{jogo_name}"):
            subprocess.Popen(["python", "jogo.py", jogo_name])
        else:
            messagebox.showerror(
                "Erro",
             f"O jogo \"{jogo_name}\" não existe!"
        )


    root.mainloop()

create_interface()