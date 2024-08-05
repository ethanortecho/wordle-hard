import json
import sys
import requests
from tkinter import *
import tkinter.font as tkFont

class Logic:
    def __init__(self, root):
        self.display = Display(self, root)
        self.reset_game()

    def reset_game(self):
        self.dictionary_key = "065c2189-e6a7-47e8-8d2e-67f0733b1b35"  # API key for the dictionary

        self.attempt = 1  # Initialize the number of attempts

        # Lists to track letters' statuses
        self.yellow_letters = []
        self.green_letters = []
        self.incorrect_letters = []

        self.current_guess = []  # Current guess input by the player

        # Keep fetching a valid target word with a definition
        while True:
            self.wordle = self.get_target_word()
            self.definition = self.get_definition(self.wordle)
            print(self.definition)
            if self.definition:
                break

        self.wordle_characters = list(self.wordle)  # Convert the target word to a list of characters

        self.display.setup_gui()  # Set up the GUI elements

    def get_target_word(self):
        while True:
            try:
                word_request = requests.get("https://random-word-api.herokuapp.com/word?length=5")
                word_json = word_request.json()
            except:
                print("Random word API request failed")

            word = (word_json[0]).upper()  # Convert the word to uppercase
            print(word)
            if not word.endswith('S'):
                return word  # Ensure the word does not end with 'S'

    def get_definition(self, word):
        try:
            dictionary_request = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.dictionary_key}")
            dictionary_json = dictionary_request.json()
        except:
            print("Dictionary API request failed")

        if dictionary_json and isinstance(dictionary_json, list) and 'shortdef' in dictionary_json[0]:
            # Extract the first short definition
            return dictionary_json[0]['shortdef'][0]
        else:
            return None  # Return None if no definition found

    def validate_and_submit_guess(self):
        if len(self.current_guess) == 5:
            guess_string = ''.join(self.current_guess)
            if self.get_definition(guess_string):
                self.process_guess()
            else:
                self.display.error_message("Not A Valid Word")
        else:
            self.display.error_message("Not Enough Letters Buckaroo")

    def process_guess(self):
        # Immediately check if the guess matches the Wordle
        if self.current_guess == self.wordle_characters:
            self.display.you_won("WIN")

        for index, letter in enumerate(self.current_guess):
            if letter == self.wordle_characters[index]:
                self.green_letters.append(letter)
                self.display.reveal_letter(index, letter, "GREEN")
            elif letter in self.wordle_characters:
                self.yellow_letters.append(letter)
                self.display.reveal_letter(index, letter, "YELLOW")
            else:
                self.incorrect_letters.append(letter)
                self.display.reveal_letter(index, letter, "GREY")

        self.display.update_keyboard()

        self.attempt += 1
        if self.attempt == 7:
            self.display.you_won("LOSE")
        self.current_guess = []  # Reset current guess for the next attempt

    def add_letter(self, letter):
        if len(self.current_guess) < 5:
            self.current_guess.append(letter)
            self.display.display_current_input()

    def backspace(self):
        if self.current_guess:
            self.current_guess.pop()
            self.display.display_current_input()

