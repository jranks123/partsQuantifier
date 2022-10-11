import csv
from fileutils import writeResults
from itemlist import ItemList


with open('data.csv') as f:
    reader = csv.reader(f)
    itemListRaw = list(reader)
    f.close()

itemListRaw.pop(0)
itemList = ItemList(itemListRaw)

duplicateItem = itemList.getDuplicateItem()
if (duplicateItem):
    print("Duplicate found: " + duplicateItem.itemNumber)
else:
    itemList.calculateStockCollumnsPartOne(itemList.rootItems)
    itemList.setItemsWithSamePartNumber()
    itemList.calculateStockCollumnsPartTwo(itemList.rootItems)
    itemList.saveToFile()
    itemList.springPartsList.saveToFile()
