import csv

def getItemListRawFromFile(worksheet, file_name, sheet_name):
    sheet = worksheet.worksheet(sheet_name)

    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sheet.get_all_values())
        f.close()

    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        itemListRaw = list(reader)
        f.close()

    return itemListRaw

def checkItemIsValid(rawItem):
    if(not rawItem[0] or len(rawItem[0]) == 0):
        print("Error: There was an item without an itemNumber")
        return False
    elif (not rawItem[1] or len(rawItem[1]) == 0):
        print("Error: Item " +  rawItem[0] + " has no sprint part number")
        return False
    elif (not rawItem[2] or len(rawItem[2]) == 0):
        print("Error: Item " +  rawItem[0] + " has no itemQuantityToBuildParent")
        return False
    elif (not rawItem[3].isnumeric()):
        print("Error: The value of stock, " + rawItem[3] + " for Item " +  rawItem[0] + " is not a numeric value ")
        return False
    elif (not rawItem[3] or len(rawItem[3]) == 0):
        print("Error: Item " +  rawItem[0] + " has no stock set")
        return False
    elif (not rawItem[4] or len(rawItem[4]) ==0):
        print("Error: Item " +  rawItem[0] + " has no type set")
        return False
    else:
        return True

def checkItemListIsValid(itemListRaw):
    for item in itemListRaw:
        if(not checkItemIsValid(item)):
            return False
    return True
