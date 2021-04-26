import telebot as tb
import networkx as nx
from telebot import types
import csv
import httplib2
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

# Ой а можно я сюда это вынесу, это очень удобно, Сита спасибо
column_name = 'B' #столбец с именами
column_conn = 'D' #столбец со знакомыми
column_vict = 'E' #колонка с жертвами
column_stat = 'C' #колонка со статусами
column_uch = 'F'

#организатор - название катки, установка дедлайна, сколько человек зарегалось, нужно ли учитывать степень знакомства
#участник - запросить имя и название катки, проверить отсутствие имени среди уже взятых, после дедлайна прислать киборд со списком взятых имён и кнопкой завершения, когда все опросы собраны или орг принудительно начал игру прислать имя жертвы

#пока игра не завершается автоматически когда кончаются жертвы

token = '1555845859:AAFT12GCr7l-vK8S67KGtqUAyOVM7_hl7Vc'
bot = tb.TeleBot(token, parse_mode=None)

def great_check(id):
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_values()
    for line in records_data:
        if line[0] == str(id):
            return line[1]

def part_gamenametaker(text, chat_id):
    for sheet in sheetlist:
        if title==text:
            shit_name = title
            rrr=2
            for rrr in range (2,1000):
                ranges = [shit_name+"!A"+str(rrr)] #
                results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
                sss = results['valueRanges'][0]['values']
                if sss == '':
                    nnn = rrr
                    rrr = rrr + 1000
                    results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
                        "valueInputOption": "USER_ENTERED",
                        "data": [
                            {"range": shit_name+"!A"+str(nnn),
                             "majorDimension": "ROWS",
                             "values": [[chat_id],]}
                                ]
                    }).execute()
                else:
                    rrr=rrr+1
            status_writer_zero(chat_id, 'partn')
            bot.send_message(chat_id, "Введи своё имя и фамилию")
            return shit_name
    bot.send_message(chat_id, "Такой текущей партии нет, попробуй ещё раз")

def thats_all(shit_id):
    rangeAll = 'A1:Z'
    request = service.spreadsheets().values().clear(spreadsheetId=shit_id, range=rangeAll, body={})
    response = request.execute()

def separator(shit_id):
    result = service.spreadsheets().values().get(spreadsheetId=shit_id, range="A1:A500").execute()
    rows = result.get('values')
    length = len(rows) #количество строчек в таблице
    edges = []
    isolat = []
    column_name = 'C' #столбец с именами
    column_conn = 'E' #столбец со знакомыми
    column_vict = 'F' #колонка с жертвами
    column_stat = 'D' #колонка со статусами

    for number in range(2,length+1):
        cell_name = column_name + str(number)
        result = service.spreadsheets().values().get(spreadsheetId=shit_id, range=cell_name).execute()
        name = result.get('values')
        cell_stat = column_stat + str(number)
        result = service.spreadsheets().values().get(
        spreadsheetId=shit_id, range=cell_stat).execute()
        stat = result.get('values')
        cell_conn = column_conn + str(number)
        result = service.spreadsheets().values().get(
        spreadsheetId=shit_id, range=cell_conn).execute()
        conn = result.get('values')
        if stat[0][0] == 'Участник':
            if conn != None:
                links = conn[0][0].split(';')
                for elem in links:
                    link = []
                    link.append(name[0][0])
                    link.append(elem)
                    edges.append(tuple(link))
            else:
                isolat.append(name[0][0])

