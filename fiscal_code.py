import json


class FiscalCode:
    def __init__(self, surname: str, name: str, gender: str, date: str, common: str):
        self.surname_ = surname
        self.name_ = name
        self.gender_ = gender
        self.date_ = date
        self.common_ = common

        table = json.load(open("table.json")) # http://it.wikipedia.org/wiki/Codice_fiscale

        self.vowels = []
        self.consonants = []
        self.table_month = table["month"]
        self.table_even = table["even"]
        self.table_odd = table["odd"]
        self.table_rest = table["rest"]
        self.commons = []
        self.name = ""
        self.surname = ""
        self.date = ""
        self.day = ""
        self.month = ""
        self.year = ""
        self.gender = ""
        self.cadastral_code = ""
        self.incomplete_fiscal_code = ""
        self.even_digits = []
        self.odd_digits = []
        self.control_letter = ""
        self.fiscal_code = ""
    
    def __makeSeparation(self, obj: str):
        for char in obj:
            if char in "aeiou":
                self.vowels.append(char)
            else:
                self.consonants.append(char)
    
    def __makeCorrectString(self, obj: str):
        special_chars = ["'", " "]
        index_list = []
        
        for i in range(0, len(obj)):
            if obj[i] in special_chars:
                index_list.append(i)

        if index_list != []:
            s = ""
            for i in range(0, len(obj)):
                if i not in index_list:
                    s += obj[i]
            return s
        return obj
    
    def __makeSurname(self, surname: str):
        self.__makeSeparation(surname)

        if len(self.consonants) >= 3:
            for i in range(0, 3):
                self.surname += self.consonants[i]
        elif len(self.consonants) == 2 and len(self.vowels) >= 1:
            for i in range(0, len(self.consonants)):
                self.surname += self.consonants[i]
            self.surname += self.vowels[0]
        elif len(self.consonants) == 1 and len(self.vowels) >= 2:
            self.surname += self.consonants[0]
            for i in range(0, 2):
                self.surname += self.vowels[i]
        else:
            self.surname = self.consonants[0] + self.vowels[0] + "x"
        
        del self.consonants[:]
        del self.vowels[:]

    def __makeName(self, name: str):
        self.__makeSeparation(name)

        if len(self.consonants) > 3:
            for i in range(0, 4):
                if i == 1: continue
                self.name += self.consonants[i]
        elif len(self.consonants) >= 3:
            for i in range(0, 3):
                self.name += self.consonants[i]
        elif len(self.consonants) == 2 and len(self.vowels) >= 1:
            for i in range(0, len(self.consonants)):
                self.name += self.consonants[i]
            self.name += self.vowels[0]
        elif len(self.consonants) == 1 and len(self.vowels) >= 2:
            self.name += self.consonants[0]
            for i in range(0, 2):
                self.name += self.vowels[i]
        else:
            self.name = self.consonants[0] + self.vowels[0] + "x"
        
        del self.consonants[:]
        del self.vowels[:]

    def __setGender(self, gender: str):
        if gender == "m":
            self.gender = "m"
        else:
            self.gender = "f"

    def __makeDate(self, date: str):
        self.date = date.split("/")
        self.year = self.date[2][-2:]
        self.month = self.table_month[int(self.date[1]) - 1]
        
        if self.gender == "m":
            if int(self.date[0]) > 9:
                self.day = str(self.date[0])
            else:
                self.day = "0" + self.date[0]
        else:
            self.day = str(40 + int(self.date[0]))
    
    def __makeCadastralCode(self, common: str):
        file = open("codici_catastali.txt", "r")

        for line in file:
            self.commons.append(line.split(","))
        
        for item in self.commons:
            if common == item[0]:
                self.cadastral_code = item[1]
        
        del self.commons[:]
    
    def __makeControlLetter(self):
        self.incomplete_fiscal_code = self.surname + self.name + self.year + self.month + self.day + self.cadastral_code
        even = self.incomplete_fiscal_code[1::2]
        odd = self.incomplete_fiscal_code[::2]

        for item in even:
            self.even_digits.append(int(self.table_even[item]))

        for item in odd:
            self.odd_digits.append(int(self.table_odd[item]))

        even_sum = 0
        for item in self.even_digits:
            even_sum += item

        odd_sum = 0
        for item in self.odd_digits:
            odd_sum += item
        
        self.control_letter = self.table_rest[str((even_sum + odd_sum) % 26)]
        self.fiscal_code = (self.incomplete_fiscal_code + self.control_letter).upper()

        del self.even_digits[:]
        del self.odd_digits[:]
    
    def saveData(self):
        with open("db_it.json") as file:
            objects = json.load(file)

        person = {
            "surname": self.surname_,
            "name": self.name_,
            "gender": self.gender_,
            "date": self.date_,
            "common": self.common_,
            "fiscal_code": self.fiscal_code
        }

        if person not in objects:
            objects.append(person)

        with open("db_it.json", "w") as json_file:
            json.dump(objects, json_file, indent=4, separators=(",", ": "))

    def makeFiscalCode(self):
        self.__makeSurname(self.__makeCorrectString(self.surname_))
        self.__makeName(self.__makeCorrectString(self.name_))
        self.__setGender(self.gender_)
        self.__makeDate(self.date_)
        self.__makeCadastralCode(self.common_)
        self.__makeControlLetter()

        self.saveData()

        return self.fiscal_code