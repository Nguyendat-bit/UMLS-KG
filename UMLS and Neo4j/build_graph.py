from genericpath import exists
import pymysql, csv
from argparse import ArgumentParser
import sys

if __name__ == '__main__':
    parser= ArgumentParser()
    parser.add_argument('--host', default= 'localhost', type= str)
    parser.add_argument('--user', default= 'root', type= str, required= True)
    parser.add_argument('--password', default= 'root', type= str, required= True)
    parser.add_argument('--database', required= True, type= str, default= 'umls2022')
    
    try:
        args= parser.parse_args() 
    except:
        parser.print_help()
        sys.exit(0)
    
    print('Connect Database')
    conn = pymysql.connect(host= args.host, user= args.user,
                            password= args.password, database= args.database)
    cursor= conn.cursor()

    print('Process Concepts')
    exists_concept= set()
    out= open('MRCONSO.processed.csv', 'w', encoding= 'utf-8')
    writer= csv.writer(out)
    cols= ['CUI:ID', ':LABEL',  'name']
    writer.writerow(cols)
    cursor.execute("select * from mrconso")
    mrconso= cursor.fetchall()
    for line in mrconso: 
        if line[0] in exists_concept: 
            continue
        if line[1] == 'ENG':
            writer.writerow([line[0], 'Concept', line[-4]])
            exists_concept.add(line[0])
    print(f'{len(exists_concept)} concepts')

    print('Process Atoms')
    out= open('MRAUI.processed.csv', 'w', encoding= 'utf-8')
    writer= csv.writer(out)
    cols= ['AUI:ID', ':LABEL', 'name', 'CUI']
    writer.writerow(cols)
    exists_atom= set()
    with open('MRCONSO.RRF', mode= 'r', encoding='utf-8') as f : 
        for line in mrconso: 
            if line[7] in exists_atom: 
                continue
            if line[2] == 'ENG':
                writer.writerow([line[7], 'Atom', line[-4], line[0]])
                exists_atom.add(line[7])
    out.close()
    print(f'{len(exists_atom)} atoms')

    print('Process relationships')

    cui_aui = exists_atom | exists_concept
    cursor.execute("select * from mrrel")
    mrrel= cursor.fetchall() 

    out= open('MRREL.processed.csv', 'w', encoding= 'utf-8')
    writer= csv.writer(out)
    cols= [':START_ID', ':END_ID',':TYPE','RELA']
    writer.writerow(cols)
    count= 0
    with open('MRREL.RRF', mode= 'r', encoding= 'utf-8') as f: 
        for line in mrrel:
            start_node= line[4]
            end_node= line[0]
            if line[6]== 'AUI': # style 2
                start_node= line[5]
            if line[2]== 'AUI': # syle 1
                end_node= line[1]
            if start_node in cui_aui and end_node in cui_aui: 
                writer.writerow([start_node, end_node, line[3], line[7]])
            count += 1
    out.close()
    print(f"{count} relationships")