#графы
    final_cycles = []
    weighted_edges = []
    mutual_edges = []

    raw_graph = nx.DiGraph()
    raw_graph.add_edges_from(edges)
    raw_graph.add_nodes_from(isolat)
    nodes = raw_graph.nodes
    for edge_number in range(len(edges)):
        rev_edge = list(edges[edge_number])
        rev_edge.reverse()
        if tuple(rev_edge) not in edges:
            raw_graph.remove_edge(edges[edge_number][0], edges[edge_number][1])
    paths = nx.shortest_path(raw_graph)
    no_conn_rate = len(nodes) + 1
    weighted_edges = []
    for limit in range(4, 0, -1):
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
        cycles = list(nx.simple_cycles(weighted_graph))
        if weighted_graph.nodes == len(nodes) and len(cycles) != 0:
            break
    for cycle in cycles:
        if len(cycle) == len(nodes):
            reversed = []
            reversed.append(cycle[0])
            part = cycle[1:len(cycle)]
            part.reverse()
            reversed.extend(part)
            if reversed not in final_cycles:
                final_cycles.append(cycle)
    max_count = 0
    for cycle in final_cycles:
        cycle_count = 0
        for n_number in range(len(nodes) - 1):
            start = cycle[n_number]
            target = cycle[n_number + 1]
            cycle_count += final_paths[start][target]['weight']
        cycle_count += final_paths[cycle[-1]][cycle[0]]['weight']
        if cycle_count > max_count:
            max_count = cycle_count
            best_cycle = cycle
#запись в фаил
    for number in range(2,length+1):
        cell_name = column_name + str(number)
        result = service.spreadsheets().values().get(
        spreadsheetId=shit_id, range=cell_name).execute()
        name = result.get('values')
        cell_vict = column_vict + str(number)
        for num in range(len(best_cycle)):
            if name[0][0] == best_cycle[num] and num != (len(best_cycle) - 1):
                empt_l = []
                empt_ll = []
                empt_l.append(best_cycle[num+1])
                empt_ll.append(empt_l)
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = shit_id, body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": cell_vict,
                     "values": empt_ll}]
            }).execute()
            elif name[0][0] == best_cycle[num] and num == (len(best_cycle) - 1):
                empt_l = []
                empt_ll = []
                empt_l.append(best_cycle[0])
                empt_ll.append(empt_l)
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = shit_id, body = {
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                    {"range": cell_vict,
                     "values": empt_ll}]
            }).execute()


def status_writer(id, status):
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
    "data": [{"range": 'A1:E1000', "values": records_data}]}).execute()
                
def add_friend(chat_id, text):
    rrr = 2
    for rrr in range (2,200):
        ranges = [shit_name+"!A"+str(rrr)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['valueRanges'][0]['values']
        if sss==chat_id:
            nnn=rrr
            rrr=rrr+1000
            break
    ranges = [shit_name+"!"+column_conn+str(nnn)] #
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                             ranges = ranges,
                             valueRenderOption = 'FORMATTED_VALUE',
                             dateTimeRenderOption = 'FORMATTED_STRING').execute()
    befff = results['valueRanges'][0]['values']
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": shit_name+"!"+column_conn+str(nnn),
             "majorDimension": "ROWS",
             "values": [[befff, ';', text],]}
    ]}).execute()

def stats_reg(chat_id):
    rrr=2
    kkk=0
    for rrr in range (2,1000):
        ranges = [shit_name+"!"+column_stat+str(rrr)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['valueRanges'][0]['values']
        rrr=rrr+1
        if sss=='regd':#НУЖНЫ СТАТУС
            kkk=kkk+1

    result=kkk
    bot.send_message(chat_id, "Уже зарегистрировалось" + result + "человек")

def stats_quest(chat_id):
    rrr=2
    kkk=0
    for rrr in range (2,1000):
        ranges = [shit_name+"!"+column_stat+str(rrr)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['valueRanges'][0]['values']
        rrr=rrr+1
        if sss=='questd':#НУЖНЫ СТАТУС
            kkk=kkk+1
    result=kkk
    bot.send_message(chat_id, "Уже прошло опрос" + result + "человек")

def stats_game(chat_id):
    rrr=2
    kkk=0
    lll=0
    for rrr in range (2,1000):
        ranges = [shit_name+"!"+column_stat+str(rrr)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['valueRanges'][0]['values']
        rrr=rrr+1
        if sss=='done':#НУЖНЫ СТАТУС
            kkk=kkk+1

        if sss=='pl':
            lll=lll+1

    result_kill=kkk
    result_live=lll
    bot.send_message(chat_id, "Вышло из игры" + result_kill + "человек, а ещё играет " + result_live + 'человек')

def command_start(chat_id):
    #todo записать айди и статус role в фаел
    keyb_first = types.ReplyKeyboardMarkup()
    for el in ['Организатор', 'Участник']:
        keyb_first.add(types.KeyboardButton(el))
    bot.send_message(chat_id, "Привет!\nВыбери свою роль:", reply_markup=keyb_first)

def part_nametaker(text, chat_id):
    ranges = [shit_name+"!"+column_name+"2:"+column_name+"1000"] #
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    names = results['valueRanges'][0]['values']
    if text in names:
        bot.send_message(chat_id, "Это имя уже занято, попробуй ещё раз")
    else:
        rrr=2
        for rrr in range (2,1000):
            ranges = [shit_name+"!A"+str(rrr)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            sss = results['valueRanges'][0]['values']
            if sss==chat_id:
                nnn=rrr
                rrr=rrr+1000
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": shit_name+"!"+column_name+str(nnn),
                         "majorDimension": "ROWS",
                         "values": [[text],]}
                ]}).execute()
            else:
                rrr=rrr+1
    bot.send_message(chat_id, "Ура, регистрация пройдена! Жди начала опроса.")
    status_writer(chat_id, 'regd')

