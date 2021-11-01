import os
import glob
from pathlib import Path
import zipfile
import shutil
import subprocess
import csv

#find . -name "*.java" | xargs -n 10 nkf -w --overwrite

def unzip(input,output,extension):
    my_zip = zipfile.ZipFile(input)
    my_zip.extractall()
    for file in my_zip.namelist():
        if my_zip.getinfo(file).filename.endswith(extension):
            name=file.split('/')[-1]
            name=name.split('\\')[-1]
            shutil.move(file,output+'/'+name)

def delete_file(path):
    for p in path.iterdir():
        if p.is_file():
            p.unlink()
    path.rmdir()

def delete_suffix(path,suffix):
    for p in path.iterdir():
        if p.is_file():
            if p.suffix==suffix:
                p.unlink()
def test_cmd():
    res=[]
    test_cmd=[]
    test_cmd.append(["java","Main"])

    for cmd in test_cmd:
        res.append(subprocess.check_output(cmd))
    return res

def java_test(test_dir):
    res=[]
    files=list(test_dir.iterdir())
    cmd=["javac"]


    file_list=["Deviation","Average","ScoreData","ScoreData","RangeStatistics","RangeStatistics","ScoreData","ScoreData","ScoreData","Deviation","Deviation","Deviation","Average","Average","Average"]
    print(len(file_list))
    ans_list={}
    ans_list[0]='class Deviation implements Statistic '
    ans_list[1]='class Average implements Statistic '
    ans_list[2]='void setStatistic(Statistic'
    ans_list[3]='calcStatistic'
    ans_list[4]='RangeStatistics implements Statisti'
    ans_list[5]='.calc'
    ans_list[6]='math'
    ans_list[7]='english'
    ans_list[8]='software'
    ans_list[9]='"math"'
    ans_list[10]='english'
    ans_list[11]='software'
    ans_list[12]='math'
    ans_list[13]='english'
    ans_list[14]='software'
    Verification={}

    for i,test in enumerate(file_list):
        Verification[i]=False

    for file in files:
        #動くかどうか
        if file.name[0]!='.' and file.suffix=='.java':
            cmd.append(str(file))
            #使用満たすかどうか
            for i,test in enumerate(file_list):
                if (test+'.java').lower() in file.name.lower():
                    with file.open() as f:
                        Verification[i]=(ans_list[i].replace(' ', '').lower() in f.read().replace(' ', '').lower())

    cmd.append("-d")
    cmd.append("./")
    subprocess.run(cmd)
    res=test_cmd()
    print(res)

    return [res,Verification]

def check(dic,ans):
    ans_res,ans_veri=java_test(ans)
    csv_data=[]
    for key, val in dic.items():
        res=val[0]
        veri=val[1]
        row=[]
        row.append(key)
        for i in range(len(res)):
            if res[i]==ans_res[i]:
                row.append(True)
            else:
                row.append(False)
        row.extend(list(veri.values()))
        row.insert(1,sum(row[1:]))
        csv_data.append(row)

    with open('students.csv', 'w', newline='') as student_file:
        writer = csv.writer(student_file)
        for row in csv_data:
            writer.writerow(row)

    return csv_data


if __name__ == '__main__':
    root = Path('./')
    test_dir=Path("./test")
    zips = Path('./zip')
    ans_dir=Path('./ans')
    delete_suffix(root,".class")
    files=list(zips.iterdir())
    syoki=list(root.iterdir())
    if test_dir.exists():
        delete_file(test_dir)
    dic={}
    for file in files:
        if file.suffix=='.zip':
            print(file.stem)
            try:
                test_dir.mkdir(exist_ok=True)
                unzip(str(file),test_dir.name,'java')
                shutil.copyfile("./ans/scores.csv", "./scores.csv")
                #実験
                res=java_test(test_dir)
                dic[file.name]=res
            except Exception as e:
                print(e)
                dic[file.name]=[[False],{1:False}]
            delete_file(test_dir)
            delete_suffix(root,".class")
            delete_suffix(root,".java")

    shutil.copyfile("./ans/scores.csv", "./scores.csv")
    check(dic,ans_dir)
    delete_suffix(root,".class")
    delete_suffix(root,".java")

    end=list(root.iterdir())
    for file in end:
        if not(file in syoki):
            print(file)
            delete_file(file)

