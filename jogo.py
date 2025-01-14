import os
import tkinter as tk
from tkinter import Text, Tk, messagebox, Frame, Label, Button, Menu, Canvas, PhotoImage
import sys

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
imagem = f"jogos/{jogo_name}/imagem.png"
canvas = Canvas(left_frame, width=600, height=300, bg="#2C2C2C", highlightthickness=0)
if os.path.exists(imagem):
    image = PhotoImage(file=imagem)
    canvas.create_image(300, 150, image=image)
else:
    canvas.create_rectangle(0, 0, 600, 300, fill="gray")
    canvas.create_text(300, 150, text="⚠", font=("Inter", 48), fill="white")
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
right_frame.grid(row=0, column=1, sticky="n", padx=20)

description_title = Label(right_frame, text="Descrição", font=("Inter", 16), bg="#2C2C2C", fg="white")
description_title.pack(anchor="w")

description_text = Text(right_frame, height=15, width=40, bg="#2C2C2C", fg="white", wrap="word")
with open(f"jogos/{jogo_name}/data.txt", "r", encoding="utf-8") as file:
    description_text.insert("1.0", file.readline().strip())
description_text.config(state="disabled")
description_text.pack()

# Reviews
review_title = Label(main_frame, text="Reviews:", font=("Inter", 16), bg="#2C2C2C", fg="white")
review_title.grid(row=1, column=0, sticky="w", pady=10)

reviews_frame = Frame(main_frame, bg="#2C2C2C")
reviews_frame.grid(row=2, column=0, columnspan=2, sticky="w")

# Função para carregar reviews de um arquivo
def carregar_reviews(arquivo):
    reviews_list = []
    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            for line in file:
                usuario, texto = line.strip().split(";", 1)
                reviews_list.append(f"{usuario} - {texto}")
    except FileNotFoundError:
        reviews_list.append("Erro: Arquivo de reviews não encontrado.")
    return reviews_list

reviews = carregar_reviews(f"jogos/{jogo_name}/reviews.txt")
for review in reviews:
    review_label = tk.Label(reviews_frame, text=review, font=("Inter", 12), bg="black", fg="white", anchor="w")
    review_label.pack(anchor="w")

# Rodar a aplicação
root.mainloop()
