import os
import glob
from pathlib import Path
import zipfile
import shutil
import subprocess
import csv
import re

if __name__ == '__main__':
    table_file="table.csv"
    res_file="week3/students.csv"
    final_file="week3.csv"
    table=[]
    res={}
    with open(table_file) as f:
        reader = csv.reader(f)
        for row in reader:
            table.append(row)

            
    with open(res_file) as f:
        reader = csv.reader(f)
        for row in reader:
            if None != re.search('\d{6}',row[0]):
                row[0]=re.search('\d{6}',row[0]).group(0)
                res[row[0]]=row[1:]
            else:
                print("not found")
                print(row[0])

    final=[]
    for b in table:
        if b[1] in res:
            final.append([b[0]]+res[b[1]])
        else:
            final.append([b[0],"-"])

    with open(final_file, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(final)
