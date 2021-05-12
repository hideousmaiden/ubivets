import telebot as tb
import networkx as nx
from telebot import types
import csv
import httplib2
import gspread
import random
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
CREDENTIALS_FILE = 'cybersep-310108-c1268b1fb570.json'
shit_name = '0'
# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

fifile = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg'

spreadsheet = service.spreadsheets().get(spreadsheetId = fifile).execute()
sheetlist = spreadsheet.get('sheets')


#пока игра не завершается автоматически когда кончаются жертвы

token = '1555845859:AAFT12GCr7l-vK8S67KGtqUAyOVM7_hl7Vc'
bot = tb.TeleBot(token, parse_mode=None)

def great_check(id):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for line in records_data:
        if line[0] == str(id):
            return line[1]

def part_gamenametaker(text, chat_id):
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                 ranges = 'A1:C',
                                 valueRenderOption = 'FORMATTED_VALUE',
                                 dateTimeRenderOption = 'FORMATTED_STRING').execute()
    names = results['valueRanges'][0]['values']
    games = {k[2] for k in names if len(k) != 0}
    if text not in games:
        bot.send_message(chat_id, "Такой текущей партии нет, попробуй ещё раз")
    else:
        part_stats = {k[1] for k in names if k[2] == text}
        if 'orgreg' in part_stats:
            client = gspread.authorize(credentials)
            sheet = client.open('Табличька')
            sheet_instance = sheet.get_worksheet(0)
            records_data = sheet_instance.get_all_values()
            for n in range(len(records_data)):
                if records_data[n][0] == str(chat_id):
                    records_data[n][2] = text
                    break
            results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
            "valueInputOption": "USER_ENTERED",
            "data": [{"range": 'A1:F1000', "values": records_data}]}).execute()
            status_writer(chat_id, 'partn')
            bot.send_message(chat_id, "Введи своё имя и фамилию: ")
        else:
            bot.send_message(chat_id, "Регистрация на эту игру уже закончилась, попробуй снова")

def separator(id):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values() #количество строчек в таблице
    edges = []
    isolat = []
    client = gspread.authorize(credentials)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(id):
            game_name = records_data[n][2]
            break
    for line in records_data:
        if line[1] == 'questd' and line[2] == game_name:
            if line[4] != '':
                links = line[4].strip(';').split(';')
                for elem in links:
                    link = []
                    link.append(line[3])
                    link.append(elem)
                    edges.append(tuple(link))
            else:
                isolat.append(line[3])

#графы
    final_cycles = []
    weighted_edges = []
    mutual_edges = []
    finals = []
    raw_graph = nx.DiGraph()
    raw_graph.add_edges_from(edges)
    raw_graph.add_nodes_from(isolat)
    nodes = raw_graph.nodes
    norm_nodes = []
    for x in nodes:
        norm_nodes.append(x)
    for edge_number in range(len(edges)):
        rev_edge = list(edges[edge_number])
        rev_edge.reverse()
        if tuple(rev_edge) not in edges:
            raw_graph.remove_edge(edges[edge_number][0], edges[edge_number][1])
    paths = nx.shortest_path(raw_graph)
    no_conn_rate = len(nodes) + 1
    weighted_edges = []
    for limit in range(4, 0, -1):
        final_cycles = []
        for start in paths:
            for target in nodes:
                if start != target:
                    if target in paths[start]:
                        weight = len(paths[start][target])
                    else:
                        weight = no_conn_rate
                    if weight > limit:
                        weighted_edge = []
                        weighted_edge.append(start)
                        weighted_edge.append(target)
                        weighted_edge.append(weight)
                        weighted_edges.append(tuple(weighted_edge))
        weighted_graph = nx.DiGraph()
        weighted_graph.add_weighted_edges_from(weighted_edges)
        final_paths =  weighted_graph.adj
        if len(weighted_graph.nodes) == len(nodes):
            for x in nx.neighbors(weighted_graph, norm_nodes[0]):
                break
            for path in nx.all_simple_paths(weighted_graph, source = norm_nodes[0], target = x):
                if len(final_cycles) != 2000:
                    if len(path) == len(nodes):
                        final_cycles.append(path)
                else:
                    break
            if len(final_cycles) != 0:
                break
    max_count = 0
    for cycle in final_cycles:
        cycle_count = 0
        for n_number in range(len(nodes) - 1):
            start = cycle[n_number]
            target = cycle[n_number + 1]
            cycle_count += final_paths[start][target]['weight']
        cycle_count += final_paths[cycle[-1]][cycle[0]]['weight']
        if cycle_count >= max_count:
            max_count = cycle_count
            best_cycle = cycle
