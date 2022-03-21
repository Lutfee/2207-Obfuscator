# importing tkinter and tkinter.ttk
# and all their functions and classes
import os
import re
from tkinter import *
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
from pathlib import Path

#----------- Global Var -----------
content = ""
file_name = ""
main_smali_file_path = ""

window = Tk()
window.geometry('480x480')
window.config(background="light blue")
progress = Progressbar(window, orient=HORIZONTAL, length=400, mode="determinate")
progress.pack(pady=20)


# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    global content
    global file_name

    file = askopenfile(mode='r')
    progress["value"] += 20
    window.update_idletasks()
    file_name = os.path.basename(file.name)

    loaded = Label(window, text=f"{file_name} is loaded")
    loaded.config(anchor=CENTER)
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
    os.system("java -jar tools/apktool.jar d -f " + apk_file + " -o output/" + apk_name)

    loaded = Label(window, text=f"{file_name} successfully decompiled")
    loaded.config(anchor=CENTER)
    loaded.pack()
    progress["value"] += 40
    window.update_idletasks()


# -------------------- Obfuscation Part --------------------
def obfuscate_smali_file():
    global main_smali_file_path
    folder = os.listdir(f"output/{file_name}")
    print('folder',folder)
    initial_count = 0

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
                            print(e)
                            nocomment(e)



    print
    "All files ending with .py in folder %s:" % folder


    for f in Path().cwd().glob("../*.smali"):
        print(f)
        # do other stuff




def nocomment(inFile):
    print(inFile)
    open_file = open(inFile, "r")
    basename = os.path.basename(inFile)
    change = ""

    for line in open_file:
        line = line.split("#", 1)
        print(line[0])
        change = change + str(line[0])
        print(change)

    open_file.close()
    outFile = open(f"data_files/obfuscated_files/{basename}", "w")
    outFile.write(change)
    outFile.close()

def test():
    rootDir = 'output'
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        print('Found directory: %s' % dirName)
        if "smali" in dirName:
            print("yes")
    for fname in fileList:
        print('\t%s' % fname)

        # List all files and directories in the specified path
        print("Files and Directories in '% s':" % folder)
        for entry in obj:
            if entry.is_dir() or entry.is_file():
                print(entry.name)
                if entry.name == "smali":
                    for next in entry:
                        print(next)



# -------------------- GUI Window --------------------
btn = Button(window, text='Open', command=lambda: open_file()).pack(side=TOP, pady=10)
btn2 = Button(window, text='Remove Comments', command=lambda: nocomment()).pack(side=TOP, pady=10)
btn3 = Button(window, text='Save', command=lambda: obfuscate_smali_file()).pack(side=TOP, pady=10)

window.mainloop()
