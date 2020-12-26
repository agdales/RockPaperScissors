import tkinter as tk


class TestGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.edit_text = tk.StringVar()

        self.intro_label = tk.Label(self, text="Press button to say Hello")
        self.hello_button = tk.Button(self, text='Say Hello (H)', command=self.press_button)
        self.text_area = tk.Label(self, textvariable=self.edit_text, width=20, height=5)

        self.intro_label.pack(padx=10, pady=5)
        self.hello_button.pack(pady=5)
        self.text_area.pack(padx=10, pady=(5, 10))

        self.bind('<Key>', self.press_key)
        self.hello_button.focus()
        self.focus()

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
    TestGUI(root).pack()
    root.mainloop()