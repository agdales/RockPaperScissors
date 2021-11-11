import tkinter as tk
from game_objects import Game


class GameApp(tk.Tk):
    """ GameApp initialises a game and a Tk instance (window)
    The window includes a title and sets up frames with the different views on the game
    The show_frame method unpacks all the frames except for the one that needs to be shown """
    def __init__(self):
        super().__init__()
        self.title('Rock, Paper, Scissors game')
        self.resizable(False, False)
        self.game = create_game()

        # creating a container
        container = tk.Frame(self)
        container.pack()

        # Create an overall title and pack it into the top of the container
        title_label = tk.Label(container,
                               text="Rock, Paper, Scissors",
                               bg="red", fg="white",
                               width=30,
                               font=("Arial", 20))
        title_label.pack()

        # Initialise frames to an empty dictionary
        self.frames = {}

        # Set up frames for each of the page classes
        pages = (GameOptionsGUI, GameGUI)
        for F in pages:
            # Sets up each frame with the GameApp (self) as the controller
            frame = F(self)
            self.frames[F] = frame

        self.show_frame(GameOptionsGUI)

    # Method to show the desired game class, which is a subclass of tk.Frame
    def show_frame(self, current_frame):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[current_frame].pack(fill=tk.X)
        self.frames[current_frame].set_up()


class GameOptionsGUI(tk.Frame):
    """ GameOptionsGUI is a subclass of tk.Frame that allows the user to enter options and then start the game"""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.game = controller.game
        self.player = self.game.player

        # Set up user_name and num_rounds as tkinter variables
        self.user_name = tk.StringVar()
        self.num_rounds = tk.IntVar()

        name_label = tk.Label(self, text="Player Name:")
        rounds_label = tk.Label(self, text="Number of Rounds:")

        # the validate command must be registered this allows the value of the edit box after it is typed, but before
        # it is accepted to be passed as '%P'
        vcmd = (self.register(self.validate_entry), '%P')
        self.name_edit = tk.Entry(self, textvariable=self.user_name,
                                  name='editbox',
                                  validate='key', validatecommand=vcmd,
                                  justify=tk.CENTER, width=15)
        round_spin = tk.Spinbox(self, textvariable=self.num_rounds,
                                state='readonly',
                                from_=1, to=100, justify=tk.CENTER, width=13)
        self.start_button = tk.Button(self, text="Start game",
                                      state=tk.DISABLED,
                                      command=self.start_game,
                                      width=15)
        self.quit_button = tk.Button(self, text="Quit",
                                     width=15, command=self.controller.destroy)

        name_label.grid(row=1, column=0, pady=5)
        rounds_label.grid(row=2, column=0, pady=5)

        self.name_edit.grid(row=1, column=1, pady=5)
        round_spin.grid(row=2, column=1, pady=5)
        self.quit_button.grid(row=5, column=0, pady=(5, 10))
        self.start_button.grid(row=5, column=1, pady=(5, 10))

        # Ensure the columns in the grid are equally spaced
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Binds the return key to have the same effect a pressing the start_button
        self.controller.bind('<Return>', lambda event=None: self.start_button.invoke())

    def set_up(self):
        if self.game.players:
            self.user_name.set(self.player.name)
        if self.game.max_rounds:
            self.num_rounds.set(self.game.max_rounds)
        else:
            self.num_rounds.set(5)
        # Put the cursor in the name_edit box and focus on the current frame (so that key strokes binds work)
        self.name_edit.focus()
        self.focus()

    def start_game(self):
        self.game.set_max_rounds(self.num_rounds.get())
        # Switch to the GameGUI frame.
        self.controller.show_frame(GameGUI)

    def validate_entry(self, user_name):
        # Validation routine, only allows the start_button to be pressed if the name entered obeys validation rules
        if (0 < len(user_name) < 13) and user_name.isalpha():
            self.start_button.config(state=tk.NORMAL)
            self.player.set_name(user_name)
        elif len(user_name) == 0:
            self.start_button.config(state=tk.DISABLED)
        else:
            return False
        return True


