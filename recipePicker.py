from tkinter import ttk
import tkinter as tk
from tkinter import *
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet

pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")


bg_color = '#3d6466'
btn_color = '#28393a'
btn_onHover = '#badee2'


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def fetch_db():
    connection = sqlite3.connect('data/recipes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM sqlite_schema WHERE type="table";')
    all_tables = cursor.fetchall()
    idx = random.randint(0, len(all_tables)-1)

    # fetch ingredients
    table_name = all_tables[idx][1]
    cursor.execute('SELECT * FROM ' + table_name + ';')
    table_records = cursor.fetchall()

    print(all_tables[idx])
    print(table_records)
    connection.close()

    return table_name, table_records


def pre_process(table_name, table_records):
    # tittle
    tittle = table_name[:-6]
    tittle = "".join(
        [char if char.islower() else " " + char for char in tittle])
    tittle = tittle.lstrip()
    # print(tittle)

    # ingredients
    ingredients = []
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
      # 2 cups of sugar
        ingredients.append(qty + " " + unit + " of " + name)
    # print(ingredients)
    return tittle, ingredients


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    # Frame1 widgets
    logo_img = ImageTk.PhotoImage(file='assets/RRecipe_logo.png')
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(
        frame1,
        text='Ready for your random recipe?',
        bg=bg_color,
        fg='White',
        font=('Ubuntu', 14),
        pady=25
    ).pack()

# Button widget

    tk.Button(
        frame1,
        text='SHUFFLE',
        font=('Ubuntu, 20'),
        bg=btn_color,
        fg='White',
        cursor='hand2',
        activebackground=btn_onHover,
        activeforeground='black',
        command=lambda: load_frame2(),
        height=1,
        width=10,
    ).pack(pady=20)


def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    table_name, table_records = fetch_db()
    tittle, ingredients = pre_process(table_name, table_records)

    # logo
    logo_img = ImageTk.PhotoImage(file='assets/RRecipe_logo_bottom.png')
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    tk.Label(
        frame2,
        text=tittle,
        bg=bg_color,
        fg='White',
        font=('Ubuntu', 20),
        pady=25
    ).pack(pady=25)

    for i in ingredients:
        tk.Label(
            frame2,
            text=i,
            bg=btn_color,
            fg='White',
            font=('Shanti', 12),
            pady=5
        ).pack(fill="both", padx=20)

    tk.Button(
        frame2,
        text='BACK',
        font=('Ubuntu, 18'),
        bg=btn_color,
        fg='White',
        cursor='hand2',
        activebackground=btn_onHover,
        activeforeground='black',
        command=lambda: load_frame1(),
        height=0,
        width=7,
    ).pack(pady=20)

    # initiallize app
root = tk.Tk()
root.title('Recipe Picker')
root.eval('tk::PlaceWindow . center')
# x = root.winfo_screenwidth() // 2
# y = int(root.winfo_screenheight() * 0.1)
# root.geometry('600x700+' + str(x) + '+' + str(y))


# Create a frame widget
frame1 = tk.Frame(root, width=600, height=700, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky='nesw')

load_frame1()
# run app
root.mainloop()
