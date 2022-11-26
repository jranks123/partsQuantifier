import csv
from fileutils import writeResults
from itemlist import ItemList
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from googleapiclient.discovery import build
import sys

def getItemListRawFromFile(worksheet, file_name, sheet_name):
    sheet = worksheet.worksheet(sheet_name)

    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(sheet.get_all_values())
        f.close()


    with open(file_name) as f:
        reader = csv.reader(f)
        itemListRaw = list(reader)
        f.close()

    return itemListRaw


totalNumberOfPods = 151


#pathToCreds = ['/Users/jonathanrankin/Downloads/parts-quantifier-c6b9beaaf2f2.json']
pathToCreds = sys.argv[1]

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(pathToCreds, scope)

# authorize the clientsheet
client = gspread.authorize(creds)


API = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '1s2TVptNPS9yYETtg8L0HAk905gNt1h4_88JzZR4LlMg'
worksheet = client.open('SPRING BOM - ISS02')

files = [
    {
        'input_file_name': "theoreticalstock.csv"
        , 'output_file_name': "byItemNumber_TheoreticalStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - theoretical stock"
        , 'output_sheet_name': "Assembly and purchasing onsite output"
    }
    , {
        'input_file_name': "actualusablestock.csv"
        , 'output_file_name': "byItemNumber_ActualUsableStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - Actualusablestock"
        , 'output_sheet_name': "Assembly and purchasing actual usable output"
    }
    , {
        'input_file_name': "onsitestock.csv"
        , 'output_file_name': "byItemNumber_OnsiteStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - onsite stock"
        , 'output_sheet_name': "Assembly and purchasing full theoretical output"
    }
]

for file in files:
    itemListRaw = getItemListRawFromFile(worksheet, file['input_file_name'], file['input_sheet_name'])
    itemListRaw.pop(0)
    itemList = ItemList(itemListRaw)

    duplicateItem = itemList.getDuplicateItem()
    if (duplicateItem):
        print("Duplicate found in sheet " + file.input_sheet_name + ": " + duplicateItem.itemNumber)
    else:
        itemList.calculateStockCollumns(itemList.rootItems)
        itemList.calculateFinalCollumns(itemList.rootItems, totalNumberOfPods)
        itemList.saveToFile(file['output_file_name'])
        itemList.writeToGsheet(API, file['output_file_name'], file['output_sheet_name'], SPREADSHEET_ID)
        #itemList.springPartsList.saveToFile()
