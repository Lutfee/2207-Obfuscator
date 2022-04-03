# importing tkinter and tkinter.ttk
# and all their functions and classes
import os
import random
import re
import shutil
import subprocess
import time
from glob import glob
from pathlib import Path
from tkinter import *
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
import tkinter.scrolledtext as st
from tkinter import Menu, messagebox
from tkinter.ttk import *

# ----------- Global Var -----------
content = ""
file_name = ""
file_path = ""
main_smali_file_path = ""

window = Tk()
window.title("Simple Obfuscator")
window.geometry('520x500')
window.config(background="light blue")


# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    global content
    global file_name
    global file_path

    progress["value"] = 0
    file = askopenfile(mode='r')
    window.update_idletasks()
    file_name = os.path.basename(file.name)
    file_path = file.name
    textLog.insert(END, f"{file_name} is loaded\n")
    textLog.yview(END)

    if file is not None:
        if file_name.__contains__(".apk"):
            print(file)
            # progress["value"] += 10
            pogBar(progress)
            window.update_idletasks()
            apk_decompile(file.name)

    else:
        content = file.read()

    with open(f'data_files/{file_name}', 'w') as f:
        f.write(content)
        f.close()

    textLog.insert(END, "*Step 1 Complete*\n", 'complete')
    textLog.yview(END)


# decompile apk
def apk_decompile(apk_file):
    progress["value"] += 20
    apk_name = os.path.basename(apk_file)
    os.system(f"java -jar tools/apktool.jar d -f -r {apk_file} -o original_apk/{apk_name}")
    os.system(f"java -jar tools/apktool.jar d -f -r {apk_file} -o output/{apk_name}")
    textLog.insert(END, f"{file_name} successfully decompiled at output/{apk_name}\n")
    textLog.yview(END)
    progress["value"] += 10
    window.update_idletasks()


# recompile and sign apk
def apk_recompile_sign(apk_file):
    pogBar(progress)
    apk_name = os.path.basename(apk_file)
    subprocess.call(
        f"java -jar tools/apktool.jar b -f -r --use-aapt2 output/{apk_file} -o data_files/obfuscated_apk/{apk_name}")
    time.sleep(3)
    subprocess.call(
        f"jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -storepass password -keystore tools/test.keystore data_files/obfuscated_apk/{apk_name} test")
    subprocess.call(f"jarsigner -verify -verbose -certs data_files/obfuscated_apk/{apk_name}")
    subprocess.call(
        f"tools/zipalign -v 4 data_files/obfuscated_apk/{apk_name} data_files/obfuscated_apk/aligned-{apk_name}")
    textLog.insert(END, f"{file_name} successfully recompiled at data_files/obfuscated_apk/aligned-{apk_name}\n")
    textLog.yview(END)
    progress["value"] += 40
    textLog.insert(END, "*Step 3 Complete*\n", 'complete')
    textLog.yview(END)


# -------------------- Obfuscation Part --------------------
def obfuscate_smali_file():
    global main_smali_file_path
    folder = os.listdir(f"output/{file_name}")
    print('folder', folder)
    count = 0
    pogBar(progress)
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

                            # print(e)
                            nocomment(e)
                            insertIFcondition(e)
                            addjunkcode(e)

    textLog.insert(END, f"{count} Smali file obfuscated!\n")
    textLog.yview(END)
    progress["value"] += 15
    textLog.insert(END, "*Step 2 Complete*\n", 'complete')
    textLog.yview(END)


def nocomment(inFile):
    textLog.yview(END)
    print(inFile)
    open_file = open(inFile, "r")
    change = ""
    regex = r'"(.*#.*)"'

    for line in open_file:
        results = re.findall(regex, line)
        if results:
            change = change + line
        else:
            line = line.split("#", 1)
            print(line[0])
            change = change + str(line[0])
            print(change)

    open_file.close()
    outFile = open(inFile, "w")
    outFile.write(change)
    outFile.close()


def addjunkcode(smaliCode):
    counter = 0
    saltNOP = "nop\n\n"

    # reset iterator [ Salt with NOP ]
    iterator = 0
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if ".method" in lines[iterator]:
                randint = random.randint(3, 5)
                for i in range(1, randint):
                    lines.insert(iterator + i, saltNOP)
                iterator += 1
            if "if-le" in lines[iterator]:
                check = [int(check) for check in re.findall(r'-?\d+\.?\d*', lines[iterator])]
                try:
                    if int(check[2]) > 500:
                        randint = random.randint(3, 5)
                        for i in range(1, randint):
                            lines.insert(iterator + i, saltNOP)
                except:
                    pass
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
                for i in range(0, anotherRand):
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


def insertIFcondition(file):
    if "array" in str(file):
        return
    with open(file, 'r') as f:
        data = f.readlines()
    size = len(data)
    i = 0
    while i < size:
        if ".locals" in data[i]:
            currentvariablevalue = int(data[i].split(".locals")[1].strip("\n"))
            if currentvariablevalue > 7:
                return
            data[i] = ".locals " + str(currentvariablevalue + 2) + "\n"
            variable_one = "v" + str(int(currentvariablevalue))
            variable_two = "v" + str(int(currentvariablevalue + 1))
            firstvariablevalue = "const/4 " + str(variable_one) + ", " + str(hex(random.randint(5, 7))) + "\n"
            secondvariablevalue = "const/4 " + str(variable_two) + ", " + str(hex(random.randint(-8, 4))) + "\n"
            condvariable = ":cond_" + str(random.randint(500, 1000)) + "\n"
            ifstatement = "if-le " + variable_one + "," + variable_two + "," + condvariable + "\n"

            data.insert(i + 1, condvariable)
            # insert junk here
            data.insert(i + 1, ifstatement)
            data.insert(i + 1, secondvariablevalue)
            data.insert(i + 1, firstvariablevalue)

        size = len(data)
        i += 1
        # data.close()
        with open(file, 'w') as f:
            f.writelines(data)


