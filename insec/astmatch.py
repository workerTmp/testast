#!/usr/bin/python3
import os
import sys
import pandas as pd
import csv
import shutil
def check_env(end_file,folder_name):

    file_name="noname"
    for file in os.listdir(folder_name):
        if file.endswith(end_file):
            file_name=file
    if file_name == "noname":
        print(end_file+" file not found")
        sys.exit()
    file_name=os.path.splitext(file_name)[0]
    return file_name

def down_git(lname,pname,rname):
    foldname = "retdec"
    if os.path.exists(foldname):
        shutil.rmtree(foldname)
    if pname == "nonono":
        os.system("git clone https://github.com/"+lname+"/"+rname+".git "+foldname)
    else:
        os.system("git clone https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git "+foldname)


def gogo_ast(lname,pname,rname,fstart):
    foldname = "retdec"
    file_csv = "ex.csv"
    file_out_csv = "exout.csv"
    file_start = fstart #"/opt/a4.out"
    if os.path.exists(file_csv):
        os.remove(file_csv)
    if os.path.exists(file_out_csv):
        os.remove(file_out_csv)
    if "afun" in file_start:
        os.system("echo \"func_;_param_;_colum_start_;_colum_end_;_count_arg_;_src_path\" >> "+file_csv)
    elif "acall" in file_start:    
        os.system("echo \"func_;_param_;_colum_num_;_count_arg_;_src_path\" >> "+file_csv)
    else:
        os.system("echo \"func_;_param_;_colum_start_;_colum_end_;_src_path\" >> "+file_csv)
    for path, subdirs, files in os.walk(foldname):
        for name in files:
            print(os.path.join(path, name))
            os.system(file_start+" "+os.path.join(path, name))
    df = pd.read_csv(file_csv,sep='_;_')
    datanow = len(df['func'].unique())
    arr = []
    for funcname in df['func'].unique():
        all_count = len(df[df['func'].isin([funcname])])
        df1 = df.loc[df['func'].isin([funcname])]
        for paramname in df1['param'].unique():
            arrow = []
            param_count = len(df1[df1['param'].isin([paramname])])
            arrow.append(all_count)
            arrow.append(param_count)
            arrow.append(funcname)
            if ">" in funcname:
                funcname=funcname.replace(">","))")
            if "<" in funcname:
                funcname=funcname.replace("<","((")    
            arrow.append(paramname)
            arrow.append(int(100*param_count/all_count))
            arr.append(arrow)
    print(arr)
    arr = sorted(arr, key=lambda x: (x[0],x[2],x[1]), reverse=True)
    with open(file_out_csv,"w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=';')
        csvWriter.writerows(arr)

def csv_7z(lname,rname,upname,opath):        
    file7z = lname+"_"+rname + ".7z"  
    cmdzip="7z a -mhe=on "+file7z+" *.csv -p"+upname
    os.system(cmdzip)
    shutil.move(file7z, opath+file7z)


def save_repo(lname,pname,rname,ptout):
    os.system("git remote remove origin")
    os.system("git config --global user.name \""+lname+"\"")
    os.system("git config --global user.email "+lname+"@github.com")
    os.system("git remote add -f origin https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git")
    os.system("git checkout master")
    os.system("git add "+ptout)
    os.system("git commit -m \"create 7z\"")
    os.system("git push origin master")


try:
    path_to_in = sys.argv[1]
    path_to_insec = sys.argv[2]
    path_to_out = sys.argv[3]
except IndexError:
    print("Usage: path/in path/insec path/to/out")
    sys.exit(1)


print("check env")    
unzip_name=check_env(".unzip",path_to_insec)
retpo_name=check_env(".repo",path_to_insec)
logi_name=check_env(".login",path_to_insec)
pass_name=check_env(".pass",path_to_insec)
#fretpo_name=check_env(".frepo",path_to_in)
flogi_name=check_env(".flogin",path_to_insec)
fpass_name=check_env(".fpass",path_to_insec)


if os.path.exists(path_to_in+"list.astmatch"):
    with open(path_to_in+"list.astmatch") as f:
        content = f.readlines()
    print(content)
    for i in content:
        rname = i.split('/')[-1].split(".git")[0]
        lname = i.split('/')[-2]
        if lname== flogi_name:
            pname = fpass_name
        else:
            pname="nonono"
        
        down_git(lname,pname,rname)        
        gogo_ast(lname,pname,rname,"/opt/acall.out")
        shutil.move("ex.csv", "ex_call_raw.csv")
        shutil.move("exout.csv", "exout_call_raw.csv")
        gogo_ast(lname,pname,rname,"/opt/afun.out")
        shutil.move("ex.csv", "ex_fun_raw.csv")
        shutil.move("exout.csv", "exout_fun_raw.csv")
        gogo_ast(lname,pname,rname,"/opt/afor.out")
        shutil.move("ex.csv", "ex_for_raw.csv")
        shutil.move("exout.csv", "exout_for_raw.csv")
        gogo_ast(lname,pname,rname,"/opt/aif.out")
        shutil.move("ex.csv", "ex_if_raw.csv")
        shutil.move("exout.csv", "exout_if_raw.csv")
        gogo_ast(lname,pname,rname,"/opt/awhile.out")
        shutil.move("ex.csv", "ex_while_raw.csv")
        shutil.move("exout.csv", "exout_while_raw.csv")
        
        csv_7z(lname,rname,unzip_name,path_to_out)        
        save_repo(logi_name,pass_name,retpo_name,path_to_out)
else:
    print("NO LIST.ASTMAT FILE")
    sys.exit()
