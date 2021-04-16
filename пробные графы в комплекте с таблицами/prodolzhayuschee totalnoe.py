import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'cybersep-310108-c1268b1fb570.json'

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


fifile = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg' #здесь надо будет вставить адрес табличьки, когда она появится


#новы лист под партию
for sheet in sheetlist:
    if title==text:
        
results = service.spreadsheets().batchUpdate(
    spreadsheetId = fifile,
    body =
{
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": "Листок", #админ ж называет листок
          "gridProperties": {
            "rowCount": 1000,
            "columnCount": 7
          }
        }
      }
    }
  ]
}).execute()



#Заголовки
results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range":
    {
    "sheetId": rosheet,
    "startRowIndex": 0,
    "endRowIndex": 1,
    "startColumnIndex": 0,
    "endColumnIndex": 7
    },
         "majorDimension": "ROWS",
         "values": [["ЯБЫ", "Фамилия", "Статус", "Знакомства", "Жертва", "количество жертв", "Статус игры"],]}
    ]
}).execute()


#Статусрайтер

results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile,
body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range":
    {
    "sheetId": rosheet
    "startRowIndex": id+1,
    "endRowIndex": id+2,
    "startColumnIndex": 2,
    "endColumnIndex": 3
    },
         "majorDimension": "ROWS",
         "values": [[status],]}
    ]
}).execute()


#Писатели

#Друг
scid=id+1
ecid=id+2
results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": {
            "sheetId": rosheet,
            "startRowIndex": scid,
            "endRowIndex": ecid,
            "startColumnIndex": 4,
            "endColumnIndex": 5
            }} # ,
         "majorDimension": "ROWS",
         "values": [
                    [text]
                   ]}
    ]
}).execute()


#ЗАГС
rrr=2
for rrr in range (2;1000)
ranges: {
    "sheetId": rosheet,
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
        "sheetId": rosheet,
        "startRowIndex": nnn+1,
        "endRowIndex": nnn+2,
        "startColumnIndex": 0,
        "endColumnIndex": 2
        },
             "majorDimension": "ROWS",
             "values": [[nnn+2, m, "role"],]}
        ]
    }).execute()
rrr=rrr+1



#Читатели

#аидизы
ranges: {
    "sheetId": rosheet,
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


#Коммунизмридеры
rrr=2
kkk=0
for rrr in range (2;1000)
ranges: {
    "sheetId": rosheet,
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
if sss==#НУЖНЫ СТАТУС
    kkk=kkk+1

result=kkk

#проверяем есть ли введённое участником название игры в табличке
for sheet if title==text: rosheet = (sheet['properties']['sheetId'])
else: rosheet = 0 
 

#Доставатель имен списком
ranges: {
    "sheetId": rosheet,
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


НЕТ ЗАПИСЫВАТЕЛЯ АИДИ - А ТАК ЭТО РЕГИСТРАТОР
НЕТ ЧИТАТЕЛЯ ИГР - А ТАК ЭТО НЕ ТАК ДЕЛАЕТСЯ НО МОЖЕМ ПОПРОБОВАТЬ

#Заказчик
ranges: {
    "sheetId": rosheet,
    "startRowIndex": id+1,
    "endRowIndex": id+2,
    "startColumnIndex": 5,
    "endColumnIndex": 6
    } #

results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
pray = results['values']


#Судмедэксперт_1
ranges: {
    "sheetId": rosheet,
    "startRowIndex": id+1,
    "endRowIndex": id+2,
    "startColumnIndex": 2,
    "endColumnIndex": 3
    }
results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
sur=results

ranges: {
    "sheetId": rosheet,
    "startRowIndex": id+1,
    "endRowIndex": id+2,
    "startColumnIndex": 5,
    "endColumnIndex": 6
    }
results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
npp=results

results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range":
        {
            "sheetId": rosheet,
            "startRowIndex": id+1,
            "endRowIndex": id+2,
            "startColumnIndex": 5,
            "endColumnIndex": 6
            },
         "majorDimension": "ROWS",
         "values": [
                    ["-----"],
                   ]}
    ]
}).execute()

                                      #
rrr=2
for rrr in range (2;1000)
ranges: {
    "sheetId": rosheet,
    "startRowIndex": rrr,
    "endRowIndex": rrr+1,
    "startColumnIndex": 5,
    "endColumnIndex": 6
    } #

results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
sss = results['values']
if sss==sur
    kkk=rrr
        } # запомнили убицу
    killer_id=kkk-1
rrr=rrr+1

results = service.spreadsheets().values().batchUpdate(spreadsheetId = fifile, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range":
        {
            "sheetId": rosheet,
            "startRowIndex": kkk,
            "endRowIndex": kkk+1,
            "startColumnIndex": 5,
            "endColumnIndex": 6
            },
         "majorDimension": "ROWS",
         "values": [
                    [npp],
                   ]}
    ]
}).execute()



#Cтатусридер
ranges: {
    "sheetId": rosheet,
    "startRowIndex": id+1,
    "endRowIndex": id+2,
    "startColumnIndex": 3,
    "endColumnIndex": 4
    } #

results = service.spreadsheets().values().batchGet(spreadsheetId = fifile,
                                     ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
user_state = results['values']

#Победитель
rrr=2
for rrr in range (2;1000)
ranges: {
    "sheetId": rosheet,
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
if sss==#НУЖНЫ СТАТУС
    wwww=rrr
    ranges: {
        "sheetId": rosheet,
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
    print (winner)
rrr=rrr+1
