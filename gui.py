from fiscal_code import FiscalCode
from tkinter import messagebox
from check import Checker
import tkinter as tk
import webbrowser


class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Informazioni Sviluppatore")
        self.resizable(False, False)

        self.github_button = tk.Button(self, text="Github", font=("Cascadia Code", "15"), command=self.getGithub)
        self.github_button.grid(column=0, row=0, padx=10, pady=10)
        self.youtube_button = tk.Button(self, text="YouTube", font=("Cascadia Code", "15") , command=self.getYoutube)
        self.youtube_button.grid(column=0, row=1, padx=10, pady=10)
        self.instagram_button = tk.Button(self, text="Instagram", font=("Cascadia Code", "15"), command=self.getInstagram)
        self.instagram_button.grid(column=0, row=2, padx=10, pady=10)
        self.telegram_button = tk.Button(self, text="Telegram: @CleverCode", font=("Cascadia Code", "15"))
        self.telegram_button.grid(column=0, row=3, padx=10, pady=10)
        
    def getGithub(self):
        webbrowser.open("https://www.github.com/AntonioBerna")
    
    def getYoutube(self):
        webbrowser.open("https://www.youtube.com/c/CleverCode")
    
    def getInstagram(self):
        webbrowser.open("https://www.instagram.com/clever_code/")


class FiscalCodeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Codice Fiscale - by Clever Code")
        # self.geometry("500x500")
        self.resizable(False, False)
        self.frame = tk.Frame()
        self.frame.pack()

        self.label = tk.Label(self.frame, text="CALCOLO CODICE FISCALE", font=("Cascadia Code", "15"))
        self.label.grid(column=0, row=0, padx=10, pady=10)
        self.help_button = tk.Button(self.frame, text="Aiuto", font=("Cascadia Code", "15"), command=self.helpWindow)
        self.help_button.grid(column=1, row=0, padx=10, pady=10, sticky="EW")        
        self.surname_label = tk.Label(self.frame, text="Cognome:", font=("Cascadia Code", "15"))
        self.surname_label.grid(column=0, row=1, padx=10, sticky="W")
        self.surname_entry = tk.Entry(self.frame, justify="center", font=("Cascadia Code", "15"))
        self.surname_entry.grid(column=1, row=1, padx=10, sticky="E")
        self.name_label = tk.Label(self.frame, text="Nome:", font=("Cascadia Code", "15"))
        self.name_label.grid(column=0, row=2, padx=10, sticky="W")
        self.name_entry = tk.Entry(self.frame, justify="center", font=("Cascadia Code", "15"))
        self.name_entry.grid(column=1, row=2, padx=10, sticky="E")
        self.date_label = tk.Label(self.frame, text="Data di nascita:", font=("Cascadia Code", "15"))
        self.date_label.grid(column=0, row=3, padx=10, sticky="W")
        self.date_entry = tk.Entry(self.frame, justify="center", font=("Cascadia Code", "15"))
        self.date_entry.grid(column=1, row=3, padx=10, sticky="E")
        self.gender_label = tk.Label(self.frame, text="Sesso:", font=("Cascadia Code", "15"))
        self.gender_label.grid(column=0, row=4, padx=10, sticky="W")
        self.radio_value = tk.IntVar()
        self.radio_value.set(-1)
        self.male = tk.Radiobutton(self.frame, text="Maschile", variable=self.radio_value, value=0)
        self.male.grid(column=1, row=4, padx=10, sticky="W")
        self.female = tk.Radiobutton(self.frame, text="Femminile", variable=self.radio_value, value=1)
        self.female.grid(column=1, row=4, padx=10, sticky="E")
        self.common_label = tk.Label(self.frame, text="Comune:", font=("Cascadia Code", "15"))
        self.common_label.grid(column=0, row=5, padx=10, sticky="W")
        self.common_entry = tk.Entry(self.frame, justify="center", font=("Cascadia Code", "15"))
        self.common_entry.grid(column=1, row=5, padx=10, sticky="E")
        self.fiscal_code_label = tk.Label(self.frame, text="Codice Fiscale:", font=("Cascadia Code", "15"))
        self.fiscal_code_label.grid(column=0, row=6, padx=10, sticky="W")
        self.fiscal_code_entry = tk.Entry(self.frame, justify="center", font=("Cascadia Code", "15"))
        self.fiscal_code_entry.grid(column=1, row=6, padx=10, sticky="E")
        self.reset_button = tk.Button(self.frame, text="Reimposta", font=("Cascadia Code", "15"), command=self.resetWindow)
        self.reset_button.grid(column=0, row=7, padx=10, pady=10, sticky="EW")
        self.start_button = tk.Button(self.frame, text="Calcola", font=("Cascadia Code", "15"), command=self.fcGenerator)
        self.start_button.grid(column=1, row=7, padx=10, pady=10, sticky="EW")

    def helpWindow(self):
        help_window = HelpWindow(self)
        help_window.grab_set()

    def resetWindow(self):
        self.surname_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.radio_value.set(-1)
        self.date_entry.delete(0, tk.END)
        self.common_entry.delete(0, tk.END)
        self.fiscal_code_entry.delete(0, tk.END)

    def __checkGender(self):
        if self.radio_value.get() == 0:
            self.gender = "m"
        else:
            self.gender = "f"
        return self.gender

    def fcGenerator(self):
        self.fiscal_code_entry.delete(0, tk.END)
        
        self.gender = self.__checkGender()
        checker = Checker()
        if self.surname_entry.get() != "" and self.name_entry.get() != "" and self.date_entry.get() != "" and self.common_entry.get() != "":
            if checker.checkGender(self.gender) and checker.checkDate(self.date_entry.get()) and checker.checkCommon(self.common_entry.get().lower()):
                fc = FiscalCode(
                    self.surname_entry.get().lower(),
                    self.name_entry.get().lower(),
                    self.gender,
                    self.date_entry.get(),
                    self.common_entry.get().lower()
                )
                self.fiscal_code_entry.insert(0, fc.makeFiscalCode())
            else:
                messagebox.showerror("Si è verificato un errore", "Valori Inseriti Non Validi!")
        else:
            messagebox.showerror("Si è verificato un errore", "Valori Inseriti Non Sufficienti!")


if __name__ == "__main__":
    window = FiscalCodeWindow()
    window.mainloop()
    