def part_quest(chat_id):
    status_writer(chat_id, 'quest')
    keyb_q = types.ReplyKeyboardMarkup()
    ranges = [shit_name+"!"+column_name+"2:"+column_name+"1000"] #
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    names = results['valueRanges'][0]['values']
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
    for rrr in range (2,1000):
        ranges = [shit_name+"!A"+str(rrr)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['valueRanges'][0]['values']
        if sss==chat_id:
            nnn=rrr
            rrr=rrr+1000
            ranges = [shit_name+"!"+column_vict+str(nnn)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            pray = results['valueRanges'][0]['values']
        else:
            rrr=rrr+1
    status_writer(chat_id, 'pl')
    bot.send_message(сhat_id, "Игра началась! Сейчас твоя задача - застать свою жертву наедине без свидетелей и сказать ей \"Тебя поймали\". После этого пойманный тобой человек должен при тебе написать боту со своего устройства \"меня нашли\", и тебе придёт имя новой жертвы. Остерегайся, ведь не только ты сегодня охотишься!\n Твоя первая цель - ", pray)

def part_killed(chat_id):
    status_writer(chat_id, 'done')
    bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")
    rrr=2
    for rrr in range (2,1000):
        ranges = [shit_name+"!A"+str(rrr)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sss = results['valueRanges'][0]['values']
        if sss==chat_id:
            nnn=rrr
            rrr=rrr+1000
            ranges = [shit_name+"!"+column_name+str(nnn)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            ubit = results['valueRanges'][0]['values']
            ranges = [shit_name+"!"+column_vict+str(nnn)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            new_pray = results['valueRanges'][0]['values']
        else:
            rrr=rrr+1
    hhh=2
    for hhh in range(2,1000):
        ranges = [shit_name+"!"+column_vict+str(hhh)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        jjj = results['valueRanges'][0]['values']
        if jjj==ubit:
            mmm=hhh
            hhh=hhh+1000
            ranges = [shit_name+"!"+column_name+str(mmm)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            svo = results['valueRanges'][0]['values']
        else:
            hhh=hhh+1
    zzz=2
    for zzz in range (2,1000):
        ranges = [shit_name+"!"+column_name+str(zzz)] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        you = results['valueRanges'][0]['values']
        if you == svo:
            ddd = zzz
            zzz = zzz + 1000
            ranges = [shit_name+"!A"+str(ddd)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            killer_id = results['valueRanges'][0]['values']
        else:
            zzz = zzz + 1
    bot.send_message(killer_id, "Успехх! Твоя новая цель - ", new_pray)
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": shit_name+"!"+column_vict+str(mmm),
             "majorDimension": "ROWS",
             "values": [[new_pray],]}]
            }).execute()

def org_gamenametaker(text, chat_id):
    for sheet in sheetlist:
        if title==text:
            bot.send_message(chat_id, "Такая партия уже существует, попробуйте ещё раз")
            break
    else:
        results = service.spreadsheets().batchUpdate(spreadsheetId = fifile, body = {"requests": [{"addSheet": {"properties": {"title": text,"gridProperties": {"rowCount": 1000,"columnCount": 7}}}}]}).execute()
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": shit_name+"!A2",
                         "majorDimension": "ROWS",
                         "values": [['0'+chat_id],]}]
                    }).execute()
        shit_name = text
        status_writer_zero('0'+chat_id, orgreg)
        keyb_org = types.ReplyKeyboardMarkup
        act_1 = types.KeyboardButton('Сколько человек уже зарегистрировалось?')
        act_2 = types.KeyboardButton('Я тоже хочу участвовать в игре')
        act_3 = types.KeyboardButton('Завершить регистрацию')
        keyb_org.add(act_1, act_2, act_3)
        bot.send_message(chat_id, "Игра создана. Чтобы зарегистрироваться, участникам нужно будет ввести её название: " + text, reply_markup=keyb_org)
        return shit_name

