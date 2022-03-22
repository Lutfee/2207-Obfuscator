# importing tkinter and tkinter.ttk
# and all their functions and classes
import os
import random
import re
import subprocess
import time
from subprocess import Popen, PIPE
from pathlib import Path
from tkinter import *
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
from tkinter.ttk import *

# ----------- Global Var -----------
content = ""
file_name = ""
file_path = ""
main_smali_file_path = ""

window = Tk()
window.title("Simple Obfuscator")
window.geometry('480x300')
window.config(background="light blue")


# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    global content
    global file_name
    global file_path

    file = askopenfile(mode='r')
    progress["value"] += 20
    window.update_idletasks()
    file_name = os.path.basename(file.name)
    file_path = file.name


    loaded = Label(window, text=f"{file_name} is loaded")
    loaded.config(anchor="s")
    loaded.pack()

    if file is not None:
        if file_name.__contains__(".apk"):
            print(file)
            progress["value"] += 20
            window.update_idletasks()
            apk_decompile(file.name)

    else:
        content = file.read()

    with open(f'data_files/{file_name}', 'w') as f:
        f.write(content)
        f.close()


# def multiProc():


# decompile apk
def apk_decompile(apk_file):
    progress["value"] += 20
    apk_name = os.path.basename(apk_file)
    os.system(f"java -jar tools/apktool.jar d -f -r {apk_file} -o output/{apk_name}")

    loaded = Label(window, text=f"{file_name} successfully decompiled at output/{apk_name}")
    loaded.config(anchor=CENTER)
    loaded.pack()
    progress["value"] += 40
    window.update_idletasks()


# recompile and sign apk
def apk_recompile_sign(apk_file):
    apk_name = os.path.basename(apk_file)
    subprocess.call(f"java -jar tools/apktool.jar b -f -r --use-aapt2 output/{apk_file} -o data_files/obfuscated_apk/{apk_name}")
    time.sleep(3)
    subprocess.call(f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -storepass password -keystore tools/test.keystore data_files/obfuscated_apk/{apk_name} test")



# -------------------- Obfuscation Part --------------------
def obfuscate_smali_file():
    global main_smali_file_path
    folder = os.listdir(f"output/{file_name}")
    print('folder', folder)
    count = 0

    substring = "smali"
    substring2 = "example"
    for i in folder:
        if re.search(substring, i):
            f = f"output/{file_name}/{i}/com"
            sub_folder = os.listdir(f)
            print(sub_folder)
            for x in sub_folder:
                print(x)
                if re.search(substring2, x):
                    fx = f"output/{file_name}/{i}/com/{x}"
                    print(fx)
                    sub_fx = os.listdir(fx)
                    for z in sub_fx:
                        main_smali_file_path = f"output/{file_name}/{i}/com/{x}/{z}"
                        for e in Path().cwd().glob(f"{main_smali_file_path}/*.smali"):
                            count += 1
                            #print(e)
                            nocomment(e)
                            addjunkcode(e)
    loaded = Label(window, text=f"{count} Smali file obfuscated!")
    loaded.config(anchor=CENTER)
    loaded.pack()

def nocomment(inFile):
    print(inFile)
    open_file = open(inFile, "r")
    basename = os.path.basename(inFile)
    change = ""

    for line in open_file:
        result = re.findall(r'"(.*#.*)"', line)
        if not result:
            line = line.split("#", 1)
            print(line[0])
            change = change + str(line[0])
            print(change)
        else:
            change = change + line

    open_file.close()
    outFile = open(inFile, "w")
    #outFile = open(f"data_files/{basename}", "w")
    outFile.write(change)
    outFile.close()

def addjunkcode(smaliCode):
    flag1 = 0
    flag2 = 0
    functionNameFirst = ["important_", "necessary_", "mustHave_", "coolCool_"]
    functionNameSecond = ["function()", "statement()", "detail()", "coolStuff()"]
    counter = 0
    saltNOP = "nop\n\n"
    saltFUNCTIONback = ".end method\n"
    iterator = 0

    # [ Function Salting ]
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if lines[iterator] == ".end method\n":
                saltFUNCTIONfront = "\n.method public " + functionNameFirst[flag1] + functionNameSecond[flag2] + "Z\n"
                if flag1 != 3 and flag2 != 3:
                    lines.insert(iterator + 1, saltFUNCTIONfront)
                    lines.insert(iterator + 2, saltFUNCTIONback)
                    iterator += 3
                    flag2 += 1
                elif flag1 != 3 and flag2 == 3:
                    flag1 += 1
                    flag2 = 0
                    lines.insert(iterator + 1, saltFUNCTIONfront)
                    lines.insert(iterator + 2, saltFUNCTIONback)
                elif flag1 == 3 and flag2 < 3:
                    lines.insert(iterator + 1, saltFUNCTIONfront)
                    lines.insert(iterator + 2, saltFUNCTIONback)
                    flag2 += 1
                elif flag1 == 3 and flag2 == 3:
                    break
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()

    # reset iterator [ Salt with NOP ]
    iterator = 0
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if ".method" in lines[iterator]:
                randint = random.randint(3, 5)
                for i in range(1,randint):
                    lines.insert(iterator + i, saltNOP)
                iterator += 1
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()

    # reset iterator [ Salt with goto junk ]
    iterator = 0
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if "nop" in lines[iterator]:
                anotherRand = random.randint(1, 3)
                for i in range(0 ,anotherRand):
                    saltGOTOfront = "goto : gogo_" + str(counter) + "\n"
                    saltGOTOback = ": gogo_" + str(counter) + "\n\n"
                    lines.insert(iterator + i, saltGOTOfront)
                    lines.insert(iterator + 1 + i, saltGOTOback)
                    counter += 1
                    iterator += 2
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()

def test():
    rootDir = 'output'
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        print('Found directory: %s' % dirName)
        if "smali" in dirName:
            print("yes")
    for fname in fileList:
        print('\t%s' % fname)

def test():


    return None

# -------------------- GUI Window --------------------

btn = Button(window, text='Step 1: Open & Decompile', command=lambda: open_file()).pack(side=TOP, pady=10)
#btn2 = Button(window, text='Remove Comments', command=lambda: nocomment()).pack(side=TOP, pady=10)
btn3 = Button(window, text='Step 2: Obfuscate Smali', command=lambda: obfuscate_smali_file()).pack(side=TOP, pady=10)
btn4 = Button(window, text='Step 3: Recompile', command=lambda: apk_recompile_sign(file_name)).pack(side=TOP, pady=10)

progress = Progressbar(window, orient=HORIZONTAL, length=400, mode="determinate")
progress.pack(pady=20)

window.mainloop()
