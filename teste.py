import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk  # Importar Pillow


def create_interface():
    root = tk.Tk()
    root.title("Game Store")
    root.geometry("900x700")
    root.configure(bg="#1a1a1a")

    # Top bar
    top_bar = tk.Frame(root, bg="#0000FF", height=50)
    top_bar.pack(fill="x")

    sign_in_button = Button(top_bar, text="Sign in", bg="black", fg="yellow", font=("Arial", 12), relief="flat")
    sign_in_button.pack(side="right", padx=10, pady=5)

    # Sidebar
    sidebar = tk.Frame(root, bg="#7a6100", width=50)
    sidebar.pack(side="left", fill="y")

    icons = ["🏠", "🔍", "💡"]
    for icon in icons:
        Label(sidebar, text=icon, font=("Arial", 16), bg="#7a6100", fg="white").pack(pady=10)

    # Main Content
    main_frame = tk.Frame(root, bg="#1a1a1a")
    main_frame.pack(side="left", fill="both", expand=True)

    # Trending section
    trending_label = Label(main_frame, text="Trending", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    trending_label.pack(anchor="w", padx=20, pady=(10, 0))

    trending_frame = tk.Frame(main_frame, bg="#1a1a1a")
    trending_frame.pack(anchor="w", padx=20, pady=10)

    # Function to resize images
    def load_image(image_path, width, height):
        try:
            image = Image.open(image_path)  # Abre a imagem
            image = image.resize((width, height), Image.ANTIALIAS)  # Redimensiona a imagem
            return ImageTk.PhotoImage(image)  # Converte para formato Tkinter
        except Exception as e:
            print(f"Erro ao carregar a imagem {image_path}: {e}")
            return None

    # Trending Games
    trending_images = ["imagens/gta.png", "imagens/crew.jpg", "imagens/bus.jpg"]  # Substitua com suas imagens
    for image_path in trending_images:
        image = load_image(image_path, 200, 100)  # Redimensionar para 200x100 pixels
        if image:
            trending_item = tk.Frame(trending_frame, bg="#1a1a1a", width=200, height=150)
            trending_item.pack(side="left", padx=10)

            img_label = Label(trending_item, image=image, bg="#1a1a1a")
            img_label.image = image  # Keep a reference to avoid garbage collection
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
        image = load_image(image_path, 150, 100)  # Redimensionar para 150x100 pixels
        if image:
            seller_item = tk.Frame(top_sellers_frame, bg="#1a1a1a", width=150, height=200)
            seller_item.pack(side="left", padx=10)

            img_label = Label(seller_item, image=image, bg="#1a1a1a")
            img_label.image = image  # Keep a reference to avoid garbage collection
            img_label.pack()

            Button(seller_item, text="wishlist", bg="gray", fg="white").pack(pady=5)
            Button(seller_item, text="Buy", bg="yellow", fg="black").pack()

    root.mainloop()


create_interface()
