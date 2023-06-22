class Checker:
    def __init__(self):
        self.genders = {"m", "M", "f", "F"}
        self.commons = self.load_commons()

    def load_commons(self):
        commons = {}
        with open("assets/codici_catastali.txt", "r") as file:
            for line in file:
                common, code, _ = line.strip().split(",")
                commons[common.lower()] = code
        return commons
    
    def checkGender(self, gender: str):
        return gender in self.genders

    def checkDate(self, date: str):
        try:
            day, month, year = date.split("/")
            day, month, year = int(day), int(month), int(year)

            if month < 1 or month > 12: return False

            if month in [1, 3, 5, 7, 8, 10, 12]:
                max_day = 31
            elif month in [4, 6, 9, 11]:
                max_day = 30
            elif year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                max_day = 29
            else:
                max_day = 28

            if day < 1 or day > max_day: return False

            return True
        except:
            return False

    def checkCommon(self, common: str):
        return common in self.commons
