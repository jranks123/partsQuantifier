import csv
from fileutils import writeResults
from itemlist import ItemList
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from googleapiclient.discovery import build
import sys
from utils import getItemListRawFromFile, checkItemListIsValid


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
        'input_file_name': "csv_files/theoreticalstock.csv"
        , 'output_file_name': "byItemNumber_TheoreticalStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - theoretical stock"
        , 'output_sheet_name': "Assembly and purchasing theoretical output"
    }
    , {
        'input_file_name': "csv_files/actualusablestock.csv"
        , 'output_file_name': "byItemNumber_ActualUsableStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - Actualusablestock"
        , 'output_sheet_name': "Assembly and purchasing actual usable output"
    }
    , {
        'input_file_name': "csv_files/onsitestock.csv"
        , 'output_file_name': "byItemNumber_OnsiteStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - onsite stock"
        , 'output_sheet_name': "Assembly and purchasing full onsite output"
    }
]

for file in files:
    itemListRaw = getItemListRawFromFile(worksheet, file['input_file_name'], file['input_sheet_name'])
    itemListRaw.pop(0)

    if (checkItemListIsValid(itemListRaw) == False):
        print("There was a problem with the data in " + file['input_sheet_name'] + ". Please fix the error before continuing")
    else:
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
