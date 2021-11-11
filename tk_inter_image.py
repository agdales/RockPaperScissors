import tkinter as tk
from PIL import Image, ImageTk


def press_scissors():
    print("Pressed the scissors button")


img_scissors = Image.open("scissors2.png")
print(img_scissors.format, img_scissors.mode)
img_scissors = img_scissors.reduce(4)
img_scissors_sm = img_scissors.reduce(2)

root = tk.Tk()
canvas = tk.Canvas(root, height=300, width=300, bg="pink")
img = ImageTk.PhotoImage(img_scissors)
canvas.create_image(150, 150, anchor=tk.CENTER, image=img)
my_label = tk.Label(root, text="Scissors Button", font=('Verdana', 15))
img_sm = ImageTk.PhotoImage(img_scissors_sm)
my_button = tk.Button(root, text="Click Me!",
                      image=img_sm,
                      command=press_scissors,
                      bg="yellow")

canvas.pack(padx=5, pady=5)
my_label.pack(pady=5)
my_button.pack(pady=10)

root.mainloop()
