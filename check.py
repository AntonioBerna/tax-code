class Checker:
    def __init__(self):
        self.genders = ["m", "M", "f", "F"]
        self.commons = []  
    
    def checkGender(self, gender: str):
        if gender in self.genders:
            return True
        return False

    def checkDate(self, date: str):
        try:
            day, month, year = date.split("/")
            
            if int(month) in [1, 3, 5, 7, 8, 10, 12]:
                max_month = 31
            elif int(month) in [4, 6, 9, 11]:
                max_month = 30
            elif int(year) % 4 == 0 and int(year) != 0 or int(year) % 400 == 0:
                max_month = 29
            else:
                max_month = 28
            
            if int(month) < 1 or int(month) > 12:
                return False
            elif int(day) < 1 or int(day) > max_month:
                return False
            else:
                return True
        except:
            return False

    def checkCommon(self, common: str):
        file = open("codici_catastali.txt", "r")

        for line in file:
            self.commons.append(line.split(","))
        
        for item in self.commons:
            if common == item[0]:
                return True
        return False