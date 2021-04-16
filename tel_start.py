import telebot as tb
from telebot import types
import csv
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'cybersep-310108-c1268b1fb570.json'

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


fifile = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg' #здесь надо будет вставить адрес табличьки, когда она появитс

spreadsheet = service.spreadsheets().get(spreadsheetId = fifile).execute()
sheetlist = spreadsheet.get('sheets')

#организатор - название катки, установка дедлайна, сколько человек зарегалось, нужно ли учитывать степень знакомства
#участник - запросить имя и название катки, проверить отсутствие имени среди уже взятых, после дедлайна прислать киборд со списком взятых имён и кнопкой завершения, когда все опросы собраны или орг принудительно начал игру прислать имя жертвы

#пока игра не завершается автоматически когда кончаются жертвы

token = '1555845859:AAFT12GCr7l-vK8S67KGtqUAyOVM7_hl7Vc'
bot = tb.TeleBot(token, parse_mode=None)

def status_writer(id, status):
    rrr=2
for rrr in range (2;1000):
    ranges: {
         "sheetId": shit_id,
        "startRowIndex": rrr,
        "endRowIndex": rrr+1,
        "startColumnIndex": 1,
        "endColumnIndex": 2
    } #

    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    sss = results['values']
    if sss==chat_id:
        nnn=rrr
        rrr=rrr+1000
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile,
            body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                     {"range":
                         {
                            "sheetId": shit_id
                            "startRowIndex": nnn,
                            "endRowIndex": nnn+1,
                            "startColumnIndex": 3,
                            "endColumnIndex": 4
                         },
                     "majorDimension": "ROWS",
                     "values": [[status],]}
                        ]
            }).execute()
    else:
         rrr=rrr+1

def add_friend(chat_id, text):
    rrr=2
    for rrr in range (2;1000):
        ranges: {
            "sheetId": shit_id,
            "startRowIndex": rrr,
            "endRowIndex": rrr+1,
            "startColumnIndex": 1,
            "endColumnIndex": 2
                } #

    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    sss = results['values']
    if sss==chat_id:
        nnn=rrr
        rrr=rrr+1000
        ranges: {
            "sheetId": shit_id,
            "startRowIndex": nnn,
            "endRowIndex": nnn+1,
            "startColumnIndex": 4,
            "endColumnIndex": 5
                } #

                results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        befff = results['values']
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
             "valueInputOption": "USER_ENTERED",
             "data": [
                 {"range": {
                       "sheetId": shit_id,
                       "startRowIndex": nnn,
                       "endRowIndex": nnn+1,
                       "startColumnIndex": 4,
                       "endColumnIndex": 5
                  }} # ,
             "majorDimension": "ROWS",
             "values": [
                        [befff, ';', text]
                      ]}
                      ]
            }).execute()
    else:
         rrr=rrr+1

def id_check(id):
    ranges: {
    "sheetId": shit_id,
    "startRowIndex": 2,
    "endRowIndex": 1000,
    "startColumnIndex": 1,
    "endColumnIndex": 2
    } #

    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    ids = results['values']

    if id not in ids:
        rrr=2
        for rrr in range (2;1000):
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": rrr,
            "endRowIndex": rrr+1,
            "startColumnIndex": 3,
            "endColumnIndex": 4
            } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            sss = results['values']
            if sss==''
                nnn=rrr
                rrr=rrr+1000
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile,
                body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                {"range":
                {
                "sheetId": shit_id,
                "startRowIndex": nnn,
                "endRowIndex": nnn+1,
                "startColumnIndex": 1,
                "endColumnIndex": 2
                },
                "majorDimension": "ROWS",
                "values": [[chat_id],]}
                    ]
                    }).execute()
            else:
                rrr=rrr+1
    command_start(id)
    status_writer(id, 'role')

def stats_reg(chat_id):
    rrr=2
    kkk=0
    for rrr in range (2;1000):
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": rrr,
        "endRowIndex": rrr+1,
        "startColumnIndex": 3,
        "endColumnIndex": 4
            } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['values']
        rrr=rrr+1
        if sss=='regd':#НУЖНЫ СТАТУС
            kkk=kkk+1

    result=kkk
    bot.send_message(chat_id, "Уже зарегистрировалось" + result + "человек")

