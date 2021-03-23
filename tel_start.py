import telebot as tb
from telebot import types
import pandas as pd
import csv
#организатор - название катки, установка дедлайна, сколько человек зарегалось, нужно ли учитывать степень знакомства
#участник - запросить имя и название катки, проверить отсутствие имени среди уже взятых, после дедлайна прислать киборд со списком взятых имён и кнопкой завершения, когда все опросы собраны или орг принудительно начал игру прислать имя жертвы

#пока игра не завершается автоматически когда кончаются жертвы
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
    bot.send_message(chat_id, "WELCOMEMESSAGE")
    bot.send_message(chat_id, "Выбери свою роль:", reply_markup=keyb_first)

@bot.message_handler(func=lambda message: message.text == 'Организатор')
def status_maker(m):
    #ЗАПИСАТЬ В ФАЙЛ СТАТУС ogamen

def org_start(chat_id):
    bot.send_message(chat_id, "Введите кодовое имя для вашей игры:")
    game_names = list()
    if m.text not in game_names:
        act_1 = types.KeyboardButton('Сколько человек уже зарегистрировалось?')
        act_2 = types.KeyboardButton('Я тоже хочу участвовать в игре')
        act_3 = types.KeyboardButton('Завершить регистрацию')
        keyb_org.add(act_1, act_2, act_3)
        #ЗАПИСАТЬ В ФАЙЛ СТАТУС ИГРЫ R И СТАТУС ОРГА OPARTN
        bot.send_message(chat_id, "Игра " + m.text + " создана, теперь игроки могут начать регистрироваться по её кодовому имени.", reply_markup=keyb_org)

def org_regcounter(chat_id):
    #пройтись по файлу и посчитать участников этой игры со статусом REGD
    regcounter = 0
    bot.send_message(chat_id, str(regcouner) + " человек")

def org_name(chat_id):
    bot.send_message(chat_id, "Введите своё имя и фамилию")
    @bot.message_handler(content_types=['text'])
    def org_name1(m):
        #ЗАПИСАТЬ ИМЯ В ФАЙЛ
        bot.send_message(chat_id, "Ура, регистрация пройдена!)

def org_startquest(m):
    #вытащить из файла id всех участников этой игры кроме орга и сменить статус игры на Q
    ids = list()
    keyb_org = types.ReplyKeyboardRemove()
    keyb_orgq = types.ReplyKeyboardMarkup()
    act_1 = types.KeyboardButton('Сколько человек уже прошло опрос?')
    act_2 = types.KeyboardButton('Пройти опрос')
    act_3 = types.KeyboardButton('Завершить прохождение опросов и начать игру')
    keyb_orgq.add(act_1, act_2, act_3)
    bot.send_message(chat_id, "Опрос о знакомых начался", reply_markup=keyb_orgq)
    for some_id in id:
        part_quest(some_id)

def org_quest(chat_id):
    keyb_orgq = types.ReplyKeyboardRemove()
    part_quest(chat_id)
    bot.send_message(chat_id, "Опрашивание идёт", reply_markup=keyb_orgq)

def org_startgame(chat_id):
    keyb_orgq = types.ReplyKeyboardRemove()
    idplusorg = list()
    #вот тут происходит возня с циклами и в файл вписываются нужные имена, статус игры меняется на P
    for that_id in idplusorg:
        #а здесь каждому игроку из его строки достаётся имя его жертвы и его статус меняется на pl
        pray = "boba"
        bot.send_message(that_id, "Игра началась! Твоя цель - ", pray)
    keyb_orgp = types.ReplyKeyboardMarkup()
    act_1 = types.KeyboardButton('Статистика')
    act_2 = types.KeyboardButton('меня нашли')
    act_3 = types.KeyboardButton('Принудительно завершить игру')
    act_4 = types.KeyboardButton('Разослать новости')
    bot.send_message(chat_id, 'Вы успешно начали игру', reply_markup=keyb_orgp)

def stats(chat_id):
    #найти чё надо в чате
    bot.send_message(chat_id, 'messagee')

def endgame(chat_id):
    keyb_orgp = types.ReplyKeyboardRemove()
    #посчитать по файлу победителей
    for another_id in idplusorg:
        bot.send_message(another_id, 'Игра завершена. Первым убит энтом а вторым тот а выиграл вообще петя')
    #сменить статус игры на E и статусы всех игрокоов на X

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
    @bot.message_handler(func=lambda message: message.text == 'Готово!'):
    def part_endquest(chat_id):
        keyb_q = types.ReplyKeyboardRemove()
        #ЗАПИСАТЬ СПИСОК ЗНАКОМЫХ В ФАЙЛ В КАКОМ ТАМ НАДО ФОРМАТЕ
        #ЗАПИСАТЬ В ФАЙЛ СТАТУС questd и 0 в счётчик жертв
        bot.send_message(chat_id, "Осталось дождаться начала игры!")

def part_game(m):
    if m.text  == 'меня нашли':
        #найти в файле строку убийцы и по его id выслать имя новой жертвы и добавить +1 в счётчик
        #записать в файл статус x
        bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")

bot.polling()
