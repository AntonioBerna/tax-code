import tkinter as tk
from tkinter import messagebox
import webbrowser

from tax import TaxCode
from tax.check import Checker

class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Help - by Clever Code")
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


class TaxCodeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tax Code Calculator - by CleverCode")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Tax Code Calculator", font=("Cascadia Code", "15"))
        self.label.grid(column=0, row=0, padx=10, pady=10)

        self.help_button = tk.Button(self, text="Help", font=("Cascadia Code", "15"), command=self.show_help_window)
        self.help_button.grid(column=1, row=0, padx=10, pady=10, sticky="EW")

        self.surname_label = tk.Label(self, text="Surname:", font=("Cascadia Code", "15"))
        self.surname_label.grid(column=0, row=1, padx=10, sticky="W")
        self.surname_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.surname_entry.grid(column=1, row=1, padx=10, sticky="E")

        self.name_label = tk.Label(self, text="Name:", font=("Cascadia Code", "15"))
        self.name_label.grid(column=0, row=2, padx=10, sticky="W")
        self.name_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.name_entry.grid(column=1, row=2, padx=10, sticky="E")

        self.date_label = tk.Label(self, text="Date of birth [dd/mm/yyyy]:", font=("Cascadia Code", "15"))
        self.date_label.grid(column=0, row=3, padx=10, sticky="W")
        self.date_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.date_entry.grid(column=1, row=3, padx=10, sticky="E")

        self.gender_label = tk.Label(self, text="Sex:", font=("Cascadia Code", "15"))
        self.gender_label.grid(column=0, row=4, padx=10, sticky="W")
        self.gender_var = tk.StringVar()
        self.gender_var.set(-1)
        self.male = tk.Radiobutton(self, text="Male", variable=self.gender_var, value="m")
        self.male.grid(column=1, row=4, padx=10, sticky="W")
        self.female = tk.Radiobutton(self, text="Female", variable=self.gender_var, value="f")
        self.female.grid(column=1, row=4, padx=10, sticky="E")

        self.common_label = tk.Label(self, text="Common:", font=("Cascadia Code", "15"))
        self.common_label.grid(column=0, row=5, padx=10, sticky="W")
        self.common_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"))
        self.common_entry.grid(column=1, row=5, padx=10, sticky="E")

        self.tax_code_label = tk.Label(self, text="Tax Code:", font=("Cascadia Code", "15"))
        self.tax_code_label.grid(column=0, row=6, padx=10, sticky="W")
        self.tax_code_entry = tk.Entry(self, justify="center", font=("Cascadia Code", "15"), state="readonly")
        self.tax_code_entry.grid(column=1, row=6, padx=10, sticky="E")

        self.reset_button = tk.Button(self, text="Reset", font=("Cascadia Code", "15"), command=self.reset_fields)
        self.reset_button.grid(column=0, row=7, padx=10, pady=10, sticky="EW")

        self.start_button = tk.Button(self, text="Calculate", font=("Cascadia Code", "15"), command=self.generate_tax_code)
        self.start_button.grid(column=1, row=7, padx=10, pady=10, sticky="EW")

    def show_help_window(self):
        help_window = HelpWindow(self)
        help_window.grab_set()

    def reset_fields(self):
        self.tax_code_entry.config(state="normal")
        self.surname_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.gender_var.set(-1)
        self.date_entry.delete(0, tk.END)
        self.common_entry.delete(0, tk.END)
        self.tax_code_entry.delete(0, tk.END)
        self.tax_code_entry.config(state="readonly")

    def generate_tax_code(self):
        self.tax_code_entry.config(state="normal")
        self.tax_code_entry.delete(0, tk.END)
        surname = self.surname_entry.get()
        name = self.name_entry.get()
        gender = self.gender_var.get()
        birth_date = self.date_entry.get()
        common = self.common_entry.get()

        if surname and name and gender and birth_date and common:
            checker = Checker()
            if checker.checkText(surname) and checker.checkText(name) and checker.checkGender(gender) and checker.checkDate(birth_date) and checker.checkCommon(common):
                code = TaxCode(surname.lower(), name.lower(), gender, birth_date, common.lower())
                self.tax_code_entry.insert(0, code.build())
                self.tax_code_entry.config(state="readonly")
            else:
                messagebox.showerror("An error occurred", "Invalid Values Entered!")
        else:
            messagebox.showerror("An error occurred", "Invalid Values Entered!")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = TaxCodeWindow()
    app.run()
