import subprocess
import platform
import signal

from tax import TaxCode
from tax.check import Checker

class UserInterface(Checker):
    def __init__(self) -> None:
        super().__init__()
        self.clear_screen()
        print("Tax Code Calculator - by CleverCode\n")

    def clear_screen(self) -> None:
        system = platform.system()
        if system == "Windows":
            subprocess.call("cls", shell=True)
        else:
            subprocess.call("clear", shell=True)

    def getPersonalData(self) -> tuple:
        surname = self.getText("Surname: ")
        name = self.getText("Name: ")
        gender = self.getGender("Sex [m/f]: ")
        birth_date = self.getBirthDate("Date of birth [dd/mm/yyyy]: ")
        common = self.getCommon("Common: ")
        return surname, name, gender, birth_date, common

    def get(self, prompt: str, validation_function) -> str:
        while True:
            userInput = input(prompt).lower()
            if validation_function(userInput):
                return userInput

    def getText(self, prompt: str) -> str:
        return self.get(prompt, self.checkText)

    def getGender(self, prompt: str) -> str:
        return self.get(prompt, self.checkGender)
    
    def getBirthDate(self, prompt: str) -> str:
        return self.get(prompt, self.checkDate)
    
    def getCommon(self, prompt: str) -> str:
        return self.get(prompt, self.checkCommon)

    def run(self) -> str:
        surname, name, gender, birth_date, common = self.getPersonalData()
        return TaxCode(surname, name, gender, birth_date, common).build()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: print("\nBye.\n") or exit(0))
    app = UserInterface()
    print(f"\nTax Code: {app.run()}\n")
