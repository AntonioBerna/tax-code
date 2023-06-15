from fc import FiscalCode
from fc.check import Checker
import tkinter as tk
from tkinter import messagebox
import webbrowser

class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Informazioni Sviluppatore")
        self.resizable(False, False)

        self.github_button = tk.Button(self, text="Github", font=("Cascadia Code", "15"), command=self.get_github)
        self.github_button.grid(column=0, row=0, padx=10, pady=10)
        self.youtube_button = tk.Button(self, text="YouTube", font=("Cascadia Code", "15"), command=self.get_youtube)
        self.youtube_button.grid(column=0, row=1, padx=10, pady=10)
        self.instagram_button = tk.Button(self, text="Instagram", font=("Cascadia Code", "15"), command=self.get_instagram)
        self.instagram_button.grid(column=0, row=2, padx=10, pady=10)
        self.telegram_button = tk.Button(self, text="Telegram: @CleverCode", font=("Cascadia Code", "15"))
        self.telegram_button.grid(column=0, row=3, padx=10, pady=10)

    def get_github(self):
        webbrowser.open("https://www.github.com/AntonioBerna")

    def get_youtube(self):
        webbrowser.open("https://www.youtube.com/c/CleverCode")

    def get_instagram(self):
        webbrowser.open("https://www.instagram.com/clever_code/")


class FiscalCodeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Codice Fiscale - by Clever Code")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="CALCOLO CODICE FISCALE", font=("Cascadia Code", "15"))
        self.label.grid(column=0, row=0, padx=10, pady=10)

        self.help_button = tk.Button(self, text="Aiuto", font=("Cascadia Code", "15"), command=self.show_help_window)
        self.help_button.grid(column=1, row=0, padx=10, pady=10, sticky="EW")

        self.surname_label = tk.Label(self, text="Cognome:", font=("Cascadia Code", "15"))
        self.surname_label.grid(column=0, row=1, padx=10, sticky="W")
        self.surname_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.surname_entry.grid(column=1, row=1, padx=10, sticky="E")

        self.name_label = tk.Label(self, text="Nome:", font=("Cascadia Code", "15"))
        self.name_label.grid(column=0, row=2, padx=10, sticky="W")
        self.name_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.name_entry.grid(column=1, row=2, padx=10, sticky="E")

        self.date_label = tk.Label(self, text="Data di nascita:", font=("Cascadia Code", "15"))
        self.date_label.grid(column=0, row=3, padx=10, sticky="W")
        self.date_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.date_entry.grid(column=1, row=3, padx=10, sticky="E")

        self.gender_label = tk.Label(self, text="Sesso:", font=("Cascadia Code", "15"))
        self.gender_label.grid(column=0, row=4, padx=10, sticky="W")
        self.gender_var = tk.StringVar()
        self.gender_var.set(-1)
        self.male = tk.Radiobutton(self, text="Maschile", variable=self.gender_var, value="m")
        self.male.grid(column=1, row=4, padx=10, sticky="W")
        self.female = tk.Radiobutton(self, text="Femminile", variable=self.gender_var, value="f")
        self.female.grid(column=1, row=4, padx=10, sticky="E")

        self.common_label = tk.Label(self, text="Comune:", font=("Cascadia Code", "15"))
        self.common_label.grid(column=0, row=5, padx=10, sticky="W")
        self.common_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.common_entry.grid(column=1, row=5, padx=10, sticky="E")

        self.fiscal_code_label = tk.Label(self, text="Codice Fiscale:", font=("Cascadia Code", "15"))
        self.fiscal_code_label.grid(column=0, row=6, padx=10, sticky="W")
        self.fiscal_code_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.fiscal_code_entry.grid(column=1, row=6, padx=10, sticky="E")

        self.reset_button = tk.Button(self, text="Reimposta", font=("Cascadia Code", "15"), command=self.reset_fields)
        self.reset_button.grid(column=0, row=7, padx=10, pady=10, sticky="EW")

        self.start_button = tk.Button(self, text="Calcola", font=("Cascadia Code", "15"), command=self.generate_fiscal_code)
        self.start_button.grid(column=1, row=7, padx=10, pady=10, sticky="EW")

    def show_help_window(self):
        help_window = HelpWindow(self)
        help_window.grab_set()

    def reset_fields(self):
        self.surname_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.gender_var.set(-1)
        self.date_entry.delete(0, tk.END)
        self.common_entry.delete(0, tk.END)
        self.fiscal_code_entry.delete(0, tk.END)

    def generate_fiscal_code(self):
        self.fiscal_code_entry.delete(0, tk.END)
        surname = self.surname_entry.get()
        name = self.name_entry.get()
        gender = self.gender_var.get()
        birth_date = self.date_entry.get()
        common = self.common_entry.get()

        if surname and name and gender and birth_date and common:
            checker = Checker()
            if checker.checkGender(gender) and checker.checkDate(birth_date) and checker.checkCommon(common.lower()):
                fc = FiscalCode(surname.lower(), name.lower(), gender, birth_date, common.lower())
                self.fiscal_code_entry.insert(0, fc.build())
            else:
                messagebox.showerror("Si è verificato un errore", "Valori Inseriti Non Validi!")
        else:
            messagebox.showerror("Si è verificato un errore", "Valori Inseriti Non Sufficienti!")

if __name__ == "__main__":
    window = FiscalCodeWindow()
    window.mainloop()
