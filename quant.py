import csv
from fileutils import writeResults
from itemlist import ItemList
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from googleapiclient.discovery import build
import sys
from utils import getItemListRawFromFile, checkItemListIsValid
from gsheets import writeToGsheet


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
        , 'output_sheet_name': "Assembly and purchasing full theoretical output"
        , 'spring_part_output_file_name': None
        , 'spring_part_output_sheet_name': None
    }
    , {
        'input_file_name': "csv_files/actualusablestock.csv"
        , 'output_file_name': "byItemNumber_ActualUsableStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - Actualusablestock"
        , 'output_sheet_name': "Assembly and purchasing actual usable output"
        , 'spring_part_output_file_name': None
        , 'spring_part_output_sheet_name': None
    }
    , {
        'input_file_name': "csv_files/onsitestock.csv"
        , 'output_file_name': "byItemNumber_OnsiteStock.csv"
        , 'input_sheet_name': "Assembly & purchasing BOM DATA - onsite stock"
        , 'output_sheet_name': "Assembly and purchasing onsite output"
        , 'spring_part_output_file_name': None
        , 'spring_part_output_sheet_name': None
    }

    , {
        'input_file_name': "csv_files/fullBom.csv"
        , 'output_file_name': "byItemNumber_fullBom.csv"
        , 'input_sheet_name': "BOM full engineering input data"
        , 'output_sheet_name': "BOM full engineering output data"
        , 'spring_part_output_file_name': "bySpringPartNumber_fullBom.csv"
        , 'spring_part_output_sheet_name': "BOM full engineering SpringPart output"
    }
]

for file in files:
    itemListRaw = getItemListRawFromFile(worksheet, file['input_file_name'], file['input_sheet_name'])
    itemListRaw.pop(0)

    print("\nChecking input for " + file['input_sheet_name'])
    if (checkItemListIsValid(itemListRaw) == False):
        print("There was a problem with the input data for this sheet. Skipping to next sheet \n")
    else:
        print("Check complete\n")
        itemList = ItemList(itemListRaw)
        duplicateItem = itemList.getDuplicateItem()
        if (duplicateItem):
            print("Duplicate found in sheet " + file.input_sheet_name + ": " + duplicateItem.itemNumber)
        else:
            itemList.calculateStockCollumns(itemList.rootItems)
            itemList.calculateFinalCollumns(itemList.rootItems, totalNumberOfPods)
            itemList.saveToFile(file['output_file_name'])
            writeToGsheet(API, file['output_file_name'], file['output_sheet_name'], SPREADSHEET_ID, worksheet)
            if (file['spring_part_output_file_name'] and file['spring_part_output_sheet_name']):
                itemList.springPartsList.saveToFile(file['spring_part_output_file_name'])
                writeToGsheet(API, file['spring_part_output_file_name'], file['spring_part_output_sheet_name'], SPREADSHEET_ID, worksheet)
