from tax import TaxCode
from tax.check import Checker
from telebot import types
import telebot
import json

bot_db = json.load(open("assets/bot_db.json"))
db_it = json.load(open("assets/db_it.json"))
bot = telebot.TeleBot(bot_db["token"], parse_mode="HTML")
checker = Checker()

user_dict = {}
class User:
    def __init__(self, surname):
        self.surname = surname
        self.name = None
        self.date = None
        self.gender = None
        self.common = None

@bot.message_handler(commands=["start"])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    fiscal_code_button = types.KeyboardButton(bot_db["name_fiscal_code_button"])
    help_button = types.KeyboardButton(bot_db["name_help_button"])
    markup.row(fiscal_code_button)
    markup.row(help_button)
    bot.send_message(message.chat.id, text=f"Ciao {message.chat.username}, benvenuto/a in {bot_db['name_bot']}!", reply_markup=markup)

@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == bot_db["name_help_button"])
def send_help(message):
    bot.send_message(message.chat.id, text=bot_db["help_text"])

@bot.message_handler(commands=["fiscal_code"])
@bot.message_handler(func=lambda message: message.text == bot_db["name_fiscal_code_button"])
def send_fiscal_code(message):
    surname_msg = bot.send_message(message.chat.id, text="Inserisci il tuo cognome:")
    bot.register_next_step_handler(surname_msg, process_surname_step)

def process_surname_step(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        user = User(surname)
        user_dict[chat_id] = user

        name_msg = bot.send_message(chat_id, "Inserisci il tuo nome:")
        bot.register_next_step_handler(name_msg, process_name_step)
    except Exception as e:
        print(f"Si è verificato un errore...\n{e}")
        bot.send_message(chat_id, "Si è verificato un errore... Riprova più tardi!")


def process_name_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        if user.name == None:
            name = message.text
            user.name = name

        date_msg = bot.send_message(chat_id, "Inserisci la tua data di nascita [gg/mm/aaaa]:")
        bot.register_next_step_handler(date_msg, process_date_step)

    except Exception as e:
        print(f"Si è verificato un errore...\n{e}")
        bot.send_message(chat_id, "Si è verificato un errore... Riprova più tardi!")


def process_date_step(message):
    try:
        if not checker.checkDate(message.text):
            bot.send_message(message.chat.id, "Si è verificato un errore: formato non corretto!")
            process_name_step(message)
        else:
            chat_id = message.chat.id
            date = message.text
            user = user_dict[chat_id]
            user.date = date

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Maschio", "Femmina")
            gender_msg = bot.send_message(chat_id, "Sesso:", reply_markup=markup)
            bot.register_next_step_handler(gender_msg, process_gender_step)
    except Exception as e:
        print(f"Si è verificato un errore...\n{e}")
        bot.send_message(chat_id, "Si è verificato un errore... Riprova più tardi!")

def process_gender_step(message):
    try:
        chat_id = message.chat.id
        gender = message.text[0]
        user = user_dict[chat_id]

        if checker.checkGender(gender):
            user.gender = gender
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        fiscal_code_button = types.KeyboardButton(bot_db["name_fiscal_code_button"])
        help_button = types.KeyboardButton(bot_db["name_help_button"])
        markup.row(fiscal_code_button)
        markup.row(help_button)
        common_msg = bot.send_message(chat_id, "Comune:", reply_markup=markup)
        bot.register_next_step_handler(common_msg, process_common_step)

    except Exception as e:
        print(f"Si è verificato un errore...\n{e}")
        bot.send_message(chat_id, "Si è verificato un errore... Riprova più tardi!")
    
def process_common_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        if user.common is None:
            common = message.text.lower()
            user.common = common
        
        file = open("assets/codici_catastali.txt", "r")
        commons = [line.split(",") for line in file]
        
        found = False
        for item in commons:
            if user.common == item[0].lower():
                found = True
                break
        
        if not found:
            bot.send_message(chat_id, "Si è verificato un errore: comune non trovato!")
            process_gender_step(message)
        else:
            code = TaxCode(surname=user.surname.lower(), name=user.name.lower(), gender=user.gender.lower(), date=user.date, common=user.common.lower())
            bot.send_message(chat_id, f"<b>Informazioni Inserite:</b>\n\nCognome: {user.surname}\nNome: {user.name}\nData di nascita: {user.date}\nSesso: {user.gender}\nComune: {user.common}\n\n<b>Codice Fiscale:</b>")
            bot.send_message(chat_id, f"<b>{code.build()}</b>")
    except Exception as e:
        print(f"Si è verificato un errore...\n{e}")
        bot.send_message(chat_id, "Si è verificato un errore... Riprova più tardi!")


if __name__ == "__main__":
    print("Bot in esecuzione.")
    bot.polling()
