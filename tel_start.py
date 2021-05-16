import telebot as tb
import networkx as nx
from telebot import types
import time
import httplib2
import gspread
import random
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
CREDENTIALS_FILE = 'cybersep-310108-c1268b1fb570.json'
shit_name = '0'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
fifile = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg'
spreadsheet = service.spreadsheets().get(spreadsheetId = fifile).execute()
sheetlist = spreadsheet.get('sheets')

token = '1555845859:AAFT12GCr7l-vK8S67KGtqUAyOVM7_hl7Vc'
bot = tb.TeleBot(token, parse_mode=None)

def great_check(id):
    records_data = getallvalues_wait()
    for line in records_data:
        if line[0] == str(id):
            return line[1]

def part_gamenametaker(text, chat_id):
    results = batchget_wait('A1:C')
    names = results['valueRanges'][0]['values']
    games = {k[2] for k in names if len(k) != 0}
    if text not in games:
        bot.send_message(chat_id, "Такой текущей партии нет, попробуй ещё раз")
    else:
        part_stats = {k[1] for k in names if k[2] == text}
        if 'orgreg' in part_stats:
            records_data = getallvalues_wait()
            for n in range(len(records_data)):
                if records_data[n][0] == str(chat_id):
                    records_data[n][2] = text
                    break
            results = batchupdate_wait('C' + str(n + 1), [[text],])
            status_writer(chat_id, 'partn')
            bot.send_message(chat_id, "Введи своё имя и фамилию: ")
        else:
            bot.send_message(chat_id, "Регистрация на эту игру уже закончилась, попробуй снова")

def append_wait(ranges, values):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    try:
        result = service.spreadsheets().values().append(spreadsheetId='1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', range= 'A1:C', valueInputOption='USER_ENTERED', body = {
                "range": ranges,
                 "values": values}).execute()
    except:
        time.sleep(60)
        append_wait(ranges, values)

def getallvalues_wait():
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    try:
        sheet_instance = sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_values()
        return records_data
    except:
        time.sleep(60)
        return getallvalues_wait()

def batchupdate_wait(ranges, values):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    try:
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg', body = {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": ranges, "values": values}]}).execute()
    except:
        time.sleep(60)
        batchupdate_wait(ranges, values)

def batchget_wait(ranges):
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    try:
        results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
        return results
    except:
        time.sleep(60)
        return batchget_wait(ranges)

def separator(id):
    records_data = getallvalues_wait()
    edges = []
    isolat = []
    records_data = getallvalues_wait()
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

    final_cycles = []
    weighted_edges = []
    mutual_edges = []
    finals = []
    raw_graph = nx.DiGraph()
    raw_graph.add_edges_from(edges)
    raw_graph.add_nodes_from(isolat)
    nodes = raw_graph.nodes
    edges = []
    norm_nodes = []
    for x in nodes:
        norm_nodes.append(x)
    for x in raw_graph.edges:
        edges.append(x)
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

    for n in range(len(records_data)):
        for num in range(len(best_cycle)):
            if records_data[n][3] == best_cycle[num] and num != (len(best_cycle) - 1):
                records_data[n][5] = best_cycle[num + 1]
                break
            elif records_data[n][3] == best_cycle[num] and num == (len(best_cycle) - 1):
                records_data[n][5] = best_cycle[0]
                break
    results =  batchupdate_wait('A1:F', records_data)

def status_writer(id, status):
    records_data = getallvalues_wait()
    for n in range(len(records_data)):
        if records_data[n][0] == str(id):
            records_data[n][1] = status
            break
    results = batchupdate_wait('B' + str(n + 1), [[status], ])

def add_friend(chat_id, text):
    records_data = getallvalues_wait()
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            records_data[n][4] += ';'
            records_data[n][4] += text
            break
    results = batchupdate_wait('E' + str(n + 1), [[records_data[n][4]], ])
 #   presence = False
  #  while presence == False:
   #     time.sleep(5)
   #     records_data = batchget_wait('E' + str(n + 1))
    #    friends = records_data['valueRanges'][0]['values'][0][0]
     #   if text in friends.split(';'):
      #      presence = True
      #  else:
     #       friends += ';'
      #      friends += text
       #     results = batchupdate_wait('E' + str(n + 1), [[friends], ])