#запись в фаил
    for n in range(len(records_data)):
        for num in range(len(best_cycle)):
            if records_data[n][3] == best_cycle[num] and num != (len(best_cycle) - 1):
                records_data[n][5] = best_cycle[num + 1]
                break
            elif records_data[n][3] == best_cycle[num] and num == (len(best_cycle) - 1):
                records_data[n][5] = best_cycle[0]
                break
        print(records_data[n])
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
    "valueInputOption": "USER_ENTERED",
    "data": [{"range": 'A1:F1000', "values": records_data}]}).execute()

def status_writer(id, status):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(id):
            records_data[n][1] = status
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
    "valueInputOption": "USER_ENTERED",
    "data": [{"range": 'A1:F1000', "values": records_data}]}).execute()

def add_friend(chat_id, text):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            records_data[n][4] += ';'
            records_data[n][4] += text
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
    "valueInputOption": "USER_ENTERED",
    "data": [{"range": 'A1:F', "values": records_data}]}).execute()

def stats_reg(chat_id):
    result = 0
    client = gspread.authorize(credentials)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    for line in records_data:
        if line[1] == 'regd' and line[2] == game_name:
            result += 1
    if result == 1:
        bot.send_message(chat_id, "Одна людина - тяжела година, - сказала тётя Зина, глотнув стакан бензина.")
    else:
        bot.send_message(chat_id, "Уже зарегистрировалось " + str(result) + " людёв")

def stats_quest(chat_id):
    result = 0
    client = gspread.authorize(credentials)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    for line in records_data:
        if line[1] == 'questd' and line[2] == game_name:
            result += 1
    if result == 1:
        bot.send_message(chat_id, "Одна людина - тяжела година, - сказала тётя Зина, глотнув стакан бензина.")
    else:
        bot.send_message(chat_id, "Уже прошло опрос " + str(result) + " человек")

def stats_game(chat_id):
    result_kl = 0
    result_pl = 0
    client = gspread.authorize(credentials)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    for line in records_data:
        if line[1] == 'done' and line[2] == game_name:
            result_kl += 1
        elif line[1] == 'pl' and line[2] == game_name:
            result_pl += 1
    bot.send_message(chat_id, "Вышло из игры " + str(result_kl) + " человек, а ещё играет " + str(result_pl) + ' человек')

def send_news(chat_id):
    result_kl = 0
    result_pl = 0
    client = gspread.authorize(credentials)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    for line in records_data:
        if line[1] == 'done' and line[2] == game_name:
            result_kl += 1
        elif line[1] == 'pl' and line[2] == game_name:
            result_pl += 1
    for l in records_data:
        if line[1] == 'pl' and line[2] == game_name:
            bot.send_message(l[0], "Новостная сводка!!\nВышло из игры " + str(result_kl) + " человек, а ещё играет " + str(result_pl) + ' человек.\nБудьте осторожны в пустынных коридорах!')

def command_start(id):
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                 ranges = 'A1:A',
                                 valueRenderOption = 'FORMATTED_VALUE',
                                 dateTimeRenderOption = 'FORMATTED_STRING').execute()
    sss = results['valueRanges'][0]['values']
    resultss = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
        "valueInputOption": "USER_ENTERED",
        "data":
            {"range": 'A' + str((len(sss) + 1)) + ':' + 'C' + str((len(sss) + 1)),
             "majorDimension": "ROWS",
             "values": [[id, 'role', '-'],]}
        }).execute()
    keyb_first = types.ReplyKeyboardMarkup()
    for el in ['Организатор', 'Участник']:
        keyb_first.add(types.KeyboardButton(el))
    bot.send_message(id, "Привет!\nВыбери свою роль:", reply_markup=keyb_first)

def part_nametaker(text, chat_id):
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                 ranges = 'D1:D',
                                 valueRenderOption = 'FORMATTED_VALUE',
                                 dateTimeRenderOption = 'FORMATTED_STRING').execute()
    names = results['valueRanges'][0]['values']
    part_names = {k[0] for k in names if len(k) != 0}
    if text in part_names:
        bot.send_message(chat_id, "Это имя уже занято, попробуй ещё раз")
    else:
        client = gspread.authorize(credentials)
        sheet = client.open('Табличька')
        sheet_instance = sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_values()
        for n in range(len(records_data)):
            if records_data[n][0] == str(chat_id):
                records_data[n][3] = text
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": 'A1:F1000', "values": records_data}]}).execute()
        bot.send_message(chat_id, "Ура, регистрация пройдена! Жди начала опроса.")
        status_writer(chat_id, 'regd')

