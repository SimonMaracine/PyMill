"""Main game module. It must be imported from the game folder and its main() executed."""

import threading
import tkinter as tk
from os.path import join

from PIL import Image, ImageTk

from src.game.pymill_hotseat import PyMillHotseat
from src.game.pymill_computer import PyMillComputer

VERSION = "v0.2.0"


class PyMillMenu(tk.Frame):

    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.root = root
        self.pack(padx=20, pady=20, expand=True)

        self.root.option_add("*tearOff", False)
        self.root.minsize(width=640, height=480)
        self.root.title("PyMill")

        self.in_game = False

        frm_buttons = tk.Frame(self)
        frm_buttons.grid(row=0, sticky=tk.S, pady=60)

        img_player_vs_player = Image.open(join("gfx", "player_vs_player.png")).resize((160, 160), Image.ANTIALIAS)
        self.img_player_vs_player = ImageTk.PhotoImage(img_player_vs_player)

        img_player_vs_computer = Image.open(join("gfx", "player_vs_computer.png")).resize((160, 160), Image.ANTIALIAS)
        self.img_player_vs_computer = ImageTk.PhotoImage(img_player_vs_computer)

        img_player_vs_player_net = Image.open(join("gfx", "player_vs_player_net.png")).resize((160, 160), Image.ANTIALIAS)
        self.img_player_vs_player_net = ImageTk.PhotoImage(img_player_vs_player_net)

        btn1 = tk.Button(frm_buttons, image=self.img_player_vs_player, command=self.run_pymill_hotseat)
        btn1.grid(column=0, row=0, padx=4)
        btn1.bind("<Enter>", lambda event: self.change_label_text("Play with a friend on the same computer"))
        btn1.bind("<Leave>", lambda event: self.change_label_text(""))

        btn2 = tk.Button(frm_buttons, image=self.img_player_vs_computer, command=self.run_pymill_computer)
        btn2.grid(column=1, row=0, padx=4)
        btn2.bind("<Enter>", lambda event: self.change_label_text("Play with the computer"))
        btn2.bind("<Leave>", lambda event: self.change_label_text(""))

        btn3 = tk.Button(frm_buttons, image=self.img_player_vs_player_net, command=None)
        btn3.grid(column=2, row=0, padx=4)
        btn3.bind("<Enter>", lambda event: self.change_label_text("Play with a friend over the network"))
        btn3.bind("<Leave>", lambda event: self.change_label_text(""))

        frm_about_text = tk.Frame(self)
        frm_about_text.grid(row=1)

        self.lbl_about_text = tk.Label(frm_about_text, text="", font="Times, 17")
        self.lbl_about_text.pack()

    def change_label_text(self, text: str):
        self.lbl_about_text.configure(text=text)

    def on_game_exit(self):  # TODO maybe let the user create as many games as he/she wants
        self.in_game = False

    def run_pymill_hotseat(self):
        # if not self.in_game:
        #     thread = threading.Thread(target=pymill_hotseat, daemon=False, args=(self.on_game_exit,))
        #     thread.start()
        #     self.in_game = True
        if not self.in_game:
            PyMillHotseat(tk.Toplevel(self.root), self.on_game_exit)
            self.in_game = True

    def run_pymill_computer(self):
        # if not self.in_game:
        #     thread = threading.Thread(target=pymill_computer, daemon=False, args=(self.on_game_exit,))
        #     thread.start()
        #     self.in_game = True
        if not self.in_game:
            PyMillComputer(tk.Toplevel(self.root), self.on_game_exit)
            self.in_game = True

    def run_pymill_network(self):
        pass


def main():
    print("PyMill " + VERSION, end="\n\n")
    root = tk.Tk()
    PyMillMenu(root)
    root.mainloop()
