from fiscal_code import FiscalCode
from check import Checker
import os


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Calcolatore Codice Fiscale - by CleverCode")

    surname = input("\nCognome: ").lower()
    name = input("Nome: ").lower()

    checker = Checker()

    flag = True
    while flag:
        gender = input("Sesso [m/f]: ").lower()
        if checker.checkGender(gender):
            flag = False
        else:
            print("Si è verificato un errore, riprova!\n")

    flag = True
    while flag:
        date = input("Data di nascita [gg/mm/aaaa]: ")
        if checker.checkDate(date):
            flag = False
        else:
            print("Si è verificato un errore, riprova!\n")

    flag = True
    while flag:
        common = input("Comune: ").lower()
        if checker.checkCommon(common):
            flag = False
        else:
            print("Si è verificato un errore, riprova!\n")

    fc = FiscalCode(surname, name, gender, date, common)
    print(f"\nCodice Fiscale: {fc.makeFiscalCode()}")
    print("\nBye.")