def stats_quest(chat_id):
    rrr=2
    kkk=0
    for rrr in range (2;1000):
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": rrr,
        "endRowIndex": rrr+1,
        "startColumnIndex": 3,
        "endColumnIndex": 4
            } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['values']
        rrr=rrr+1
        if sss=='questd':#НУЖНЫ СТАТУС
            kkk=kkk+1
    result=kkk
    bot.send_message(chat_id, "Уже прошло опрос" + result + "человек")

def stats_game(chat_id):
    rrr=2
    kkk=0
    lll=0
    for rrr in range (2;1000):
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": rrr,
        "endRowIndex": rrr+1,
        "startColumnIndex": 3,
        "endColumnIndex": 4
            } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['values']
        rrr=rrr+1
        if sss=='done':#НУЖНЫ СТАТУС
            kkk=kkk+1

        if sss=='pl':
            lll=lll+1

    result_kill=kkk
    result_live=lll
    bot.send_message(chat_id, "Вышло из игры" + result_kill + "человек, а ещё играет " + result_live + 'человек')

def command_start(chat_id):
    keyb_first = types.ReplyKeyboardMarkup()
    keyb_first.add(types.KeyboardButton(el) for el in ['Организатор', 'Участник'])
    bot.send_message(chat_id, "Привет!\nВыбери свою роль:", reply_markup=keyb_first)

def part_gamenametaker(text, chat_id):
    for sheet in sheetlist:
        if title==text:
            sh_id = sheetId
            status_writer(chat_id, 'partn')
            bot.send_message(chat_id, "Введи своё имя и фамилию")
            return sh_id
    bot.send_message(chat_id, "Такой текущей партии нет, попробуй ещё раз")

def part_nametaker(text, chat_id):
    ranges: {
    "sheetId": shit_id,
    "startRowIndex": 2,
    "endRowIndex": 1000,
    "startColumnIndex": 2,
    "endColumnIndex": 3
    } #

    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    names = results['values']

    if text in names:
        bot.send_message(chat_id, "Это имя уже занято, попробуй ещё раз")
    else:
        rrr=2
        for rrr in range (2;1000):
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": rrr,
            "endRowIndex": rrr+1,
            "startColumnIndex": 3,
            "endColumnIndex": 4
            } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            sss = results['values']
            if sss==chat_id:
                nnn=rrr
                rrr=rrr+1000
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile,
                body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                {"range":
                    {
                    "sheetId": shit_id,
                    "startRowIndex": nnn,
                    "endRowIndex": nnn+1,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                    },
                "majorDimension": "ROWS",
                "values": [[text],]}
            ]
                }).execute()
            else:
                rrr=rrr+1
    bot.send_message(chat_id, "Ура, регистрация пройдена! Жди начала опроса.")
    status_writer(chat_id, 'regd')

def part_quest(chat_id):
    status_writer(chat_id, 'quest')
    keyb_q = types.ReplyKeyboardMarkup()
    ranges: {
    "sheetId": shit_id,
    "startRowIndex": 2,
    "endRowIndex": 1000,
    "startColumnIndex": 2,
    "endColumnIndex": 3
        } #

    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    names = results['values']
    keyb_q.add(types.KeyboardButton(n) for n in names)
    n = types.KeyboardButton('Готово!')
    keyb_q.add(n)
    bot.send_message(chat_id, "Выбери в этом списке тех людей, с которыми ты знаком, то есть узнаешь их, если увидишь. Нажми \"Готово!\", когда закончишь.", reply_markup=keyb_q)

def part_endquest(chat_id):
    keyb_q = types.ReplyKeyboardRemove()
    status_writer(chat_id, 'questd')
    bot.send_message(chat_id, "Осталось дождаться начала игры!")

def part_startgame(chat_id):
    rrr=2
    for rrr in range (2;1000):
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": rrr,
        "endRowIndex": rrr+1,
        "startColumnIndex": 1,
        "endColumnIndex": 2
            } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                 ranges = ranges,
                                 valueRenderOption = 'FORMATTED_VALUE',
                                 dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['values']
        if sss==chat_id:
            nnn=rrr
            rrr=rrr+1000
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": nnn,
            "endRowIndex": nnn+1,
            "startColumnIndex": 5,
            "endColumnIndex": 6
                } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            pray=results
        else:
            rrr=rrr+1
    status_writer(chat_id, 'pl')
    bot.send_message(сhat_id, "Игра началась! Сейчас твоя задача - застать свою жертву наедине без свидетелей и сказать ей \"Тебя поймали\". После этого пойманный тобой человек должен при тебе написать боту со своего устройства \"меня нашли\", и тебе придёт имя новой жертвы. Остерегайся, ведь не только ты сегодня охотишься!\n Твоя первая цель - ", pray)