def part_quest(chat_id, records_data, game_name):
    status_writer(chat_id, 'quest')
    keyb_q = types.ReplyKeyboardMarkup()
    names = {records_data[p][3] for p in range(len(records_data)) if records_data[p][2] == game_name and records_data[p][1] != 'partn' and records_data[p][0] != chat_id}
    for name in names: keyb_q.add(types.KeyboardButton(name))
    n = types.KeyboardButton('Готово!')
    keyb_q.add(n)
    bot.send_message(chat_id, "Выбери в этом списке тех людей, с которыми ты знаком, то есть узнаешь их, если увидишь. Нажми \"Готово!\", когда закончишь.\nПожалуйста, не нажимай на имена слишком быстро, иначе бот не успеет прогрузиться и считать их все.", reply_markup=keyb_q)

def part_endquest(chat_id):
    keyb_q = types.ReplyKeyboardRemove()
    status_writer(chat_id, 'questd')
    bot.send_message(chat_id, "Осталось дождаться начала игры!", reply_markup = keyb_q)

def part_startgame(some_id):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for line in records_data:
        if line[0] == str(some_id):
            prey = line[5]
    status_writer(some_id, 'pl')
    bot.send_message(some_id, u"""Игра началась!""")
    bot.send_photo(some_id, open('telebot_4.jpg', 'rb'))
    bot.send_message(some_id, """Сейчас твоя задача - застать свою жертву наедине без свидетелей и сказать ей ***Тебя поймали***.\nПосле этого пойманный тобой человек должен при тебе ___написать боту___ со своего устройства ***меня нашли***, и тебе придёт имя новой жертвы. Остерегайся, ведь не только ты сегодня охотишься!\nТвоя первая цель - """ + prey, parse_mode='Markdown')

def part_killed(chat_id):
    status_writer(chat_id, 'done')
    bot.send_photo(chat_id, open('telebot_2.jpg', 'rb'))
    bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    doomed_counter = 0
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id) and records_data[n][2] == game_name:
            doomed = records_data[n][3]
            victim_name = records_data[n][5]
            records_data[n][5] = ''
    for n in range(len(records_data)):
        if records_data[n][5] == doomed:
            killer_id = records_data[n][0]
            records_data[n][5] = victim_name
    for line in records_data:
        if line[2] == game_name and line[5] != '':
            doomed_counter += 1
    print(doomed_counter)
    if doomed_counter == 2:
        for line in records_data:
            if line[3] == '' and line[2] == game_name:
                org_id = line[0]
        thats_all(org_id)
    else:
        pic = random.choice(['telebot_3.jpg', 'telebot_5.jpg', 'telebot_6.jpg'])
        bot.send_photo(chat_id, open(pic, 'rb'))
        bot.send_message(killer_id, "Успехх! Твоя новая цель - " + victim_name)
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
    "valueInputOption": "USER_ENTERED",
    "data": [{"range": 'A1:F1000', "values": records_data}]}).execute()

def org_gamenametaker(text, chat_id):
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                 ranges = 'C1:C',
                                 valueRenderOption = 'FORMATTED_VALUE',
                                 dateTimeRenderOption = 'FORMATTED_STRING').execute()
    names = results['valueRanges'][0]['values']
    games = {k[0] for k in names if len(k) != 0}
    if text in games:
        bot.send_message(chat_id, "Такая партия уже существует, попробуйте ещё раз")
    else:
        client = gspread.authorize(credentials)
        sheet = client.open('Табличька')
        sheet_instance = sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_values()
        for n in range(len(records_data)):
            if records_data[n][0] == str(chat_id):
                records_data[n][2] = text
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": 'A1:F1000', "values": records_data}]}).execute()

        keyb_org = types.ReplyKeyboardMarkup()
        for i in ['Сколько человек уже зарегистрировалось?', 'Завершить регистрацию'] : keyb_org.add(types.KeyboardButton(i))
        status_writer(chat_id, 'orgreg')
        bot.send_message(chat_id, "Игра создана!!\nЧтобы зарегистрироваться, участникам нужно будет ввести её название: ***" + text + '***', parse_mode='Markdown', reply_markup=keyb_org)


def org_startquest(chat_id):
    keyb_orgq = types.ReplyKeyboardMarkup()
    for act in ['Сколько человек уже прошло опрос?', 'Завершить прохождение опросов и начать игру']:
        keyb_orgq.add(types.KeyboardButton(act))
    bot.send_message(chat_id, "Опрос о знакомых начался", reply_markup=keyb_orgq)
    status_writer(chat_id, 'orgquest')
    client = gspread.authorize(credentials)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    ids = {records_data[p][0] for p in range(len(records_data)) if records_data[p][2] == game_name and records_data[p][1] == 'regd'}
    for some_id in ids:
        part_quest(some_id, records_data, game_name)

