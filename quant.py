import csv
from fileutils import writeResults
from itemlist import ItemList


with open('data.csv') as f:
    reader = csv.reader(f)
    itemListRaw = list(reader)
    f.close()

totalNumberOfPods = 151

itemListRaw.pop(0)
itemList = ItemList(itemListRaw)

duplicateItem = itemList.getDuplicateItem()
if (duplicateItem):
    print("Duplicate found: " + duplicateItem.itemNumber)
else:
    itemList.calculateStockCollumns(itemList.rootItems)
    itemList.calculateFinalCollumns(itemList.rootItems, totalNumberOfPods)
    itemList.saveToFile()
    itemList.springPartsList.saveToFile()