def part_killed(chat_id):
    status_writer(chat_id, 'done')
    bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")
    rrr=2
    for rrr in range (2;1000):
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": rrr,
        "endRowIndex": rrr+1,
        "startColumnIndex": 1,
        "endColumnIndex": 2
        } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                 ranges = ranges,
                                 valueRenderOption = 'FORMATTED_VALUE',
                                 dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['values']
        if sss==chat_id:
            nnn=rrr
            rrr=rrr+1000
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": rrr,
            "endRowIndex": rrr+1,
            "startColumnIndex": 2,
            "endColumnIndex": 3
            } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            ubit=results
            hhh=2
            for hhh in range(2;1000):
                ranges: {
                "sheetId": shit_id,
                "startRowIndex": hhh,
                "endRowIndex": hhh+1,
                "startColumnIndex": 5,
                "endColumnIndex":
                } #

                results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                         ranges = ranges,
                                         valueRenderOption = 'FORMATTED_VALUE',
                                         dateTimeRenderOption = 'FORMATTED_STRING').execute()
                jjj=results
                if jjj==ubit:
                    mmm=hhh
                    hhh=hhh+1000
                    ranges: {
                    "sheetId": shit_id,
                    "startRowIndex": mmm,
                    "endRowIndex": mmm+1,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                    } #

                    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                             ranges = ranges,
                                             valueRenderOption = 'FORMATTED_VALUE',
                                             dateTimeRenderOption = 'FORMATTED_STRING').execute()
                    svo=results
                else:
                    hhh=hhh+1
        else:
            rrr=rrr+1
    zzz=2
    for zzz in range (2;1000):
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": zzz,
        "endRowIndex": zzz+1,
        "startColumnIndex": 2,
        "endColumnIndex": 3
        } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                 ranges = ranges,
                                 valueRenderOption = 'FORMATTED_VALUE',
                                 dateTimeRenderOption = 'FORMATTED_STRING').execute()
        you=results
        if you==svo:
            ddd=zzz
            zzz=zzz+1000
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": ddd,
            "endRowIndex": ddd+1,
            "startColumnIndex": 1,
            "endColumnIndex": 2
            } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            killer_id = results
        else:
            zzz=zzz+1
    aaa=2
    for aaa in range(2;1000):
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": aaa,
        "endRowIndex": aaa+1,
        "startColumnIndex": 1,
        "endColumnIndex": 2
            } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                             ranges = ranges,
                             valueRenderOption = 'FORMATTED_VALUE',
                             dateTimeRenderOption = 'FORMATTED_STRING').execute()
        aaaaa=results
        if aaaaa==chat_id:
            ppp=aaa
            aaa=aaa+1000
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": ppp,
            "endRowIndex": ppp+1,
            "startColumnIndex": 5,
            "endColumnIndex": 6
            } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            new_pray = results
        else:
            aaa=aaa+1
    bot.send_message(killer_id, "Успехх! Твоя новая цель - ", new_pray)

def org_gamenametaker(text, chat_id):
    for sheet in sheetlist:
        if title==text:
            bot.send_message(chat_id, "Такая партия уже существует, попробуйте ещё раз")
            break
    else:
        results = service.spreadsheets().batchUpdate(spreadsheetId = fifile, body = {"requests": [{"addSheet": {"properties": {"title": text,"gridProperties": {"rowCount": 1000,"columnCount": 7}}}}]}).execute()
        for sheet in sheetlist:
            if title==text:
                sh_id = sheetId
        status_writer(chat_id, orgreg)
        keyb_org = types.ReplyKeyboardMarkup
        act_1 = types.KeyboardButton('Сколько человек уже зарегистрировалось?')
        act_2 = types.KeyboardButton('Я тоже хочу участвовать в игре')
        act_3 = types.KeyboardButton('Завершить регистрацию')
        keyb_org.add(act_1, act_2, act_3)
        bot.send_message(chat_id, "Игра создана. Чтобы зарегистрироваться, участникам нужно будет ввести её название: " + text, reply_markup=keyb_org)
        return sh_id