def org_startquest(chat_id):
    ranges = [shit_name+"!A2:A1000"] #
    results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    ids = results['valueRanges'][0]['values']
    keyb_org = types.ReplyKeyboardRemove()
    keyb_orgq = types.ReplyKeyboardMarkup()
    act_1 = types.KeyboardButton('Сколько человек уже прошло опрос?')
    act_3 = types.KeyboardButton('Завершить прохождение опросов и начать игру')
    keyb_orgq.add(act_1, act_3)
    bot.send_message(chat_id, "Опрос о знакомых начался", reply_markup=keyb_orgq)
    status_writer('0'+id, 'orgquest') #здесь надо проследить чтобы статусврайтер не переписывал и статул участниковой строки орга если она есть
    for some_id in id:
        part_quest(some_id)

def org_start(chat_id, text):
    if text == 'Сколько человек уже прошло опрос?':
        stats_reg(chat_id)
    elif text == 'Я тоже хочу участвовать в игре':
        rrr=2
        for rrr in range (2,1000):
            ranges = [shit_name+"!"+column_stat+str(rrr)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            sss = results['valueRanges'][0]['values']
            if sss == '':
                nnn = rrr
                rrr = rrr + 1000
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": shit_name+"!A"+str(nnn),
                         "majorDimension": "ROWS",
                         "values": [[chat_id],]}]
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
        separator(shit_id)
        status_writer('0'+chat_id, 'orggame')
        ranges = [shit_name+"!A2:A1000"] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        ids = results['valueRanges'][0]['values']
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
        ranges = [shit_name+"!A2:A1000"] #
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        ids = results['valueRanges'][0]['values']
        rrr = 2
        for rrr in range (2,1000):
            ranges = [shit_name+"!"+column_stat+str(rrr)] #
            results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
            sss = results['valueRanges'][0]['values']
            if sss=='pl':#НУЖНЫ СТАТУС
                wwww=rrr
                ranges = [shit_name+"!"+column_name+str(wwww)] #
                results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
                winner = results['valueRanges'][0]['values']
            rrr=rrr+1
            all_winner = all_winner + winner
        for some_id in ids:
            status_writer(some_id, done)
            bot.send_message(some_id, 'Игра закончена. !! Победитель - ' + all_winner)
        bot.send_message(chat_id, 'Ваша игра завершена. Надеемся, все повеселились. Мы открыты для отзывов и предложений: ')
        thats_all(shit_id)

def roletaker(chat_id, text):
    keyb_first = types.ReplyKeyboardRemove()
    if text == 'Организатор':
        bot.send_message(user_id, "Введите кодовое имя для вашей игры:", reply_markup=keyb_first)
        status_writer(user_id, 'ogamen')
    elif text == 'Участник':
        bot.send_message(chat_id, 'Введи кодовое слово игры, в которой ты участвуешь', reply_markup=keyb_first)
        status_writer(user_id, 'gamen')

@bot.message_handler(content_types=['text'])
def main_body(m):
    user_text = m.text
    user_id = m.chat.id
    if user_text == '\help':
        bot.send_message(user_id, 'бог поможет')
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
    else:
        command_start(user_id)

bot.polling()