def stats_reg(chat_id):
    result = 0
    records_data = getallvalues_wait()
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
    records_data = getallvalues_wait()
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
    records_data = getallvalues_wait()
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
    records_data = getallvalues_wait()
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
        if l[1] == 'pl' and l[2] == game_name:
            bot.send_message(l[0], "Новостная сводка!!\nВышло из игры " + str(result_kl) + " человек, а ещё играет " + str(result_pl) + ' человек.\nБудьте осторожны в пустынных коридорах!')

def command_start(id):
    append_wait('A1:C', [[id, 'role', '-'],])
    keyb_first = types.ReplyKeyboardMarkup()
    for el in ['Организатор', 'Участник']:
        keyb_first.add(types.KeyboardButton(el))
    bot.send_message(id, "Привет!\nВыбери свою роль:", reply_markup=keyb_first)

def part_nametaker(text, chat_id):
    results = batchget_wait('D1:D')
    names = results['valueRanges'][0]['values']
    part_names = {k[0] for k in names if len(k) != 0}
    if text in part_names:
        bot.send_message(chat_id, "Это имя уже занято, попробуй ещё раз")
    else:
        records_data = getallvalues_wait()
        for n in range(len(records_data)):
            if records_data[n][0] == str(chat_id):
                records_data[n][3] = text
                break
        results = batchupdate_wait('D' + str(n + 1), [[text],])
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
    records_data = getallvalues_wait()
    for line in records_data:
        if line[0] == str(some_id):
            prey = line[5]
            break
    status_writer(some_id, 'pl')
    bot.send_message(some_id, u"""Игра началась!""")
    bot.send_photo(some_id, open('telebot_4.jpg', 'rb'))
    bot.send_message(some_id, """Сейчас твоя задача - застать свою жертву наедине без свидетелей и сказать ей ***Тебя поймали***.\nПосле этого пойманный тобой человек должен при тебе ___написать боту___ со своего устройства ***меня нашли***, и тебе придёт имя новой жертвы. Остерегайся, ведь не только ты сегодня охотишься!\nТвоя первая цель - """ + prey, parse_mode='Markdown')

def part_killed(chat_id):
    status_writer(chat_id, 'done')
    bot.send_photo(chat_id, open('telebot_2.jpg', 'rb'))
    bot.send_message(chat_id, "Ты выбыл_а из игры, эта погоня была легендарной. Когда игра закончится, ты узнаешь имена победителей")
    records_data = getallvalues_wait()
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
        if line[2] == game_name and line[1] == 'pl':
            doomed_counter += 1
    if doomed_counter == 2:
        for line in records_data:
            if line[1] == 'orggame' and line[2] == game_name:
                org_id = line[0]
                break
        results = batchupdate_wait('A1:F', records_data)
        thats_all(org_id)
    else:
        pic = random.choice(['telebot_3.jpg', 'telebot_5.jpg', 'telebot_6.jpg'])
        bot.send_photo(chat_id, open(pic, 'rb'))
        bot.send_message(killer_id, "Успехх! Твоя новая цель - " + victim_name)
        results = batchupdate_wait('A1:F', records_data)