def org_startquest(chat_id):
    ranges: {
    "sheetId": shit_id,
    "startRowIndex": 2,
    "endRowIndex": 1000,
    "startColumnIndex": 1,
    "endColumnIndex": 2
        } #

    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    ids = results['values']
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
        rrr=2
        for rrr in range (2;1000):
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": rrr,
            "endRowIndex": rrr+1,
            "startColumnIndex": 3,
            "endColumnIndex": 4
            } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            sss = results['values']
            if sss==''
                nnn=rrr
                rrr=rrr+1000
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile,
                body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                {"range":
                {
                "sheetId": shit_id,
                "startRowIndex": nnn,
                "endRowIndex": nnn+1,
                "startColumnIndex": 1,
                "endColumnIndex": 2
                },
                "majorDimension": "ROWS",
                "values": [[chat_id],]}
                    ]
                    }).execute()
            else:
                rrr=rrr+1#!!!
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
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": 2,
        "endRowIndex": 1000,
        "startColumnIndex": 1,
        "endColumnIndex": 2
            } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                         ranges = ranges,
                                         valueRenderOption = 'FORMATTED_VALUE',
                                         dateTimeRenderOption = 'FORMATTED_STRING').execute()
        ids = results['values']
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
        ranges: {
        "sheetId": shit_id,
        "startRowIndex": 2,
        "endRowIndex": 1000,
        "startColumnIndex": 1,
        "endColumnIndex": 2
            } #

        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                         ranges = ranges,
                                         valueRenderOption = 'FORMATTED_VALUE',
                                         dateTimeRenderOption = 'FORMATTED_STRING').execute()
        ids = results['values']
        rrr=2
        for rrr in range (2;1000):
            ranges: {
            "sheetId": shit_id,
            "startRowIndex": rrr,
            "endRowIndex": rrr+1,
            "startColumnIndex": 3,
            "endColumnIndex": 4
                } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            sss = results['values']
            if sss=='pl':#НУЖНЫ СТАТУС
                wwww=rrr
                ranges: {
                "sheetId": shit_id,
                "startRowIndex": wwww,
                "endRowIndex": wwww+1,
                "startColumnIndex": 2,
                "endColumnIndex": 3
                    } #

                results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                         ranges = ranges,
                                         valueRenderOption = 'FORMATTED_VALUE',
                                         dateTimeRenderOption = 'FORMATTED_STRING').execute()
                winner=results
            rrr=rrr+1
        for some_id in ids:
            status_writer(some_id, done)
            bot.send_message(some_id, 'Игра закончена. !! Победитель - ' + winner)
        bot.send_message(chat_id, 'Ваша игра завершена. Надеемся, все повеселились. Мы открыты для отзывов и предложений: ')


@bot.message_handler(content_types=['text'])
def main_body(m):
    user_text = m.text
    user_id = m.chat.id
    id_check(user_id)
    rrr=2
    for rrr in range (2;1000):
        ranges: {
            "sheetId": shit_id,
            "startRowIndex": rrr,
            "endRowIndex": rrr+1,
            "startColumnIndex": 1,
            "endColumnIndex": 2
            } #

            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['values']
        if sss==user_id:
           nnn=rrr
           rrr=rrr+1000
           ranges: {
           "sheetId": shit_id,
           "startRowIndex": nnn,
           "endRowIndex": nnn+1,
           "startColumnIndex": 3,
           "endColumnIndex": 4
           } #

           results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                            ranges = ranges,
                                            valueRenderOption = 'FORMATTED_VALUE',
                                            dateTimeRenderOption = 'FORMATTED_STRING').execute()
            user_state = results['values']
        else:
         rrr=rrr+1
     #ЖЕНЯ СДЕЛАЙ
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
        shit_id = part_gamenametaker(user_text, user_id)

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
        shit_id = org_gamenametaker(user_text, user_id)

    elif user_state == 'orgreg':
        org_start(user_id, user_text)

    elif user_state == 'orgquest':
        org_quest(user_id, user_text)

    elif user_state == 'orggame':
        org_game(user_id, user_text)

bot.polling()
