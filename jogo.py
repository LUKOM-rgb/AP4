import os
import tkinter as tk
from tkinter import Text, Tk, messagebox, Frame, Label, Button, Canvas, PhotoImage
from PIL import Image, ImageTk
import sys

# Função para adicionar avaliação
def adicionar_review(jogo_name):
    review_window = tk.Toplevel()
    review_window.title(f"Adicionar avaliação para {jogo_name}")
    review_window.geometry("400x300")
    review_window.configure(bg="#2C2C2C")

    label = tk.Label(review_window, text="Introduza sua avaliação:", fg="#E6C614", bg="#2C2C2C")
    label.pack(pady=10)

    entry_review = tk.Entry(review_window, width=50)
    entry_review.pack(pady=10)

    def guardar_review():
        review_text = entry_review.get()
        if review_text and user_data:  # Verifica se user_data está definido
            # Guardar a avaliação no arquivo de reviews
            with open(f"jogos/{jogo_name}/reviews.txt", "a", encoding="utf-8") as file:
                file.write(f"{user_data[0]};{review_text}\n")  # user_data[0] é o nome do utilizador
            messagebox.showinfo("Sucesso", "avaliação adicionada com sucesso!")
            review_window.destroy()
        else:
            messagebox.showerror("Erro", "A avaliação não pode estar vazia ou não tem sessão iniciada.")

    button_guardar = tk.Button(review_window, text="Guardar avaliação", command=guardar_review, bg="#E6C614" ,activebackground="#776500")
    button_guardar.pack(pady=20)

# Ler de projeto.py
if len(sys.argv) > 1:
    jogo_name = sys.argv[1]
    print(f"{jogo_name} carregado com sucesso!")
else:
    print("Não foi especificado um jogo.")

# Configurações principais
root = Tk()
root.title(f"{jogo_name}")
root.geometry("1920x1080")
root.configure(bg="#2C2C2C")

# Frame principal
main_frame = Frame(root, bg="#2C2C2C")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Seção da esquerda (Vídeo e Avaliação)
left_frame = Frame(main_frame, bg="#2C2C2C")
left_frame.grid(row=0, column=0, sticky="n")

# Imagem
imagem = None
for ext in [".png", ".jpg", ".jpeg"]:
    potencial_imagem = f"jogos/{jogo_name}/imagem{ext}"
    if os.path.exists(potencial_imagem):
        imagem = potencial_imagem
        break

canvas = Canvas(left_frame, width=800, height=400, bg="#2C2C2C", highlightthickness=0)
if os.path.exists(imagem):
    try:
        img = Image.open(imagem)
        img = img.resize((800, 400))
        image = ImageTk.PhotoImage(img)
        canvas.create_image(400, 200, image=image)
        canvas.image = image  # Necessário para evitar que a imagem seja descarregada
    except Exception as e:
        canvas.create_rectangle(0, 0, 800, 400, fill="gray")
        canvas.create_text(400, 200, text=f"Erro: {e}", font=("Inter", 14), fill="white")
else:
    # Exibir um retângulo cinza e um ícone de aviso
    canvas.create_rectangle(0, 0, 800, 400, fill="gray")
    canvas.create_text(400, 200, text="⚠", font=("Inter", 48), fill="white")

canvas.pack()

# Avaliação
rating_frame = Frame(left_frame, bg="#2C2C2C")
rating_frame.pack(pady=10)

stars = []

with open(f"jogos/{jogo_name}/data.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    if len(lines) > 1:
        rating = float(lines[1].strip())

        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star

        stars.extend(["★"] * full_stars)
        if half_star: stars.append("⯨")
        stars.extend(["☆"] * empty_stars)
for star in stars:
    star_label = Label(rating_frame, text=star, font=("Inter", 20), bg="#2C2C2C", fg="yellow")
    star_label.pack(side="left")

rating_label = Label(rating_frame, text=f"{rating} / 5", font=("Inter", 20), bg="#2C2C2C", fg="white")
rating_label.pack(side="left", padx=10)

# Seção da direita (Descrição)
right_frame = Frame(main_frame, bg="#2C2C2C")
right_frame.grid(row=0 , column=4, sticky="n", padx=100)

description_title = Label(right_frame, text="Descrição", font=("Inter", 16), bg="#2C2C2C", fg="white")
description_title.pack(anchor="w")

description_text = Text(right_frame, height=15, width=70, bg="#2C2C2C", fg="white", wrap="word")
with open(f"jogos/{jogo_name}/data.txt", "r", encoding="utf-8") as file:
    description_text.insert("1.0", file.readline().strip())
description_text.config(state="disabled")
description_text.pack()

# Reviews
review_title = Label(main_frame, text="Reviews:", font=("Inter", 16), bg="#2C2C2C", fg="white")
review_title.grid(row=1, column=0, sticky="w", pady=5)

reviews_frame = Frame(main_frame, bg="#2C2C2C")
reviews_frame.grid(row=2, column=0, columnspan=2, sticky="w")

# Adicionar botão para adicionar avaliação
add_review_button = Button(main_frame, text="Adicionar avaliação", bg="#E6C614", fg="#FFFFFF", activebackground="#776500",command=lambda: adicionar_review(jogo_name))
add_review_button.grid(row=3, column=0, sticky="w", pady=30)

# Função para carregar reviews de um arquivo
def carregar_reviews(arquivo):
    reviews_list = []
    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            for line in file:
                Utilizador, texto = line.strip().split(";", 1)
                reviews_list.append(f"{Utilizador} - {texto}")
    except FileNotFoundError:
        reviews_list.append("Erro: Arquivo de reviews não encontrado.")
    return reviews_list

reviews = carregar_reviews(f"jogos/{jogo_name}/reviews.txt")
for avaliação in reviews:
    review_label = tk.Label(reviews_frame, text=avaliação, font=("Inter", 12), bg="#2C2C2C", fg="white", anchor="w")
    review_label.pack(anchor="w", pady=2)  # adicionar o label à frame
try:
    with open("logged_as.txt", "r", encoding="utf-8") as file:
        dados = file.readlines()

    # Verificar se o nome de utilizador e senha correspondem
    for line in dados:
        user_data = line.strip().split("|")  # Dividir
        print(f"{user_data}")
except FileNotFoundError:
    messagebox.showerror("Não tem sessão iniciada!")

# Rodar a aplicação
root.mainloop()