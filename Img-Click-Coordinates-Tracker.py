import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

coordinates = {}
click_count = 1

def on_click(event):
    global click_count
    x = event.x
    y = event.y
    filename = coordinates.get('filename')
    if filename:
        if filename in coordinates:
            coordinates[filename][click_count] = (x, y)
        else:
            coordinates[filename] = {click_count: (x, y)}
        save_coordinates()
        print(f"Clicked at ({x}, {y})")
        draw_click_number(event)
        click_count += 1
    else:
        print("Please open an image first.")

def open_image():
    global click_count
    click_count = 1  # Reset click count when opening a new image
    filename = filedialog.askopenfilename()
    if filename:
        image = Image.open(filename)
        photo = ImageTk.PhotoImage(image)
        canvas.config(width=image.width, height=image.height)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo, tags="image")
        canvas.image = photo  # Keep a reference to avoid garbage collection
        coordinates['filename'] = filename

def save_coordinates():
    filename = coordinates.get('filename')
    if filename:
        with open(f"{filename}_coordinates.txt", "w") as f:
            for click_id, (x, y) in coordinates[filename].items():
                f.write(f"Click {click_id}: ({x}, {y})\n")
        print("Coordinates saved to file")

def get_color(click_count):
    if click_count <= 20:
        return "brown"
    elif click_count <= 27:
        return "blue"
    elif click_count <= 33:
        return "green yellow"
    elif click_count <= 36:
        return "yellow"
    else:
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Generate random hex color code

def draw_click_number(event):
    x = event.x
    y = event.y
    fill_color = get_color(click_count)
    canvas.create_text(x, y, text=str(click_count), fill=fill_color, tags="number")

root = tk.Tk()
root.title("Image Viewer")

canvas = tk.Canvas(root)
canvas.pack()

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

canvas.bind("<Button-1>", on_click)

root.mainloop()
