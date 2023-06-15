from fc import FiscalCode
from fc.check import Checker
import subprocess
import platform

class UserInterface(Checker):
    def __init__(self):
        super().__init__()
        self.clear_screen()
        print("Calcolatore Codice Fiscale - by CleverCode")

    def clear_screen(self):
        system = platform.system()
        if system == "Windows":
            subprocess.call("cls", shell=True)
        else:
            subprocess.call("clear", shell=True)

    def get_personal_data(self):
        surname = input("\nCognome: ").lower()
        name = input("Nome: ").lower()
        gender = self.get_gender()
        birth_date = self.get_birth_date()
        common = self.get_common()
        return surname, name, gender, birth_date, common

    def get_gender(self):
        while True:
            gender = input("Sesso [m/f]: ").lower()
            if self.checkGender(gender):
                return gender

    def get_birth_date(self):
        while True:
            birth_date = input("Data di nascita [gg/mm/aaaa]: ")
            if self.checkDate(birth_date):
                return birth_date

    def get_common(self):
        while True:
            common = input("Comune: ").lower()
            if self.checkCommon(common):
                return common

    def start(self):
        surname, name, gender, birth_date, common = self.get_personal_data()
        return FiscalCode(surname, name, gender, birth_date, common).build()

if __name__ == "__main__":
    try:
        app = UserInterface()
        print(f"\nCodice Fiscale: {app.start()}")
    except KeyboardInterrupt:
        print("\nBye.")
