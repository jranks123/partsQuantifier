import csv

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
