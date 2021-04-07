import telebot as tb
from telebot import types
import csv
#организатор - название катки, установка дедлайна, сколько человек зарегалось, нужно ли учитывать степень знакомства
#участник - запросить имя и название катки, проверить отсутствие имени среди уже взятых, после дедлайна прислать киборд со списком взятых имён и кнопкой завершения, когда все опросы собраны или орг принудительно начал игру прислать имя жертвы

#пока игра не завершается автоматически когда кончаются жертвы
#есть план-капкан стирать из файла инфу про игру как только она кончилась тогда не придётся проверять введённое оргом имя игры на уникальность
token = '1555845859:AAFT12GCr7l-vK8S67KGtqUAyOVM7_hl7Vc'
bot = tb.TeleBot(token, parse_mode=None)

def status_writer(id, status):
    #ЖЕНЯ СДЕЛАЙ

@bot.message_handler(content_types=['text'])
def main_body(m):
    user_text = m.text
    user_id = m.chat.id
    user_state = 'ДОСТАТЬ ИЗ ФАЙЛА' #ЖЕНЯ СДЕЛАЙ
    ids = 'ДОСТАТЬ ИЗ ФАЙЛА'
    if user_text == '\help':
        bot.send_message(user_id, 'бог поможет')
    id_check(user_id)
    if user_state == 'role':
        keyb_first = types.ReplyKeyboardRemove()
        if user_text == 'Организатор':
            bot.send_message(user_id, "Введите кодовое имя для вашей игры:")
            status_writer(user_id, 'ogamen')
        elif user_text == 'Участник':
            bot.send_message(chat_id, 'Введи кодовое слово игры, в которой ты участвуешь', reply_markup=keyb_first)
            status_writer(user_id, 'gamen')

    elif user_state == 'gamen':
        part_gamenametaker(user_text, user_id)

    elif user_state == 'partn':
        part_nametaker(user_text, user_id)

    elif user_state == 'quest':
        if user_text == 'Готово!':
            part_endquest(user_id)
        else:
            #ДОПИСАТЬ ПОЛУЧЕННУЮ ФАМИЛИЮ user_text В СПИСЕК ЗНАКОМЦЕВ В ФАЙЛЕ
    elif user_state == 'pl' and user_text == 'меня нашли':
        part_killed(user_id)

def id_check(id):
    ids = 'ДОСТАТЬ ИЗ ФАЙЛА'
    if id not in ids:
        command_start(id)
        status_writer(id, 'role')

def command_start(chat_id):
    keyb_first = types.ReplyKeyboardMarkup()
    keyb_first.add(types.KeyboardButton(el) for el in ['Организатор', 'Участник'])
    bot.send_message(chat_id, "Привет!\nВыбери свою роль:", reply_markup=keyb_first)

def part_gamenametaker(text, chat_id):
    game_names = 'ДОСТАТЬ ИЗ ФАЙЛА'
    if text not in game_names:
        bot.send_message(chat_id, "Такой текущей партии нет, попробуй ещё раз")
    else:
        status_writer(chat_id, 'partn')
        bot.send_message(chat_id, "Введи своё имя и фамилию")

def part_nametaker(text, chat_id):
    names = 'ДОСТАТЬ ИЗ ФАЙЛА'
    if text in names:
        bot.send_message(chat_id, "Это имя уже занято, попробуй ещё раз")
    else:
        bot.send_message(chat_id, "Ура, регистрация пройдена! Жди начала опроса.")
        status_writer(chat_id, 'regd')

def part_quest(chat_id):
    status_writer(chat_id, 'quest')
    keyb_q = types.ReplyKeyboardMarkup()
    names = 'ДОСТАТЬ СПИСОК ФАМИЛИЙ ИЗ ФАЙЛА'
    keyb_q.add(types.KeyboardButton(n) for n in names)
    n = types.KeyboardButton('Готово!')
    keyb_q.add(n)
    bot.send_message(chat_id, "Выбери в этом списке тех людей, с которыми ты знаком, то есть узнаешь их, если увидишь. Нажми \"Готово!\", когда закончишь.", reply_markup=keyb_q)

def part_endquest(chat_id):
    keyb_q = types.ReplyKeyboardRemove()
    status_writer(chat_id, 'questd')
    bot.send_message(chat_id, "Осталось дождаться начала игры!")

def part_startgame(chat_id):
    pray = 'ДОСТАТЬ ИЗ ФАЙЛА'
    status_writer(chat_id, 'pl')
    bot.send_message(сhat_id, "Игра началась! Сейчас твоя задача - застать свою жертву наедине без свидетелей и сказать ей \"Тебя поймали\". После этого пойманный тобой человек должен при тебе написать боту со своего устройства \"меня нашли\", после чего тебе придёт имя новой жертвы. Остерегайся, ведь не только ты сегодня охотишься!\n Твоя первая цель - ", pray)

def part_killed(chat_id):
    status_writer(chat_id, 'x')
    bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")
    killer_id = 'ДОСТАТЬ ИЗ ФАЙЛА'
    new_pray = 'ДОСТАТЬ ИЗ ФАЙЛА в строчке  chat_id'
    bot.send_message(killer_id, "Успехх! Твоя новая цель - ", new_pray)
