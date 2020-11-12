import csv

def load_name(filename):
    idx_val = dict()
    f = open(filename, 'r', encoding='utf-8')

    # f = open('./category.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        idx_val[line[0]] = line[1]
    f.close()   
    
    return idx_val
