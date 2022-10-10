import csv

def writeResults(path, header, results):
    f = open(path, 'w')
    writer = csv.writer(f)
    writer.writerow(header)
    for row in results:
        writer.writerow(row)
    f.close()

def writeQuantityByItemNumber(partsList):
    path = ('./results/byItemNumber.csv')
    header = ['item number', 'sprint part number', 'item quantity to build parent', 'item quantity for whole pod']
    rows = []
    for part in partsList.parts:
        row = [
            part.itemNumber
            , part.springPartNumber
            , part.itemQuantityToBuildParent
            , part.itemQuantityToBuildPod]
        rows.append(row)
    writeResults(path, header, rows)

def writeQuantityByPartNumber(quantityByPartNumber):
    path = ('./results/byPart.csv')
    header = ["sprint part number", "part quantity for whole pod"]
    writeResults(path, header, quantityByPartNumber)
