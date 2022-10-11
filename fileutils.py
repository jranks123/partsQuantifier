import csv

def writeResults(path, header, results):
    f = open(path, 'w')
    writer = csv.writer(f)
    writer.writerow(header)
    for row in results:
        writer.writerow(row)
    f.close()
