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
    well = 'ЖЕНЯ СДЕЛАЙ'

def add_friend(chat_id, text):
    well = 'ДОПИСАТЬ ПОЛУЧЕННЫЙ ТЕКСТ В ФАЙЛ В СПИСОК ЗНАКОМЦЕВ ПОЛЬЗОВАТЕЛЯ'

def id_check(id):
    ids = 'ДОСТАТЬ ИЗ ФАЙЛА'
    if id not in ids:
        well = 'ЗАПИСАТЬ АЙДИ В ФАЙЛ'
        command_start(id)
        status_writer(id, 'role')

def stats_reg(chat_id):
    result = 'ДОСТАТЬ ИЗ ФАЙЛА СКОЛЬКО ЧЕЛОВЕК ЗАРЕГИСТРИРОВАЛОСЬ НА ИГРУ ЭТОГО ОРГАНИЗАТОРА'
    bot.send_message(chat_id, "Уже зарегистрировалось" + result + "человек")

def stats_quest(chat_id):
    result = 'ДОСТАТЬ ИЗ ФАЙЛА СКОЛЬКО ЧЕЛОВЕК УЖЕ ПРОШЛО ОПРОС У ЭТОГО ОРГАНИЗАТОРА'
    bot.send_message(chat_id, "Уже прошло опрос" + result + "человек")

def stats_game(chat_id):
    result_kill = 'ДОСТАТЬ ИЗ ФАЙЛА КОЛИЧЕСТВО УБИТЫХ'
    result_live = 'ДОСТАТЬ ИЗ ФАЙЛА ЖИВУЧИХ'
    bot.send_message(chat_id, "Вышло из игры" + result_kill + "человек, а ещё играет " + result_live + 'человек')

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
    bot.send_message(сhat_id, "Игра началась! Сейчас твоя задача - застать свою жертву наедине без свидетелей и сказать ей \"Тебя поймали\". После этого пойманный тобой человек должен при тебе написать боту со своего устройства \"меня нашли\", и тебе придёт имя новой жертвы. Остерегайся, ведь не только ты сегодня охотишься!\n Твоя первая цель - ", pray)

def part_killed(chat_id):
    status_writer(chat_id, 'done')
    bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")
    killer_id = 'ДОСТАТЬ ИЗ ФАЙЛА'
    new_pray = 'ДОСТАТЬ ИЗ ФАЙЛА в строчке  chat_id'
    bot.send_message(killer_id, "Успехх! Твоя новая цель - ", new_pray)

def org_gamenametaker(text, chat_id):
    game_names = 'ДОСТАТЬ ИЗ ФАЙЛА'
    if text in game_names:
        bot.send_message(chat_id, "Такая партия уже существует, попробуйте ещё раз")
    else:
        name = 'ЗАПИСАТЬ В ФАЙЛ НАЗВАНИЕ НОВОЙ ИГРЫ text'
        status_writer(chat_id, orgreg)
        keyb_org = types.ReplyKeyboardMarkup
        act_1 = types.KeyboardButton('Сколько человек уже зарегистрировалось?')
        act_2 = types.KeyboardButton('Я тоже хочу участвовать в игре')
        act_3 = types.KeyboardButton('Завершить регистрацию')
        keyb_org.add(act_1, act_2, act_3)
        bot.send_message(chat_id, "Игра создана. Чтобы зарегистрироваться, участникам нужно будет ввести её название: " + text, reply_markup=keyb_org)

def org_startquest(chat_id):
    ids = 'ДОСТАТЬ ЯБЫ ВСЕХ УЧАСТНИКОВ ИЗ ФАЙЛА'
    keyb_org = types.ReplyKeyboardRemove()
    keyb_orgq = types.ReplyKeyboardMarkup()
    act_1 = types.KeyboardButton('Сколько человек уже прошло опрос?')
    act_3 = types.KeyboardButton('Завершить прохождение опросов и начать игру')
    keyb_orgq.add(act_1, act_3)
    bot.send_message(chat_id, "Опрос о знакомых начался", reply_markup=keyb_orgq)
    status_writer(id, 'orgquest') #здесь надо проследить чтобы статусврайтер не переписывал и статул участниковой строки орга если она есть
    for some_id in id:
        part_quest(some_id)

def org_start(chat_id, text):
    if text == 'Сколько человек уже прошло опрос?':
        stats_reg(chat_id)
    elif text == 'Я тоже хочу участвовать в игре':
        well = 'ЗАПИСАТЬ АЙДИ В ФАЙЛ повторно'
        keyb_org = types.ReplyKeyboardRemove
        bot.send_message(chat_id, "Введите своё имя и фамилию")
        status_writer(user_id, 'partn')
    elif text == 'Завершить регистрацию':
        org_startquest(chat_id)

def org_quest(chat_id, text):
    if text == 'Сколько человек уже прошло опрос?':
        stats_quest(chat_id)
    elif text == 'Завершить прохождение опросов и начать игру':
        keyb_orgq = types.ReplyKeyboardRemove
        status_writer(chat_id, 'orggame')
        ids = 'ДОСТАТЬ ИЗ ФАЙЛА'
        for some_id in ids:
            part_startgame(some_id)
        keyb_orgp = types.ReplyKeyboardMarkup()
        act_1 = types.KeyboardButton('Статистика')
        act_2 = types.KeyboardButton('меня нашли')
        act_3 = types.KeyboardButton('Принудительно завершить игру')
        act_4 = types.KeyboardButton('Разослать новости')
        bot.send_message(chat_id, 'Вы успешно начали игру', reply_markup=keyb_orgp)

def org_game(chat_id, text):
    if text =='Статистика':
        stats_game(chat_id)
    elif text == 'Принудительно завершить игру':
        ids = 'ДОСТАТЬ ИЗ ФАЙЛА'
        winner = 'ДОСТАТЬ'
        for some_id in ids:
            status_writer(some_id, done)
            bot.send_message(some_id, 'Игра закончена. !! Победитель - ' + winner)
        bot.send_message(chat_id, 'Ваша игра завершена. Надеемся, все повеселились. Мы открыты для отзывов и предложений: ')


@bot.message_handler(content_types=['text'])
def main_body(m):
    user_text = m.text
    user_id = m.chat.id
    id_check(user_id)
    user_state = 'ДОСТАТЬ ИЗ ФАЙЛА' #ЖЕНЯ СДЕЛАЙ
    if user_text == '\help':
        bot.send_message(user_id, 'бог поможет')

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
            add_friend(user_id, user_text)
    elif user_state == 'pl' and user_text == 'меня нашли':
        part_killed(user_id)

    elif user_state == 'ogamen':
        org_gamenametaker(user_text, user_id)

    elif user_state == 'orgreg':
        org_start(user_id, user_text)

    elif user_state == 'orgquest':
        org_quest(user_id, user_text)

    elif user_state == 'orggame':
        org_game(user_id, user_text)

bot.polling()