def org_start(chat_id, text):
    if text == 'Сколько человек уже зарегистрировалось?':
        stats_reg(chat_id)
    elif text == 'Завершить регистрацию':
        org_startquest(chat_id)

def org_quest(chat_id, text):
    if text == 'Сколько человек уже прошло опрос?':
        stats_quest(chat_id)
    elif text == 'Завершить прохождение опросов и начать игру':
        keyb_orgq = types.ReplyKeyboardRemove()
        separator(chat_id)
        status_writer(chat_id, 'orggame')
        client = gspread.authorize(credentials)
        sheet = client.open('Табличька')
        sheet_instance = sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_values()
        for n in range(len(records_data)):
            if records_data[n][0] == str(chat_id):
                game_name = records_data[n][2]
                break
        ids = {records_data[p][0] for p in range(len(records_data)) if records_data[p][2] == game_name and records_data[p][1] == 'questd'}
        for some_id in ids:
            part_startgame(some_id)
        keyb_orgp = types.ReplyKeyboardMarkup()
        for act in ['Статистика', 'Разослать новости', 'Принудительно завершить игру']: keyb_orgp.add(types.KeyboardButton(act))
        bot.send_message(chat_id, 'Вы успешно начали игру', reply_markup=keyb_orgp)

def thats_all(chat_id):
    new_table = []
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    winners = []
    comma = ', '
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    for line in records_data:
        if line[2] == game_name:
            key_fin = types.ReplyKeyboardRemove()
            bot.send_message(line[0], 'Игра закончилась!!\nНадеемся, вам понравилось. Мы открыты для отзывов и предложений: cyparaber@gmail.com', reply_markup = key_fin)
            if line[1] == 'pl':
                winners.append(line[3])
        else:
            new_table.append(line)
    for line in records_data:
        if line[2] == game_name:
            bot.send_message(line[0], 'Вот они победители слева направо:' + comma.join(winners) + '!')
            bot.send_photo(chat_id, open('telebot_7.jpg', 'rb'))
    sheet_instance.clear()
#    print(new_table)
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
    "valueInputOption": "USER_ENTERED",
    "data": [{"range": 'A1:F1000', "values": new_table}]}).execute()

def org_game(chat_id, text):
    if text =='Статистика':
        stats_game(chat_id)
    elif text == 'Принудительно завершить игру':
        thats_all(chat_id)
    elif text == 'Разослать новости':
        send_news(chat_id)
        

def roletaker(chat_id, text):
    keyb_first = types.ReplyKeyboardRemove()
    if text == 'Организатор':
        bot.send_message(chat_id, "Введите кодовое имя для вашей игры:", reply_markup=keyb_first)
        status_writer(chat_id, 'ogamen')
    elif text == 'Участник':
        bot.send_message(chat_id, 'Введи кодовое слово игры, в которой ты участвуешь', reply_markup=keyb_first)
        status_writer(chat_id, 'gamen')
    bot.send_photo(chat_id, open('telebot_1.jpg', 'rb'))

def gamereader(id):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for line in records_data:
        if line[0] == str(id):
            return line[2]

@bot.message_handler(content_types=['text'])
def main_body(m):
    user_text = m.text
    user_id = m.chat.id
    if user_text == '/help':
        bot.send_message(user_id, 'бог поможет')
    elif user_text == '/backstage':
        bot.send_message(user_id, 'нет блин фронт')
    else:
        user_state = great_check(user_id)
        if user_state == 'role':
            roletaker(user_id, user_text)
        elif user_state == 'gamen':
            part_gamenametaker(user_text, user_id)
        elif user_state == 'ogamen':
            org_gamenametaker(user_text, user_id)
        elif user_state == 'partn':
            part_nametaker(user_text, user_id)
        elif user_state == 'quest':
                if user_text == 'Готово!':
                    part_endquest(user_id)
                else:
                    add_friend(user_id, user_text)
        elif user_state == 'pl' and user_text == 'меня нашли':
            part_killed(user_id)
        elif user_state == 'orgreg':
            org_start(user_id, user_text)
        elif user_state == 'orgquest':
            org_quest(user_id, user_text)
        elif user_state == 'orggame':
            org_game(user_id, user_text)
        elif user_state == None:
            command_start(user_id)

bot.polling()
