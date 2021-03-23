import telebot as tb
from telebot import types
import pandas as pd
import csv
#организатор - название катки, установка дедлайна, сколько человек зарегалось, нужно ли учитывать степень знакомства
#участник - запросить имя и название катки, проверить отсутствие имени среди уже взятых, после дедлайна прислать киборд со списком взятых имён и кнопкой завершения, когда все опросы собраны или орг принудительно начал игру прислать имя жертвы

token = '1555845859:AAFT12GCr7l-vK8S67KGtqUAyOVM7_hl7Vc'
bot = tb.TeleBot(token, parse_mode=None)
chat_id = m.chat.id

#добавить инфу о механизме работы и вводный месседж
@bot.message_handler(commands=['start'])
def command_start(m):
    chat_id = m.chat.id
    with open('ubivets.csv', 'a+', encoding="utf-8") as f:
        table = DictReader(f)
        for row in table:
            if row[id] == chat_id:
                keyb_start = types.ReplyKeyboardMarkup(row_width=1)
                item_start_yes = types.KeyboardButton('Начать новую игру')
                item_start_no = types.KeyboardButton('Продолжить текущую игру')
                keyb_start.add(item_start_yes, item_start_no)
                bot.send_message(chat_id, "Ты уже участвуешь в какой-то игре. Если начать новую игру, данные о начатой будут стёрты.", reply_markup=keyb_start)
                break
        else:
            func_start(chat_id)

def restart(m):
    chat_id = m.chat.id
    keyb_start = types.ReplyKeyboardRemove()
    if m.text == 'Начать новую игру':
        #ПЕРЕЗАПИСАТЬ СТАТУС В ФАЙЛ
        func_start(m)
    if m.text == 'Продолжить текущую игру':
        bot.send_message(chat_id, 'Ок')

def func_start(m):
    keyb_first = types.ReplyKeyboardMarkup()
    item_org = types.KeyboardButton('Организатор')
    item_part = types.KeyboardButton('Участник')
    keyb_first.row(item_org, item_part)
    bot.send_message(chat_id, "TODO WELCOMEMESSAGE")
    bot.send_message(chat_id, "Выбери свою роль:", reply_markup=keyb_first)


def part_start(chat_id):
    keyb_first = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, 'Введи кодовое слово игры, в которой ты участвуешь', reply_markup=keyb_first)
    @bot.message_handler(content_types=['text'])
    def part_gamenametaker(m):
        chat_id = m.chat.id
        if m.text not in game_names:
            bot.send_message(chat_id, "Такой текущей партии нет")
        else:
            bot.send_message(chat_id, "Введи своё имя и фамилию")
            #ЗАПИСАТЬ В ФАЙЛ regd

def part_name(m):
    chat_id = m.chat.id
    #ЗАПИСАТЬ ИМЯ В ФАЙЛ
    #ЗАПИСАТЬ REGD В ФАЙЛ
    bot.send_message(chat_id, "Ура, регистрация пройдена! Жди начала опроса.")

def part_quest(chat_id):
    #ЗАПИСАТЬ В ФАЙЛ СТАТУС quest
    keyb_q = types.ReplyKeyboardMarkup()
    familiar = []
    for name in names:
        n = types.KeyboardButton(name)
        keyb_q.add(n)
    n = types.KeyboardButton('Готово!')
    keyb_q.add(n)
    bot.send_message(chat_id, 'Выбери в этом списке тех людей, с которыми ты знаком, то есть узнаешь их, если увидишь. Нажми "Готово!", когда закончишь.', reply_markup=keyb_q)
@bot.message_handler(func=lambda message: message.text in names)
def namegetter(m, familiar):
    familiar.append(m.text)
    return familiar
@bot.message_handler(func=lambda message: message.text == ''Готово!'):
def part_endquest(chat_id):
    keyb_q = types.ReplyKeyboardRemove()
    #ЗАПИСАТЬ СПИСОК ЗНАКОМЫХ В ФАЙЛ В КАКОМ ТАМ НАДО ФОРМАТЕ
    #ЗАПИСАТЬ В ФАЙЛ СТАТУС questd и 0 в счётчик жертв
    bot.send_message(chat_id, "Регистрация завершена, осталось дождаться начала игры!")

def part_game(m):
    if m.text  == 'меня нашли':
        #найти в файле строку убийцы и по его id выслать имя новой жертвы и добавить +1 в счётчик
        #записать в файл статус x
        bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")

bot.polling()
