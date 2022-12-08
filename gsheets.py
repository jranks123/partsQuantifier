from googleapiclient.discovery import build


def find_sheet_id_by_name(API, sheet_name, SPREADSHEET_ID):
    # ugly, but works
    sheets_with_properties = API \
        .spreadsheets() \
        .get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties') \
        .execute() \
        .get('sheets')

    for sheet in sheets_with_properties:
        if 'title' in sheet['properties'].keys():
            if sheet['properties']['title'] == sheet_name:
                return sheet['properties']['sheetId']


def writeToGsheet(API, path, sheetName, SPREADSHEET_ID):
    path = ('./csv_files/' + path)
    sheet_id = find_sheet_id_by_name(API, sheetName, SPREADSHEET_ID)
    if(sheet_id):
        res = push_csv_to_gsheet(
            csv_path=path
            , sheet_id=sheet_id
            , SPREADSHEET_ID = SPREADSHEET_ID
            , API = API
            , sheetName = sheetName
        )
        if(res['spreadsheetId']):
            print("Successfully wrote results to " +  sheetName)
    else:
        print('Could not find sheet: ' + sheetName)


def push_csv_to_gsheet(csv_path, sheet_id, SPREADSHEET_ID, API, sheetName):
    with open(csv_path, 'r', newline='') as csv_file:
        csvContents = csv_file.read()
    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": sheet_id,
                    "rowIndex": "0",  # adapt this if you need different positioning
                    "columnIndex": "0", # adapt this if you need different positioning
                },
                "data": csvContents,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }

    # write results to sheet
    request = API.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body)
    response = request.execute()
    return response
