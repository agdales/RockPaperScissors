import tkinter as tk


class TestGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg="gray15")
        parent.config(bg="dodger blue")

        self.intro_label = tk.Label(self, text="This is a title", bg="light blue")
        self.side_bar = tk.Label(self, bg="lemon chiffon", width=10)
        self.text_label1 = tk.Label(self, text="TextLabel1", bg="pale green")
        self.text_label2 = tk.Label(self, text="TextLabel2", bg="powder blue")
        self.edit1 = tk.Entry(self, bg="light coral")
        self.edit2 = tk.Entry(self, bg="maroon")
        self.button1 = tk.Button(self, text="Button1")
        self.button2 = tk.Button(self, text="Button1")

        self.intro_label.grid(row=0, column=0, columnspan=3, sticky="news")
        self.side_bar.grid(row=1, column=0, rowspan=3, sticky="nsew")
        self.text_label1.grid(row=1, column=1, padx=(10, 30), pady=10)
        self.text_label2.grid(row=2, column=1, sticky="ew")
        self.button1.grid(row=3, column=1)
        self.edit1.grid(row=1, column=2)
        self.edit2.grid(row=2, column=2)
        self.button2.grid(row=3, column=2)

        for i in range(3):
            self.columnconfigure(i, weight=1, minsize=100)

        for i in range(4):
            self.rowconfigure(i, weight=1, minsize=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TK inter GUI trial")
    root.geometry('300x300')
    my_frame = TestGUI(root)
    my_frame.pack(fill="both", expand=True, padx=5, pady=5)
    root.mainloop()
