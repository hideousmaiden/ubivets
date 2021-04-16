import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	

CREDENTIALS_FILE = 'cybersep-310108-c1268b1fb570.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 


fifile = '1oQKWSfnal13xLCPpfHqH46ROC9w9RBmIhpA70D8lLKg'

results = service.spreadsheets().batchUpdate(
    spreadsheetId = fifile, #здесь надо будет вставить адрес табличьки, когда она появится
    body = 
{
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": "Лист другой", #админ ж называет листок
          "gridProperties": {
            "rowCount": 1000,
            "columnCount": 7
          }
        }
      }
    }
  ]
}).execute()

results = service.spreadsheets().batchUpdate(
    spreadsheetId = fifile, #здесь надо будет вставить адрес табличьки, когда она появится
    body = 
{
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": "Лист вдруг", #админ ж называет листок
          "gridProperties": {
            "rowCount": 1000,
            "columnCount": 7
          }
        }
      }
    }
  ]
}).execute()

results = service.spreadsheets().batchUpdate(
    spreadsheetId = fifile, #здесь надо будет вставить адрес табличьки, когда она появится
    body = 
{
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": "Лист наверное", #админ ж называет листок
          "gridProperties": {
            "rowCount": 1000,
            "columnCount": 7
          }
        }
      }
    }
  ]
}).execute()

