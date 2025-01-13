import tkinter as tk
from tkinter import Button, Label, Menu
from PIL import Image, ImageTk  # Importar Pillow
import subprocess

def create_interface():
    root = tk.Tk()
    root.title("Game Store")
    root.geometry("1440x1032")
    root.configure(bg="#1a1a1a")

    # Barra de Menu
    def barra_menu():
        menu_bar = Menu(root, bg="#E6C614", fg="#FFFFFF")  # Cor de fundo e texto

        # Menu Arquivo
        file_menu = Menu(menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF")
        file_menu.add_command(label="Sign up", command=open_create_account)
        file_menu.add_command(label="Filtro", command=home)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)

        # Menu Ajuda
        help_menu = Menu(menu_bar, tearoff=0, bg="#E6C614", fg="#FFFFFF")
        help_menu.add_command(label="Sobre", command=sobre)
        menu_bar.add_cascade(label="Ajuda", menu=help_menu)

        # Adicionar a barra de menus na janela principal
        root.config(menu=menu_bar)

    # Função para abrir a página de cadastro
    def open_create_account():
        try:
            subprocess.Popen(["python", "login.py"])
        except FileNotFoundError:
            print("Erro ao abrir o arquivo 'login.py'")

    # Função para voltar para a home
    def home():
        try:
            subprocess.Popen(["python", "projeto.py"])
            root.destroy()
        except FileNotFoundError:
            print("Erro ao abrir o arquivo 'projeto.py'")

    # Função para exibir o sobre
    def sobre():
        print("Sobre a aplicação Game Store")

    barra_menu()

    # Main Content
    main_frame = tk.Frame(root, bg="#1a1a1a")
    main_frame.pack(side="left", fill="both", expand=True)

    # Trending section
    trending_label = Label(main_frame, text="Trending", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    trending_label.pack(anchor="w", padx=20, pady=(10, 0))

    trending_frame = tk.Frame(main_frame, bg="#1a1a1a")
    trending_frame.pack(anchor="w", padx=20, pady=10)

    # Função para redimensionar imagens
    def load_image(image_path, width, height):
        try:
            image = Image.open(image_path)
            image = image.resize((width, height), Image.LANCZOS)  # Usando LANCZOS
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Erro ao carregar a imagem {image_path}: {e}")
            return None

    # Trending Games
    trending_images = ["imagens/gta6.jpg", "imagens/banner2.jpg", "imagens/banner.png"]
    for image_path in trending_images:
        image = load_image(image_path, 390, 243)
        if image:
            trending_item = tk.Frame(trending_frame, bg="#1a1a1a", width=200, height=150)
            trending_item.pack(side="left", padx=10)

            img_label = Label(trending_item, image=image, bg="#1a1a1a")
            img_label.image = image
            img_label.pack()

    # Top Sellers section
    top_sellers_label = Label(main_frame, text="Top sellers", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    top_sellers_label.pack(anchor="w", padx=20, pady=(20, 0))

    top_sellers_frame = tk.Frame(main_frame, bg="#1a1a1a")
    top_sellers_frame.pack(anchor="w", padx=20, pady=10)

    # Top Sellers Games
    top_sellers_images = [
        "imagens/lords.jpg",
        "imagens/fc_25.png",
        "imagens/Bus.jpg",
        "imagens/mine.jpeg",
        "imagens/R6.jpg",
    ]

    for image_path in top_sellers_images:
        image = load_image(image_path, 230, 341)
        if image:
            seller_item = tk.Frame(top_sellers_frame, bg="#1a1a1a", width=150, height=200)
            seller_item.pack(side="left", padx=10)

            img_label = Label(seller_item, image=image, bg="#1a1a1a")
            img_label.image = image
            img_label.pack()

            Button(seller_item, text="wishlist", bg="gray", fg="white").pack(pady=5)

    root.mainloop()

create_interface()