def org_gamenametaker(text, chat_id):
    results = batchget_wait('C1:C')
    names = results['valueRanges'][0]['values']
    games = {k[0] for k in names if len(k) != 0}
    if text in games:
        bot.send_message(chat_id, "Такая партия уже существует, попробуйте ещё раз")
    else:
        records_data = getallvalues_wait()
        for n in range(len(records_data)):
            if records_data[n][0] == str(chat_id):
                records_data[n][2] = text
                break
        results = batchupdate_wait('C' + str(n + 1), [[text], ])
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
    records_data = getallvalues_wait()
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
        records_data = getallvalues_wait()
        for n in range(len(records_data)):
            if records_data[n][0] == str(chat_id):
                game_name = records_data[n][2]
                break
        ids = {records_data[p][0] for p in range(len(records_data)) if records_data[p][2] == game_name and records_data[p][1] in ['questd', 'quest']}
        for some_id in ids:
            part_startgame(some_id)
        keyb_orgp = types.ReplyKeyboardMarkup()
        for act in ['Статистика', 'Разослать новости', 'Принудительно завершить игру']: keyb_orgp.add(types.KeyboardButton(act))
        bot.send_message(chat_id, 'Вы успешно начали игру', reply_markup=keyb_orgp)

def thats_all(chat_id):
    new_table = []
    records_data = getallvalues_wait()
    winners = []
    client = gspread.authorize(credentials)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    sheet = client.open('Табличька')
    sheet_instance = sheet.get_worksheet(0)
    for n in range(len(records_data)):
        if records_data[n][0] == str(chat_id):
            game_name = records_data[n][2]
            break
    for n in range(len(records_data)):
        if records_data[n][2] == game_name:
            key_fin = types.ReplyKeyboardRemove()
            bot.send_message(records_data[n][0], 'Игра закончилась!!\nНадеемся, вам понравилось. Мы открыты для отзывов и предложений: cyparaber@gmail.com', reply_markup = key_fin)
            if records_data[n][1] == 'pl':
                winners.append(records_data[n][3])
        else:
            new_table.append(records_data[n])
    for line in records_data:
        if line[2] == game_name:
            bot.send_message(line[0], 'Вот они победители слева направо: ' + ', '.join(winners) + '!')
            bot.send_photo(line[0], open('telebot_7.jpg', 'rb'))
    sheet_instance.clear()
    results = batchupdate_wait('A1:F', new_table)

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
        bot.send_photo(chat_id, open('telebot_1.jpg', 'rb'))
        bot.send_message(chat_id, "Введите кодовое имя для вашей игры:", reply_markup=keyb_first)
        status_writer(chat_id, 'ogamen')
    elif text == 'Участник':
        bot.send_photo(chat_id, open('telebot_1.jpg', 'rb'))
        bot.send_message(chat_id, 'Введи кодовое слово игры, в которой ты участвуешь', reply_markup=keyb_first)
        status_writer(chat_id, 'gamen')

def gamereader(id):
    records_data = getallvalues_wait()
    for line in records_data:
        if line[0] == str(id):
            return line[2]

@bot.message_handler(content_types=['photo'])
def photo_sender(m):
    file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = "/home/cyparaber/ubivets/" + file_info.file_path
    with open(src, "wb") as new_file:
        new_file.write(downloaded_file)
    user_id = m.chat.id
    for i in [834879398, 633285518, 12652859078]:
        if user_id != i:
            bot.send_photo(i, open(scr, "rb"))