class GameGUI(tk.Frame):
    def __init__(self, controller):
        # Initialises the GameGUI as an instance of its superclass - a tkinter frame
        super().__init__()

        self.controller = controller
        self.game = controller.game

        self.report_message = tk.StringVar()
        self.results_message = tk.StringVar()

        self.outcome = tk.Label(self, textvariable=self.report_message, bg="blue", fg="white", width=30)

        # Creates a dictionary with the action buttons for 'rock', 'paper' and scissors
        # Use the 'anonymous function' lambda to give a callback command with an argument
        self.action_buttons = \
            {'rock': tk.Button(self, text="Rock (R)", width=15, command=lambda: self.select_object("rock")),
             'paper': tk.Button(self, text="Paper (P)", width=15, command=lambda: self.select_object("paper")),
             'scissors': tk.Button(self, text="Scissors (S)", width=15, command=lambda: self.select_object("scissors"))}

        self.quit_button = tk.Button(self, text="Quit", width=15, command=self.controller.destroy)
        self.restart_button = tk.Button(self, text="New game (N)", width=15, command=self.restart_game)
        self.options_button = tk.Button(self, text="Change Options (O)", width=15, command=self.reset_game)
        self.results = tk.Label(self, textvariable=self.results_message, height=2)

        # Place objects on the grid
        for i, btn in enumerate(self.action_buttons.values(), 1):
            btn.grid(row=i, column=0, pady=5)
        self.outcome.grid(row=1, column=1, rowspan=3)
        self.results.grid(row=4, column=0, columnspan=2, pady=5)
        self.quit_button.grid(row=5, column=0, pady=(5, 10), rowspan=2)
        self.restart_button.grid(row=5, column=1, pady=5)
        self.options_button.grid(row=6, column=1, pady=(5, 10))

        # Ensure the columns in the grid are equally spaced
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Binds the return key to have the same effect a pressing the start_button
        self.bind('<Key>', self.press_key)

    def set_up(self):
        self.report_message.set("Choose rock, paper or scissors to start")
        self.results_message.set(
            f"Welcome {self.game.players[0].name}. You have {self.game.max_rounds} rounds to play")
        # Focus on the current frame (so that key strokes binds work)
        self.focus()

    def press_key(self, event):
        key_pressed = event.char.lower()
        if key_pressed == "r":
            self.action_buttons["rock"].invoke()
        if key_pressed == "p":
            self.action_buttons["paper"].invoke()
        if key_pressed == "s":
            self.action_buttons["scissors"].invoke()
        if key_pressed == "o":
            self.options_button.invoke()
        if key_pressed == "n":
            self.restart_button.invoke()
        if key_pressed == "q" or event.keysym == "Escape":
            self.quit_button.invoke()

    def select_object(self, item):
        self.game.next_round()
        self.game.players[0].choose_object(item)
        self.game.players[1].choose_object()
        self.game.find_winner()
        self.show_report()

    def show_report(self):
        if self.game.current_round == 0:
            self.set_up()
        else:
            self.report_message.set(self.game.report_round())
            result_msg = self.game.report_score()
            result_msg = result_msg.replace("\n", " ")

            if self.game.is_finished():
                result_msg += "\n" + self.game.report_winner()
                for btn in self.action_buttons.values():
                    btn.config(state=tk.DISABLED)
            else:
                result_msg += f"\nYou have {self.game.max_rounds - self.game.current_round} rounds left to play"

            self.results_message.set(result_msg)

    def restart_game(self):
        self.game.reset()
        self.show_report()
        for btn in self.action_buttons.values():
            btn.config(state=tk.NORMAL)

    def reset_game(self):
        self.restart_game()
        # Switch to the GameOptionsGUI frame.
        self.controller.show_frame(GameOptionsGUI)


def create_game():
    """Create a game instance"""
    game = Game()
    game.player = game.add_human_player()
    game.add_computer_player()
    return game


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
