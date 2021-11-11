import tkinter as tk
from game_objects import Game


class TestGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.edit_text = tk.StringVar()

        self.intro_label = tk.Label(self, text="Press button to say Hello", bg="light blue")
        self.hello_button = tk.Button(self, text='Say Hello (H)', command=self.press_button, bg="ivory2")
        self.text_area = tk.Label(self, textvariable=self.edit_text, width=20, height=5, bg="gold")
        self.edit_box = tk.Entry(self)
        self.print_button = tk.Button(self, text='Print edit box', command=self.entry_print)

        self.edit_box.insert(0, 'default')

        self.intro_label.pack(padx=10, pady=5)
        self.hello_button.pack(pady=5)
        self.text_area.pack(padx=10, pady=(5, 10))
        self.edit_box.pack(pady=(5, 10))
        self.print_button.pack(pady=(5, 10))

        self.bind('<Key>', self.press_key)
        # Put focus on the frame to allow key bind to work
        self.focus()

    def entry_print(self):
        print(self.edit_box.get())

    def press_button(self):
        txt = self.edit_text.get()
        txt += "Hello World!\n"
        self.edit_text.set(txt)

    def press_key(self, event):
        key_pressed = event.char.lower()
        if key_pressed == "h":
            self.hello_button.invoke()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TK inter GUI trial")
    root.geometry('300x300')
    TestGUI(root).pack()
    root.mainloop()