def clearFiles():
    textLog.insert(END, "Folders Cleared\n", 'complete')
    textLog.yview(END)
    files_obs = glob('data_files/obfuscated_apk/*')
    files_ori = glob('original_apk/*')
    files_output = glob('output/*')
    file_apk = glob('data_files/*.apk')

    for f in files_obs:
        os.remove(f)
    for f in files_ori:
        shutil.rmtree(f)
    for f in files_output:
        shutil.rmtree(f)
    for f in file_apk:
        os.remove(f)


def destroy(item):
    item.destroy()


def pogBar(bar):
    for i in range(5):
        bar["value"] += i
        window.update_idletasks()
        time.sleep(0.5)


def openNewWindow():
    def openOri():
        tf = askopenfile(
            initialdir="original_apk",
            title="Open Smali file",
            filetypes=(("Smali Files", "*.smali"),)
        )
        print(tf)
        file = tf.name
        oriPath.insert(END, tf)
        tf = open(file)  # or tf = open(tf, 'r')
        data = tf.read()
        textOriginal.insert(END, data)
        tf.close()

    def openObfuse():
        tf = askopenfile(
            initialdir="output",
            title="Open Smali file",
            filetypes=(("Smali Files", "*.smali"),)
        )
        print(tf)
        file = tf.name
        obfusPath.insert(END, file)
        tf = open(file)  # or tf = open(tf, 'r')
        data = tf.read()
        textObfuscate.insert(END, data)
        tf.close()

    compareWindow = Toplevel(window)
    compareWindow.title("Compare Smali Files")
    # sets the geometry of toplevel
    compareWindow.geometry("740x780")

    topFrame = Frame(compareWindow)
    btmFrame = Frame(compareWindow)

    textOriginal = Text(topFrame, width=40, height=40)
    textObfuscate = Text(topFrame, width=40, height=40)
    originalLabel = Label(topFrame, text="ORIGINAL")
    obfuscateLabel = Label(topFrame, text="OBFUSCATED")

    originalLabel.grid(row=0, column=0, sticky=W, pady=10, padx=10)
    obfuscateLabel.grid(row=0, column=2, sticky=W, pady=10, padx=10)
    textOriginal.grid(row=1, column=0, sticky=W, pady=10, padx=10)
    textObfuscate.grid(row=1, column=2, sticky=W, pady=10, padx=10)

    oriPath = Entry(btmFrame, width=90)
    obfusPath = Entry(btmFrame, width=90)
    oriPath.grid(row=3, column=1, pady=2, padx=10)
    obfusPath.grid(row=4, column=1, pady=2, padx=10)

    Button(
        btmFrame,
        text="Open Original",
        command=openOri
    ).grid(row=3, column=0, pady=2, padx=10)
    Button(
        btmFrame,
        text="Open Obfuscated",
        command=openObfuse
    ).grid(row=4, column=0, pady=2, padx=10)
    topFrame.pack(side=TOP)
    btmFrame.pack(side=BOTTOM, pady=10)
    compareWindow.mainloop()


def openManual():
    manualWindow = Toplevel(window)
    manualWindow.title("Manual")
    # sets the geometry of toplevel
    manualWindow.geometry("580x400")
    manual_text = Text(manualWindow, width=40, height=40)
    manual_file = open("tools/manual.txt", 'r')  # or tf = open(tf, 'r')
    data = manual_file.read()
    manual_text.insert(END, data)
    manual_file.close()
    manual_text.pack(fill=BOTH)


def clearWarning():
    MsgBox = messagebox.askquestion('Warning',
                                    'Are you sure you want to clear all old data?\n *Save a copy of the obfuscated apk before clearing*',
                                    icon='warning')
    if MsgBox == 'yes':
        clearFiles()


# -------------------- GUI Window --------------------
btn1 = Button(window, text='Step 1: Open & Decompile APK', command=lambda: open_file()).pack(side=TOP, pady=10)
btn2 = Button(window, text='Step 2: Obfuscate Smali', command=lambda: obfuscate_smali_file()).pack(side=TOP, pady=10)
btn3 = Button(window, text='Step 3: Recompile', command=lambda: apk_recompile_sign(file_name)).pack(side=TOP, pady=10)
optionLabel = Label(window, text="OPTIONAL")
optionLabel.config(anchor=CENTER)
optionLabel.pack(side=TOP, pady=10)
btn4 = Button(window, text='Step 4: Compare Smali Files', command=lambda: openNewWindow()).pack(side=TOP, pady=10)
btn4 = Button(window, text='CLEAR OLD DATA', command=lambda: clearWarning()).pack(side=TOP, pady=10)

progress = Progressbar(window, orient=HORIZONTAL, length=400, mode="determinate")
progress.pack(pady=20)

textLog = st.ScrolledText(window, width=40, height=40)
textLog.tag_config('complete', background="yellow", foreground="green")
textLog.tag_config('process', background="yellow", foreground="red")
textLog.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

menubar = Menu(window)
window.config(menu=menubar)
help_menu = Menu(menubar)

help_menu.add_command(label="Manual", command=lambda: openManual())
menubar.add_cascade(label="Help", menu=help_menu)

window.mainloop()
