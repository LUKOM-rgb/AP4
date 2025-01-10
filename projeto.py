import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from PIL import Image, ImageTk  # Para trabalhar com imagens

class jogostoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Games Store")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C2C2C")

        # Lista de desejos
        self.lista = []

        # Dados dos jogos, incluindo os caminhos das capas
        self.jogos_data = [
            {"name": "Grand Theft Auto V", "Genero": "Ação", "Capa": "imagens/gta_v.png"},
            {"name": "Ready or Not", "Genero": "Ação", "Capa": "imagens/ready_or_not.png"},
            {"name": "Grand Theft Auto Online", "Genero": "Ação", "Capa": "imagens/gta_online.png"},
            {"name": "Manor Lords", "Genero": "Simulação", "Capa": "imagens/manor_lords.png"},
            {"name": "EAFC 25", "Genero": "Desporto", "Capa": "imagens/eafc_25.png"},
            {"name": "Bus Simulator 21", "Genero": "Simulação", "Capa": "imagens/bus_simulator.png"},
            {"name": "Minecraft", "Genero": "Aventura", "Capa": "imagens/minecraft.png"},
            {"name": "Rainbow Six Siege", "Genero": "Ação", "Capa": "imagens/rainbow_six.png"}
        ]

        # Frame para filtros
        self.filter_frame = Frame(self.root, bg="#2C2C2C", width=150)
        self.filter_frame.pack(side=tk.RIGHT, fill=tk.Y)

        Label(self.filter_frame, text="Filtros", bg="#2C2C2C", font=("Inter", 14, "bold"), fg="#2C2C2C").pack(pady=10)

        # Adicionar filtros
        filtros = ["Ação", "Aventura", "Simulação", "Desporto", "todos"]
        for filtro in filtros:
            Button(self.filter_frame, text=filtro.capitalize(), font=("Inter", 12), bg="#2C2C2C", fg="#FFFFFF", 
                   activebackground="#2C2C2C", activeforeground="#2C2C2C",
                   command=lambda g=filtro: self.filter_jogos(g)).pack(fill=tk.X, pady=5)

        # Botão para abrir lista de desejos
        Button(self.filter_frame, text="Lista de Desejos", font=("Inter", 12, "bold"), bg="#FFFFFF", fg="#2C2C2C",
               command=self.open_lista).pack(fill=tk.X, pady=20)

        # Frame para exibição de jogos
        self.jogo_display_frame = Frame(self.root, bg="#2C2C2C")
        self.jogo_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.display_jogos(self.jogos_data)

    def display_jogos(self, jogos):
        # Limpar o frame de exibição
        for widget in self.jogo_display_frame.winfo_children():
            widget.destroy()

        if not jogos:
            Label(self.jogo_display_frame, text="Não há jogos disponíveis", font=("Inter", 14), bg="#FFFFFF", fg="#FFFFFF").pack(pady=20)
            return

        row_frame = None
        for index, jogo in enumerate(jogos):
            if index % 5 == 0:  # Novo row_frame a cada 5 jogos
                row_frame = Frame(self.jogo_display_frame, bg="#2C2C2C")
                row_frame.pack(fill=tk.X, pady=10)
            self.create_card(row_frame, jogo)

    def create_card(self, parent, jogo):
        card_frame = Frame(parent, bg="#FFFFFF", relief="sunken", borderwidth=1, padx=10, pady=10)
        card_frame.pack(side=tk.LEFT, padx=10)

        # Carregar imagem da capa
        try:
            img = Image.open(jogo["Capa"])
            img = img.resize((100, 150))  # Redimensiona a capa
            photo = ImageTk.PhotoImage(img)
            img_label = Label(card_frame, image=photo, bg="white")
            img_label.image = photo  # Mantém uma referência para a imagem
            img_label.pack(pady=5)
        except Exception:
            Label(card_frame, text="Capa não disponível", bg="white", font=("Inter", 10)).pack(pady=5)

        Label(card_frame, text=jogo["name"], font=("Inter", 12, "bold"), bg="white").pack(pady=5)

        Label(card_frame, text=f"Gênero: {jogo['Genero']}", font=("Inter", 10), bg="white").pack(pady=5)

        Button(card_frame, text="Adicionar à lista", command=lambda g=jogo["name"]: self.add_to_lista(g)).pack(pady=5)

    def add_to_lista(self, jogo):
        if jogo not in self.lista:
            self.lista.append(jogo)
            messagebox.showinfo("Lista de desejos", f"{jogo} foi adicionado à sua lista de desejos!")
        else:
            messagebox.showinfo("Lista de desejos", f"{jogo} já está na sua lista de desejos!")

    def open_lista(self):
        lista_window = tk.Toplevel(self.root)
        lista_window.title("Lista de Desejos")
        lista_window.geometry("600x400")
        lista_window.configure(bg="#2C2C2C")

        Label(lista_window, text="Sua Lista de Desejos", font=("Inter", 16, "bold"), bg="#2C2C2C", fg="#E6C614").pack(pady=10)

        # Exibição dos itens da lista de desejos
        for jogo in self.lista:
            self.create_lista_card(lista_window, jogo)

    def create_lista_card(self, parent, jogo_name):
        card_frame = Frame(parent, bg="#FFFFFF", relief="sunken", borderwidth=1, padx=10, pady=10)
        card_frame.pack(pady=5, fill=tk.X)

        Label(card_frame, text=jogo_name, font=("Inter", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=5)

        remove_button = Button(card_frame, text="Remover", command=lambda g=jogo_name: self.remove_from_lista(g, card_frame))
        remove_button.pack(side=tk.RIGHT, padx=5)

    def remove_from_lista(self, jogo, frame):
        if jogo in self.lista:
            self.lista.remove(jogo)
            frame.destroy()
            messagebox.showinfo("Lista", f"{jogo} foi removido da sua lista.")

    def filter_jogos(self, Genero):
        if Genero == "todos":
            Filtro_jogos = self.jogos_data
        else:
            Filtro_jogos = [jogo for jogo in self.jogos_data if jogo["Genero"] == Genero]

        self.display_jogos(Filtro_jogos)


if __name__ == "__main__":
    root = tk.Tk()
    app = jogostoreApp(root)
    root.mainloop()