class Display:
    def __init__(self, logic, root):
        self.root = root
        self.logic = logic
        root.configure(bg="black")
        self.setup_gui()

    def display_current_input(self):
        for index, letter in enumerate(self.logic.current_guess):
            self.canvas, self.text_item = self.row_mapping[self.logic.attempt][index]
            self.canvas.itemconfig(self.text_item, text=letter)

        # Clear the remaining canvases
        for index in range(len(self.logic.current_guess), len(self.first_row)):
            self.canvas, self.text_item = self.row_mapping[self.logic.attempt][index]
            self.canvas.itemconfig(self.text_item, text="")

    def reveal_letter(self, index, letter, status):  # Reveal letter with color based on its status
        self.canvas, self.text_item = self.row_mapping[self.logic.attempt][index]
        if status == "GREEN":
            self.canvas.config(bg='#00b114')
        elif status == "YELLOW":
            self.canvas.config(bg="#dbb500")
        elif status == "GREY":
            self.canvas.config(bg="#939598")

    def update_keyboard(self):
        for letter in self.logic.incorrect_letters:
            self.button_mapping[letter].config(state=DISABLED)
        for letter in self.logic.yellow_letters:
            self.button_mapping[letter].config(fg="#e2ce3a")
        for letter in self.logic.green_letters:
            self.button_mapping[letter].config(fg="#6aaa64")

    def error_message(self, message):
        self.error_label.config(text=message)
        self.error_label.lift()
        self.error_label.place(relx=.5, rely=.3, anchor="center")
        self.root.after(1000, self.error_label.place_forget)

    def you_won(self, status):  # Display win/lose message
        color = 'black'
        self.congrats_window = Toplevel(root, bg=color)

        spacer = Label(self.congrats_window, padx=33, bg=color)
        spacer.grid(row=3, column=0)
        spacer = Label(self.congrats_window, padx=33, bg=color)
        spacer.grid(row=3, column=4)

        spacer = Label(self.congrats_window, padx=275, bg=color)
        spacer.grid(row=0, column=1, columnspan=3)

        self.status_label = Label(self.congrats_window, text="", bg=color, font=("Raleway", 60), pady=100)
        self.status_label.grid(row=0, column=1, columnspan=3)

        if status == "WIN":
            self.status_label.config(text="YOU WON!")
        if status == "LOSE":
            self.status_label.config(text="YOU LOST")

        self.word_reveal = Label(self.congrats_window, text='the word was...', bg=color, font=("Raleway", 20))
        self.word_reveal.grid(row=1, column=1, columnspan=3)

        self.wordle = Label(self.congrats_window, text=f'{self.logic.wordle}', bg=color, fg='purple', font=("Raleway", 60))
        self.wordle.grid(row=2, column=1, columnspan=3)

        self.definition = Label(self.congrats_window, bg=color, text=f'Definition: {self.logic.definition}', wraplength=500, font=("Raleway", 20))
        self.definition.grid(row=3, column=1, columnspan=3, pady=30)

        self.play_again = Button(self.congrats_window, text="PLAY AGAIN", height=3, width=10, font=("Raleway", 20), command=self.logic.reset_game)
        self.play_again.grid(row=4, column=1, pady=75)

        self.exit_game = Button(self.congrats_window, text="EXIT GAME", height=3, width=10, font=("Raleway", 20), command=sys.exit)
        self.exit_game.grid(row=4, column=3, pady=75)

    def setup_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the root window

        self.first_row = []
        self.second_row = []
        self.third_row = []
        self.fourth_row = []
        self.fifth_row = []
        self.sixth_row = []
        self.row_mapping = {1: self.first_row, 2: self.second_row, 3: self.third_row, 4: self.fourth_row, 5: self.fifth_row, 6: self.sixth_row}

        square_size = 60
        for column in range(2, 7):
            for row, row_list in enumerate([self.first_row, self.second_row, self.third_row, self.fourth_row, self.fifth_row, self.sixth_row], start=2):
                self.canvas = Canvas(root, width=square_size, height=square_size, bg="black", highlightthickness=1, highlightbackground="grey")
                self.canvas.grid(row=row, column=column, padx=3, pady=3, columnspan=2)
                self.text_item = self.canvas.create_text(square_size / 2, square_size / 2, text="", font=("Helvetica", 20, "bold"), fill="white", anchor="center")
                row_list.append((self.canvas, self.text_item))

        # Miscellaneous GUI elements
        self.error_label = Label(root, text='', padx=15, pady=15, bg='red')

        title = Label(root, text="ETHAN'S WORDLE", font=("Raleway", "50"), bg="black")
        subtitle = Label(root, text="(HARD EDITION)", font=("Raleway", 30), bg="black", fg='orange')
        subtitle.grid(row=1, column=0, columnspan=10, pady=20)

        title.grid(row=0, column=0, columnspan=10, pady=0)

        spacer = Label(root, pady=15, bg="black")
        spacer.grid(row=8, column=0, columnspan=12)
        spacer = Label(root, pady=15, bg="black")
        spacer.grid(row=12, column=0, columnspan=12)

        font = tkFont.Font(family="Raleway", size=30)

        # First row of letters
        self.Q = Button(root, text='Q', font=font, height=2, width=2, command=lambda: self.logic.add_letter("Q"))
        self.W = Button(root, text='W', font=font, height=2, width=2, command=lambda: self.logic.add_letter("W"))
        self.E = Button(root, text='E', font=font, height=2, width=2, command=lambda: self.logic.add_letter("E"))
        self.R = Button(root, text='R', font=font, height=2, width=2, command=lambda: self.logic.add_letter("R"))
        self.T = Button(root, text='T', font=font, height=2, width=2, command=lambda: self.logic.add_letter("T"))
        self.Y = Button(root, text='Y', font=font, height=2, width=2, command=lambda: self.logic.add_letter("Y"))
        self.U = Button(root, text='U', font=font, height=2, width=2, command=lambda: self.logic.add_letter("U"))
        self.I = Button(root, text='I', font=font, height=2, width=2, command=lambda: self.logic.add_letter("I"))
        self.O = Button(root, text='O', font=font, height=2, width=2, command=lambda: self.logic.add_letter("O"))
        self.P = Button(root, text='P', font=font, height=2, width=2, command=lambda: self.logic.add_letter("P"))

        # Second row of letters
        self.A = Button(root, text='A', font=font, height=2, width=2, command=lambda: self.logic.add_letter("A"))
        self.S = Button(root, text='S', font=font, height=2, width=2, command=lambda: self.logic.add_letter("S"))
        self.D = Button(root, text='D', font=font, height=2, width=2, command=lambda: self.logic.add_letter("D"))
        self.F = Button(root, text='F', font=font, height=2, width=2, command=lambda: self.logic.add_letter("F"))
        self.G = Button(root, text='G', font=font, height=2, width=2, command=lambda: self.logic.add_letter("G"))
        self.H = Button(root, text='H', font=font, height=2, width=2, command=lambda: self.logic.add_letter("H"))
        self.J = Button(root, text='J', font=font, height=2, width=2, command=lambda: self.logic.add_letter("J"))
        self.K = Button(root, text='K', font=font, height=2, width=2, command=lambda: self.logic.add_letter("K"))
        self.L = Button(root, text='L', font=font, height=2, width=2, command=lambda: self.logic.add_letter("L"))

        # Third row of letters
        self.Z = Button(root, text='Z', font=font, height=2, width=2, command=lambda: self.logic.add_letter("Z"))
        self.X = Button(root, text='X', font=font, height=2, width=2, command=lambda: self.logic.add_letter("X"))
        self.C = Button(root, text='C', font=font, height=2, width=2, command=lambda: self.logic.add_letter("C"))
        self.V = Button(root, text='V', font=font, height=2, width=2, command=lambda: self.logic.add_letter("V"))
        self.B = Button(root, text='B', font=font, height=2, width=2, command=lambda: self.logic.add_letter("B"))
        self.N = Button(root, text='N', font=font, height=2, width=2, command=lambda: self.logic.add_letter("N"))
        self.M = Button(root, text='M', font=font, height=2, width=2, command=lambda: self.logic.add_letter("M"))
        self.enter_button = Button(root, text='ENTER', font=font, height=2, width=5, command=self.logic.validate_and_submit_guess)
        self.backspace_button = Button(root, text="DELETE", font=font, height=2, width=5, command=self.logic.backspace)

        # First row of letters
        self.Q.grid(row=10, column=0)
        self.W.grid(row=10, column=1)
        self.E.grid(row=10, column=2)
        self.R.grid(row=10, column=3)
        self.T.grid(row=10, column=4)
        self.Y.grid(row=10, column=5)
        self.U.grid(row=10, column=6)
        self.I.grid(row=10, column=7)
        self.O.grid(row=10, column=8)
        self.P.grid(row=10, column=9)

        # Second row of letters
        self.A.grid(row=11, column=0, columnspan=2)
        self.S.grid(row=11, column=1, columnspan=2)
        self.D.grid(row=11, column=2, columnspan=2)
        self.F.grid(row=11, column=3, columnspan=2)
        self.G.grid(row=11, column=4, columnspan=2)
        self.H.grid(row=11, column=5, columnspan=2)
        self.J.grid(row=11, column=6, columnspan=2)
        self.K.grid(row=11, column=7, columnspan=2)
        self.L.grid(row=11, column=8, columnspan=2)

        # Third row of letters
        self.Z.grid(row=12, column=1, columnspan=2)
        self.X.grid(row=12, column=2, columnspan=2)
        self.C.grid(row=12, column=3, columnspan=2)
        self.V.grid(row=12, column=4, columnspan=2)
        self.B.grid(row=12, column=5, columnspan=2)
        self.N.grid(row=12, column=6, columnspan=2)
        self.M.grid(row=12, column=7, columnspan=2)

        self.enter_button.grid(row=14, column=1, columnspan=4)
        self.backspace_button.grid(row=14, column=6, columnspan=2)

        self.button_mapping = {
            "A": self.A,
            "B": self.B,
            "C": self.C,
            "D": self.D,
            "E": self.E,
            "F": self.F,
            "G": self.G,
            "H": self.H,
            "I": self.I,
            "J": self.J,
            "K": self.K,
            "L": self.L,
            "M": self.M,
            "N": self.N,
            "O": self.O,
            "P": self.P,
            "Q": self.Q,
            "R": self.R,
            "S": self.S,
            "T": self.T,
            "U": self.U,
            "V": self.V,
            "W": self.W,
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z
        }

if __name__ == "__main__":
    root = Tk()
    app = Logic(root)
    root.mainloop()
    root.configure(bg="black")
















































