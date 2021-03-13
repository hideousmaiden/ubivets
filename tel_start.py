import telebot as tb
from telebot import types
import re
#организатор - название катки, установка дедлайна, сколько человек зарегалось, нужно ли учитывать степень знакомства
#участник - запросить имя и название катки, проверить отсутствие имени среди уже взятых, после дедлайна прислать киборд со списком взятых имён и кнопкой завершения, когда все опросы собраны или орг принудительно начал игру прислать имя жертвы

token = '1555845859:AAFT12GCr7l-vK8S67KGtqUAyOVM7_hl7Vc'
bot = tb.TeleBot(token, parse_mode=None)
names = []         #как сохранять уже введённые имена чтобы они не слетали каждый раз когда бот перезапускается
game_names = []        # разветвление по каткам надо тоже сделать
#добавить инфу о механизме работы и вводный месседж

@bot.message_handler(commands=['start'])
def command_start(m):
    chat_id = m.chat.id
    keyb_first = types.ReplyKeyboardMarkup()
    item_org = types.KeyboardButton('Организатор')
    item_part = types.KeyboardButton('Участник')
    keyb_first.row(item_org, item_part)
    bot.send_message(chat_id, "Привет!\nВыбери свою роль:", reply_markup=keyb_first)

@bot.message_handler(func=lambda message: message.text == "Организатор" or  message.text == "Участник")
def org_start(m):
    keyb_first = types.ReplyKeyboardRemove()
    chat_id = m.chat.id
    if m.text == 'Организатор':
        bot.send_message(chat_id, 'организуй', reply_markup=keyb_first)
    elif m.text == 'Участник':
        bot.send_message(chat_id, 'Введи кодовое слово игры, в которой ты участвуешь', reply_markup=keyb_first)
        @bot.message_handler(content_types=['text'])
        def part_gamenametaker(m):
            chat_id = m.chat.id
            if m.text not in game_names:
                bot.send_message(chat_id, "Такой текущей партии нет")
            else:
                bot.send_message(chat_id, "Введи своё имя и фамилию")


bot.polling()