@bot.message_handler(content_types=['text'])
def main_body(m):
    user_text = m.text
    user_id = m.chat.id
    if user_text == '/help':
        bot.send_message(user_id, u'''Если вы хотите присоединиться к игре в качестве участника, отправьте сообщение ***/start***, затем выберите опцию ***Участник*** и введите название партии, к которой хотите присоединиться.\nЗарегистрируйтесь под тем именем, под которым вас знают остальные играющие. Когда регистрация завершится (все желающие войдут в игру), вам будет предложено выбрать имена тех людей, с кем вы знакомы. Это произойдет через некоторое время после того, как зарегистрируетесь
        лично вы.\nПосле того, как вы выберете всех знакомых вам людей из предложенного списка, нажмите ***Готово!***.\nЕсли вам пришло сообщение о начале опроса о знакомых, но список не отображается, нажмите на значок с четырьмя квадратами внутри в верхней части клавиатуры (в той, где отображается набираемый текст) справа.\nЕсли вы все сделали правильно, позже вам придет имя вашей жертвы – человека, которого вы должны поймать без свидетелей и оповестить о том, что вы – его убийца. Это
        произойдет после того, как все участники отметят своих знакомых.\n
        Если вас убили, отправьте сообщение ***меня нашли*** прямо после убийства.\n
        Если вы убили, проверьте, что жертва отправила боту сообщение ***меня нашли*** со своего аккаунта. Затем вам придет сообщение с именем вашей новой жертвы.\n
        Если во время убийства появились свидетели, убийство считается несостоявшимся.\n
        Когда в живых останутся лишь два человека, игра закончится и вам придет сообщение с именами победителей.\n
        Игра может закончиться досрочно – тогда, когда ее решит завершить организатор – в этом случае победителями будут считаться все, кто не умер к этому моменту.\n\n
        Если вы хотите начать новую игру в качестве организатора, отправьте сообщение ***/start***, затем выберите опцию ***Организатор*** и введите название вашей партии. Регистрация участников начнется автоматически.\n
        Вы можете посмотреть, сколько человек уже зарегистрировалось. Для этого отправьте боту сообщение ***Сколько человек уже зарегистрировалось?***\n
        После того, как вы решите, что зарегистрировались все желающие, отправьте сообщение ***Завершить регистрацию***. После этого автоматически начнется опрос всех участников об их знакомствах. Новые участники присоединиться уже не смогут.\n
        Вы можете в любой момент посмотреть, сколько человек уже прошло опрос. Для этого отправьте сообщение ***Сколько человек уже прошло опрос?***\n
        После того, как вы решите, что все участники прошли опрос о знакомствах, отправьте боту сообщение ***Завершить прохождение опросов и начать игру***. После этого каждому участнику автоматически отправится имя его первой жертвы. Проходить опросы участники больше не смогут.\n
        В любой момент вы можете посмотреть, сколько человек убито. Для этого отправьте сообщение ***Статистика***\n
        Вы можете рассылать новости всем участникам о том, как проходит игра. Для этого отправьте сообщение ***Разослать новости***\n
        Игра завершится автоматически, когда в живых останется ровно два участника. Они будут объявлены победителями, всем придет оповещение о конце партии\n
        Вы можете в любой момент досрочно завершить игру. В этом случае победителями будут объявлены все, кто остался в живых до этого времени. После завершения игры возобновить ее будет нельзя. Для завершения отправьте сообщение ***Принудительно завершить игру***\n
        Если у вас остались вопросы, на которые вы не нашли ответа в сообщениях бота, у организатора или в этом гайде, напишите нам на почту ___cyparaber@gmail.com___. На эту же почту можно отправить все ваши пожелания, предложения и негодования о нашем боте, мы будем им очень рады.\n
        Приятной игры (и пусть победит хитрейший)!''', parse_mode = "Markdown")
    elif user_id == 1265285907 or user_id == 834879398:
        bot.send_message(633285518, user_text, parse_mode = "Markdown")
    elif user_id == 633285518:
        bot.send_message(12652859078, user_text, parse_mode = "Markdown")
        bot.send_message(834879398, user_text, parse_mode = "Markdown")            
    elif user_text == '/backstage':
        bot.send_message(user_id, 'Наш бот разработан на языке программирования Python. Всю информацию об участниках он хранит в Google-таблице, ссылку на которую мы можем предоставить, если вы обратитесь к нам на почту.\nНаш бот определяет жертву для каждого игрока с помощью графа, построенного на основе информации о знакомствах каждого. Все участники связаны единым циклом, в котором соседи не знают друг друга и имеют как можно меньшее количество общих знакомых. Каждые правый сосед является жертвой левому. После того, как человека убили, его киллеру достается та жертва, которую убитый не успел найти. Игра продолжается до момента, когда в живых останется ровно два человека (в этот момент они будут являться жертвами друг друга), или до принудительного завершения игры организатором. По всем дополнительным вопросам можно обращаться к нам на почту cyparaber@gmail.com . Удачной игры!', parse_mode = "Markdown")
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
