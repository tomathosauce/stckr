import os, argparse, time
parser = argparse.ArgumentParser()

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

from stckr import  create_pack

title = input("Titulo del pack: ")
author = input("Autor del pack: ")
input("Selecciona el icono del pack (presionar ENTER)")
thumbnail = filedialog.askopenfilename()
print(thumbnail)

if not thumbnail:
    exit()

input("Selecciona las imagenes (presionar ENTER)")
files = filedialog.askopenfilenames(parent=root,title='Choose a file')
print(files)

if not files:
    exit()

input("Selecciona la carpeta (presionar ENTER)")
path = filedialog.askdirectory(parent=root,title='Choose a folder')

if not path:
    exit()

create_pack(title, author, thumbnail, path)