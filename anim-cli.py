import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

from anim import resize_animated

input("Selecciona el sticker (presionar ENTER)")
sticker_path = filedialog.askopenfilename()
sticker_path = sticker_path.lower()

if sticker_path.endswith((".gif", ".webp")):

    resize_animated(sticker_path, 512)

    print("LISTO.")
else:
    print("TIPO DE ARCHIVO INVALIDO")